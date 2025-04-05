import os
import subprocess
from datetime import datetime
import redis
from typing import List
from random import choice
import uuid

from django.conf import settings

from .util.util import generate_random_alphanumeric_sequence

class ResourceUnavailable(Exception):
    pass

class ClusterNodeManager:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=os.getenv('REDIS_HOST'),
            port=os.getenv('REDIS_PORT'),
            db=os.getenv('REDIS_DB'),
            password=os.getenv('REDIS_PASSWORD'),
            decode_responses=True
        )

    def get_available_nodes(self) -> List[str]:
        """Obtém todos os nós do cluster com GPU disponível via PBS/TORQUE"""
        try:
            cmd = "pbsnodes | awk '/^[a-zA-Z]/{node=$1} /state = free/{free=1} /NOGPU/{free=0} /^$/{if(free==1) print node; free=0}'"
            
            # Executa comando pbsnodes para listar nós
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                shell=True
            )
            
            # Parse a saída do comando para extrair nós com GPU
            nodes = self._parse_pbsnodes_output(result.stdout)
            
            return nodes
        except subprocess.CalledProcessError as e:
            print(f"Erro ao executar pbsnodes: {e}")
            return []

    def _parse_pbsnodes_output(self, output: str) -> List[str]:
        """Parse da saída do pbsnodes para encontrar nós com GPU livre"""
        nodes = []
        
        for node in output.splitlines():
            if node.strip() != '':
                nodes.append(node.strip())
        
        return nodes

    def mark_node_as_busy(self, node_name: str):
        """Marca um nó como ocupado por um job específico"""
        key = f"cluster:node:{node_name}"
        
        reservation_id = uuid.uuid4().hex
        
        self.redis_client.hset(key, mapping={
            'reservation_id': reservation_id,
            'timestamp': datetime.now().isoformat()
        })
        
        return reservation_id

    def mark_node_as_free(self, node_name: str):
        """Marca um nó como livre"""
        key = f"cluster:node:{node_name}"
        self.redis_client.delete(key)

    def get_reservation_id_from_node_name(self, node_name: str) -> str:
        return self.redis_client.hget(f"cluster:node:{node_name}", "reservation_id")

    def get_free_gpu_node(self) -> str:
        """Obtém um nó livre com GPU, considerando os nós já em uso por outros workers"""
        available_nodes = self.get_available_nodes()
        
        # Filtra nós que já estão em uso por outros workers
        free_nodes = [
            node for node in available_nodes
            if not self.redis_client.exists(f"cluster:node:{node}")
        ]
        
        return choice(free_nodes) if free_nodes else ""

    def is_node_reservation_valid(self, node_name: str, reservation_id: str):
        return True if self.redis_client.hget(f"cluster:node:{node_name}", "reservation_id") == reservation_id else False

    def reserve_free_gpu_node(self) -> str:
        free_gpu_node = self.get_free_gpu_node()
        
        if free_gpu_node != "":
            self.mark_node_as_busy(node_name=free_gpu_node)
            
        return free_gpu_node
    
    def cleanup_stale_nodes(self, max_age_hours: int = 2):
        """Limpa registros antigos de nós ocupados"""
        threshold = datetime.now().timestamp() - (max_age_hours * 3600)
        
        # Lista todas as chaves de nós
        for key in self.redis_client.scan_iter("cluster:node:*"):
            node_data = self.redis_client.hgetall(key)
            if node_data:
                timestamp = datetime.fromisoformat(node_data['timestamp']).timestamp()
                if timestamp < threshold:
                    self.redis_client.delete(key)

def replace_job_id_in_template(script_content: str):
    JOB_ID_SIZE = 10
    job_id = generate_random_alphanumeric_sequence(JOB_ID_SIZE)
    
    script_content = script_content.replace("{{job_id}}", job_id)
    
    return script_content

def replace_node_name_in_template(script_content: str, node_name: str):
    script_content = script_content.replace("{{node_name}}", node_name)
    return script_content

def replace_java_home_in_template(script_content: str):
    script_content = script_content.replace("{{JAVA_HOME}}", os.getenv('JAVA_HOME'))
    return script_content

def replace_conda_env_in_template(script_content: str):
    script_content = script_content.replace("{{conda_env}}", os.getenv('CONDA_ENV'))
    return script_content

def replace_pdf2chemicals_path_in_template(script_content: str):
    pdf2chemicals_path = get_pdf2chemicals_path()
    
    script_content = script_content.replace("{{pdf2chemicals_path}}", pdf2chemicals_path)
    return script_content

def replace_pdf_path_in_template(script_content: str, pdf_path: str):
    script_content = script_content.replace("{{pdf_path}}", pdf_path)
    return script_content

def replace_output_dir_in_template(script_content: str, output_dir: str):
    script_content = script_content.replace("{{output_dir}}", output_dir)
    return script_content

def replace_export_format_in_template(script_content: str, export_format: str):
    export_format_content = "--format json "
    
    if export_format == 'zip':
        export_format_content += f"--format {export_format} "
    
    script_content = script_content.replace("{{export_format}}", export_format_content)
    
    return script_content

def replace_conf_formats_in_template(script_content: str, conf_formats: list[str]):
    conf_formats_content = ""
    
    for fmt in conf_formats:
        conf_formats_content += f"-conf-fmt {fmt} "
        
    script_content = script_content.replace("{{conf_formats}}", conf_formats_content)
    
    return script_content

def replace_structure_formats_in_template(script_content: str, structure_formats: list[str]):
    structure_formats_content = ""
    
    for fmt in structure_formats:
        structure_formats_content += f"-structure-fmt {fmt} "
        
    script_content = script_content.replace("{{structure_formats}}", structure_formats_content)
    
    return script_content

def replace_filename_formats_in_template(script_content: str, filename: str):
    script_content = script_content.replace("{{filename}}", f"--filename {filename}")
    return script_content

# Function to generate a script name with a random suffix
def generate_script_name(base_name="pbs-script") -> str:
    """
    Generates a unique PBS script name with a uuid4 suffix.
    Returns: The script name with the random suffix.
    """
        
    return f"{base_name}-{uuid.uuid4()}.pbs"

# Function to save the generated script in the media directory
def save_script(script_content):
    """
    Saves the PBS script content to a file inside MEDIA_ROOT.
    
    Parameters:
    - script_content: The content of the PBS script.
    - script_name: The name of the file where the script will be saved.
    """
    # Directory to save PBS scripts
    pbs_scripts_dir = os.path.join(settings.MEDIA_ROOT, 'pbs_scripts')
    
    # Generate the script name with a random suffix
    script_name = generate_script_name()
    
    # Ensure the directory exists, otherwise create it
    os.makedirs(pbs_scripts_dir, exist_ok=True)

    # Full path to the file where the script will be saved
    script_path = os.path.join(pbs_scripts_dir, script_name)

    # Save the script to the file
    with open(script_path, 'w') as file:
        file.write(script_content)
    
    return script_path 

def get_pdf2chemicals_pbs_template_path():
    return os.path.join(os.path.dirname(__file__), 'pbs_template', 'pdf2chemicals_pbs_template.pbs')

def get_pdf2chemicals_path():
    return os.path.join(settings.BASE_ROOT_DIR, 'libs', 'pdf2chemicals', 'pdf2chemicals.py')
                   
def get_pbs_script_content():
    template_path = get_pdf2chemicals_pbs_template_path()
    
    # Load the template content
    with open(template_path, 'r') as file:
        script_content = file.read()
        
    return script_content
 
def generate_pbs_script(pdf_path, output_dir, export_format, conf_formats, structure_formats, filename, node_name):
    """
    Generates a PBS script for chemical processing by replacing the necessary variables.
    
    Parameters:
    - template_path: Path to the PBS template file.
    - pdf2chemicals_path: Path to the pdf2chemicals script.
    - pdf_path: Path to the PDF to be processed.
    - output_dir: Directory where the results will be saved.
    - json_prefix: Prefix for the output JSON file.
    """
    script_content = get_pbs_script_content()
    
    script_content = replace_job_id_in_template(script_content)
    script_content = replace_node_name_in_template(script_content, node_name)
    script_content = replace_java_home_in_template(script_content)
    script_content = replace_conda_env_in_template(script_content)
    script_content = replace_pdf2chemicals_path_in_template(script_content)
    script_content = replace_pdf_path_in_template(script_content, pdf_path)
    script_content = replace_output_dir_in_template(script_content, output_dir)
    script_content = replace_export_format_in_template(script_content, export_format)
    script_content = replace_conf_formats_in_template(script_content, conf_formats)
    script_content = replace_structure_formats_in_template(script_content, structure_formats)
    script_content = replace_filename_formats_in_template(script_content, filename)
    
    # Save the generated script in the media directory
    script_path = save_script(script_content)
    
    return script_path

def is_pbs_job_completed(job_id: str) -> bool:
    """Checks if a PBS/Torque job is completed based on tracejob and grep command

    Args:
        job_id (str): Job ID to be checked

    Returns:
        bool: True if the job is complete, False otherwise.
    """
    try:
        # Comando para buscar palavras-chave diretamente com grep
        result = subprocess.run(
            f"tracejob -q -n 30 {job_id} | grep -qE 'resources_used|Exit_status|array_index'",
            shell=True
        )

        # Retorna True se grep encontrou algo, False caso contrário
        return result.returncode == 0

    except FileNotFoundError:
        print("Error: tracejob or grep not found. Check your installation.")
        return False