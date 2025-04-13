import os
import json
import subprocess
import uuid
import logging

from celery import chain, group, shared_task

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from tasks.models import UserTask
from tasks.util.tasks import BaseTask
from user.models import User
from pdf2chemicals_service.util.tasks import ChainedTask
from chemicals.tasks import post_chemical

from .util.util import file_exists, remove_file
from .cluster import (
    ResourceUnavailable,
    ClusterNodeManager, 
    generate_pbs_script, 
    is_pbs_job_completed
)

logger = logging.getLogger(__name__)

@shared_task(
    base=ChainedTask,
    name='pdf2chemicals_service.tasks.pdf2chemicals_tasks_extract_and_save_chemicals_from_pdf', 
    bind=True,  
    acks_late=True,
    queue='pdf2chemicals_tasks',
    autoretry_for=(Exception,),
    retry_backoff=True,
    task_reject_on_worker_lost=True
)
def extract_and_save_chemicals_from_pdf(self, *args, **kwargs):
    if 'task_id' not in kwargs:
        kwargs['task_id'] = str(uuid.uuid4())
    
    task_id = kwargs['task_id']
    output_dir = 'pdf2chemicals_output'
    output_filename = str(uuid.uuid4())

    try:
        user = User.objects.get(id=kwargs['user_id'])
    except ObjectDoesNotExist:
        raise self.retry(countdown=10, max_retries=5)

    # Definindo o workflow
    workflow = chain(
        create_pbs_script_task.s(
            pdf_path=kwargs['pdf_path'], 
            export_format=kwargs['export_format'], 
            conf_formats=kwargs['conf_formats'], 
            structure_formats=kwargs['structure_formats'],
            output_dir=output_dir,
            output_filename=output_filename 
        ),
        send_pdf2chemicals_hpc_task.s(),
        monitor_pdf2chemicals_job.s(),
        load_chemical_from_json.s(export_format=kwargs['export_format']),
        post_chemicals_in_db.s(user_id=kwargs['user_id']),
        return_pdf2chemicals_task_final_result.s(
            export_format=kwargs['export_format'],
            output_dir=output_dir,
            output_filename=output_filename,
            task_id=task_id
        )
    )
    
    # Aplicando o workflow com link_error
    result = workflow.apply_async(
        link_error=handle_pdf2chemicals_task_error.s(
            pdf_path=kwargs['pdf_path'],
            user_id=kwargs['user_id'],
            original_filename=kwargs['original_filename'],
            export_format=kwargs['export_format'],
            conf_formats=kwargs['conf_formats'],
            structure_formats=kwargs['structure_formats'],
            task_id=task_id
        ),
        task_id=task_id
    )
    
    # Melhorando o gerenciamento da task no banco
    user_task, _ = UserTask.objects.update_or_create(
        task_id=task_id,
        defaults={
            "user": user,
            "task_name": extract_and_save_chemicals_from_pdf.name,
            "status": result.status,
            "label": f'PDF2Chemicals: {kwargs['original_filename']}'
        }
    )
    
    print(user_task)
    
    return task_id

@shared_task(
    base=ChainedTask,
    name='pdf2chemicals_service.tasks.handle_pdf2chemicals_task_error',
    bind=True,
    acks_late=True,
    queue='pdf2chemicals_tasks'
)
def handle_pdf2chemicals_task_error(self, *args, **kwargs):
    # Extraindo os parâmetros necessários de kwargs
    user_id = kwargs.get('user_id')
    pdf_path = kwargs.get('pdf_path')
    original_filename = kwargs.get('original_filename')
    export_format = kwargs.get('export_format')
    conf_formats = kwargs.get('conf_formats')
    structure_formats = kwargs.get('structure_formats')
    task_id = kwargs.get('task_id', str(uuid.uuid4()))
    
    task = UserTask.objects.filter(task_id=task_id).first()
    
    if not task:
        logger.error(f"Task {task_id} not found.")
        return
    
    if task.status in ["REVOKED", "RETRY", "SUCCESS"]:
        logger.info(f"Skipping retry for task {task_id} as it has status {task.status}.")
        return
    
    logger.info(f"Retrying task {task_id} in 5 minutes for user {user_id}.")
    
    extract_and_save_chemicals_from_pdf.apply_async(
        kwargs={
            'user_id': user_id,
            'pdf_path': pdf_path,
            'original_filename': original_filename,
            'export_format': export_format,
            'conf_formats': conf_formats,
            'structure_formats': structure_formats,
            'task_id': task_id
        },
        countdown=60 * 5  # Waits 5 minutes to retry.
    )
    
    UserTask.objects.update_or_create(
        task_id=task_id, 
        defaults = {
            'status': 'RETRY'
        }
    )

@shared_task(
    name='pdf2chemicals_service.tasks.pdf2chemicals_tasks_post_chemicals_in_db', 
    bind=True,  
    acks_late=True,
    queue='pdf2chemicals_tasks',
    priority=1,
    autoretry_for=(Exception,),
    max_retries=5,
    default_retry_delay=60 * 2, # Waits 2 minutes to execute 
    retry_backoff=True,
    task_reject_on_worker_lost=True
)
def post_chemicals_in_db(self, chemical_list, user_id):
    post_chemical_group = group(
        post_chemical.s(chemical=chemical, user_id=user_id) 
        for chemical in chemical_list
    )
    
    post_chemical_group.apply_async()

@shared_task(
    base=ChainedTask,
    name='pdf2chemicals_service.tasks.pdf2chemicals_tasks_create_pbs_script_task',
    bind=True,
    acks_late=True,
    queue='pdf2chemicals_tasks',
    priority=1,
    max_retries=None,
    default_retry_delay=60 * 2,  # Aguarda 2 minutos para executar
    retry_backoff=True,
    task_reject_on_worker_lost=True
)
def create_pbs_script_task(self, *args, **kwargs):
    output_abs_dir = os.path.join(settings.MEDIA_ROOT, kwargs['output_dir'])
    # Geração do caminho e nome do arquivo JSON
    json_filepath = os.path.join(output_abs_dir, f'{kwargs['output_filename']}.json')

    # Caminho absoluto do PDF
    absolute_pdf_path = os.path.join(settings.MEDIA_ROOT, kwargs['pdf_path'])

    # Reserva de um nó no cluster
    cluster_node_manager = ClusterNodeManager()
    node_name = cluster_node_manager.reserve_free_gpu_node()

    if node_name == '':
        raise ResourceUnavailable("No pbs node is available at the moment.")

    reservation_id = cluster_node_manager.get_reservation_id_from_node_name(node_name)

    # Geração do script PBS
    script_path = generate_pbs_script(
        pdf_path=absolute_pdf_path,
        output_dir=output_abs_dir,
        export_format=kwargs['export_format'], 
        conf_formats=kwargs['conf_formats'], 
        structure_formats=kwargs['structure_formats'],
        filename=kwargs['output_filename'],
        node_name=node_name
    )

    # Verificação da existência do script
    if not file_exists(script_path):
        cluster_node_manager.mark_node_as_free(node_name)
        raise FileExistsError(f"PBS/TORQUE script file {script_path} not found.")

    # Verificação da validade da reserva
    if not cluster_node_manager.is_node_reservation_valid(node_name, reservation_id):
        remove_file(script_path)
        raise KeyError("Cluster node reservation id is invalid.")

    # Retorno dos dados para a próxima task
    return {
        'pbs_script_path': script_path,
        'node_name': node_name,
        'reservation_id': reservation_id,
        'json_filepath': json_filepath,
        'pdf_path': absolute_pdf_path
    }

@shared_task(
    base=ChainedTask,
    name='pdf2chemicals_service.tasks.pdf2chemicals_tasks_send_pdf2chemicals_hpc_task',
    bind=True,
    acks_late=True,
    queue='pdf2chemicals_tasks',
    priority=1,
    max_retries=None,
    default_retry_delay=60 * 2,  # Aguarda 2 minutos para executar
    retry_backoff=True,
    task_reject_on_worker_lost=True
)
def send_pdf2chemicals_hpc_task(self, *args, **kwargs):
    # Dados recebidos da task anterior
    pbs_script_path = kwargs.get('pbs_script_path')
    node_name = kwargs.get('node_name')
    reservation_id = kwargs.get('reservation_id')
    json_filepath = kwargs.get('json_filepath')
    pdf_path = kwargs.get('pdf_path')

    # Instanciação do gerenciador de nós
    cluster_node_manager = ClusterNodeManager()

    # Verificação adicional da validade da reserva (opcional, mas recomendado)
    if not cluster_node_manager.is_node_reservation_valid(node_name, reservation_id):
        remove_file(pbs_script_path)
        raise KeyError("Cluster node reservation id is invalid.")

    # Comando para submeter o job ao cluster
    cmd = f'sh -c "(cd {os.getenv("TORQUE_USER_HOME")} && {os.getenv("TORQUE_HOME")}/bin/qsub {pbs_script_path})"'

    # Execução do comando
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True,
        check=False
    )

    # Tratamento de falhas na submissão
    if result.returncode != 0:
        remove_file(pbs_script_path)
        cluster_node_manager.mark_node_as_free(node_name)
        raise subprocess.CalledProcessError('Job was not received in the HPC cluster.')

    job_id = result.stdout.strip()

    # Retorno dos dados
    return {
        'pbs_script_path': pbs_script_path,
        'job_id': job_id,
        'node_name': node_name,
        'json_filepath': json_filepath,
        'pdf_path': pdf_path
    }

@shared_task(
    base=ChainedTask,
    name='pdf2chemicals_service.tasks.pdf2chemicals_tasks_monitor_pdf2chemicals_job', 
    bind=True,  
    acks_late=True,
    queue='pdf2chemicals_tasks',
    priority=1,
    max_retries=None,
    default_retry_delay=60 * 5, # Waits 5 minutes to execute 
    retry_backoff=True,
    task_reject_on_worker_lost=True
)
def monitor_pdf2chemicals_job(self, *args, **kwargs):
    """
    Task to monitor the directory and detect the JSON file.
    """
    if not is_pbs_job_completed(kwargs['job_id']):
        self.retry()
    
    cluster_node_manager = ClusterNodeManager()
    
    cluster_node_manager.mark_node_as_free(kwargs['node_name'])
    
    remove_file(kwargs['pbs_script_path'])
    
    if not file_exists(kwargs['json_filepath']):
        raise FileExistsError("Json file not found. PBS/TORQUE cluster job executed unsuccessfully.")
    
    remove_file(kwargs['pdf_path'])
    
    return {
        'json_filepath': kwargs['json_filepath']
    }
    
@shared_task(
    base=ChainedTask,
    name='chemicals.tasks.pdf2chemicals_tasks_load_chemical_from_json', 
    bind=True, 
    queue='pdf2chemicals_tasks',
    priority=10,
    autoretry_for=(Exception,),
    max_retries=5,
    default_retry_delay=60 * 2, # Waits 2 minutes to execute 
    retry_backoff=True,
    task_reject_on_worker_lost=True
)
def load_chemical_from_json(self, *args, **kwargs):
    with open(kwargs['json_filepath'], mode='r') as json_file:
        chemical_list = json.load(json_file)
    
    if kwargs['export_format'] != 'json':
        remove_file(kwargs['json_filepath'])
    
    return chemical_list

@shared_task(
    base=ChainedTask,
    name='pdf2chemicals_service.tasks.pdf2chemicals_tasks_return_pdf2chemicals_task_final_result', 
    bind=True,  
    acks_late=True,
    queue='pdf2chemicals_tasks',
    priority=1,
    autoretry_for=(Exception,),
    max_retries=5,
    default_retry_delay=60 * 2, # Waits 2 minutes to execute 
    retry_backoff=True,
    task_reject_on_worker_lost=True
)
def return_pdf2chemicals_task_final_result(self, *args, **kwargs):
    output_filepath = os.path.join(kwargs['output_dir'], f'{kwargs['output_filename']}.{kwargs['export_format']}')
    
    result = {
        'format': kwargs['export_format'],
        'output_filepath': output_filepath
    }
    
    user_task, _ = UserTask.objects.update_or_create(
        task_id=kwargs['task_id'],
        defaults={
            "status": 'SUCCESS',
            "result": result
        }
    )
    
    print(user_task)
