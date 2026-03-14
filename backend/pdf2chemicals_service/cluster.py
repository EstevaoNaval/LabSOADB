import os
import re
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
            host=os.getenv("REDIS_HOST"),
            port=os.getenv("REDIS_PORT"),
            db=os.getenv("REDIS_DB"),
            password=os.getenv("REDIS_PASSWORD"),
            decode_responses=True,
        )

    def get_available_nodes(self) -> List[str]:
        """Obtém todos os nós do cluster com GPU disponível via PBS/TORQUE"""
        try:
            cmd = "pbsnodes | awk '/^[a-zA-Z]/{node=$1} /state = free/{free=1} /NOGPU/{free=0} /^$/{if(free==1) print node; free=0}'"

            # Executa comando pbsnodes para listar nós
            result = subprocess.run(
                cmd, capture_output=True, text=True, check=True, shell=True
            )

            # Parse a saída do comando para extrair nós com GPU
            nodes = self._parse_pbsnodes_output(result.stdout)

            return nodes
        except subprocess.CalledProcessError as e:
            print(f"Failed to execute pbsnodes: {e}")
            return []

    def _parse_pbsnodes_output(self, output: str) -> List[str]:
        """Parse da saída do pbsnodes para encontrar nós com GPU livre"""
        nodes = []

        for node in output.splitlines():
            if node.strip() != "":
                nodes.append(node.strip())

        return nodes

    def _mark_node_as_busy(self, node_name: str):
        """Marca um nó como ocupado por um job específico"""
        key = f"cluster:node:{node_name}"

        reservation_id = uuid.uuid4().hex

        self.redis_client.hset(
            key,
            mapping={
                "reservation_id": reservation_id,
                "timestamp": datetime.now().isoformat(),
            },
        )

        return reservation_id

    def mark_node_as_available(self, node_name: str):
        """Marca um nó como livre"""
        key = f"cluster:node:{node_name}"
        self.redis_client.delete(key)

    def get_reservation_id_from_node_name(self, node_name: str) -> str:
        return self.redis_client.hget(f"cluster:node:{node_name}", "reservation_id")

    def get_available_gpu_node(self) -> str:
        """Obtém um nó livre com GPU, considerando os nós já em uso por outros workers"""
        available_nodes = self.get_available_nodes()

        # Filtra nós que já estão em uso por outros workers
        available_nodes = [
            node
            for node in available_nodes
            if not self.redis_client.exists(f"cluster:node:{node}")
        ]

        return choice(available_nodes) if available_nodes else ""

    def is_node_reservation_valid(self, node_name: str, reservation_id: str):
        return (
            True
            if self.get_reservation_id_from_node_name(node_name) == reservation_id
            else False
        )

    def reserve_available_gpu_node(self) -> str:
        available_gpu_node = self.get_available_gpu_node()

        if available_gpu_node != "":
            self._mark_node_as_busy(node_name=available_gpu_node)
            return available_gpu_node

        return ""

    def cleanup_stale_nodes(self, max_age_hours: int = 7):
        """Limpa registros antigos de nós ocupados"""
        threshold = datetime.now().timestamp() - (max_age_hours * 60 * 60)

        # Lista todas as chaves de nós
        for key in self.redis_client.scan_iter("cluster:node:*"):
            node_data = self.redis_client.hgetall(key)
            if node_data:
                timestamp = datetime.fromisoformat(node_data["timestamp"]).timestamp()
                if timestamp < threshold:
                    self.redis_client.delete(key)


def delete_hpc_job(job_id: str):
    cmd = (
        f'sh -c "(cd {os.getenv("TORQUE_USER_HOME")} && '
        f'{os.getenv("TORQUE_HOME")}/bin/qdel {job_id})"'
    )

    result = subprocess.run(
        cmd, shell=True, capture_output=True, text=True, check=False
    )


def replace_job_id_in_template(script_content: str):
    JOB_ID_SIZE = 10
    job_id = generate_random_alphanumeric_sequence(JOB_ID_SIZE)

    script_content = script_content.replace("{{job_id}}", job_id)

    return script_content


def replace_node_name_in_template(script_content: str, node_name: str):
    script_content = script_content.replace("{{node_name}}", node_name)
    return script_content


def replace_java_home_in_template(script_content: str):
    script_content = script_content.replace("{{JAVA_HOME}}", os.getenv("JAVA_HOME"))
    return script_content


def replace_conda_env_in_template(script_content: str):
    script_content = script_content.replace("{{conda_env}}", os.getenv("CONDA_ENV"))
    return script_content


def replace_pdf2chemicals_path_in_template(script_content: str):
    pdf2chemicals_path = get_pdf2chemicals_path()

    script_content = script_content.replace(
        "{{pdf2chemicals_path}}", pdf2chemicals_path
    )
    return script_content


def replace_pdf_path_in_template(script_content: str, pdf_path: str):
    script_content = script_content.replace("{{pdf_path}}", pdf_path)
    return script_content


def replace_output_dir_in_template(script_content: str, output_dir: str):
    script_content = script_content.replace("{{output_dir}}", output_dir)
    return script_content


def replace_export_format_in_template(script_content: str, export_format: str):
    export_format_content = "--format json "

    if export_format == "zip":
        export_format_content += f"--format {export_format} "

    script_content = script_content.replace("{{export_format}}", export_format_content)

    return script_content


def replace_conf_formats_in_template(script_content: str, conf_formats: list[str]):
    conf_formats_content = ""

    for fmt in conf_formats:
        conf_formats_content += f"-conf-fmt {fmt} "

    script_content = script_content.replace("{{conf_formats}}", conf_formats_content)

    return script_content


def replace_structure_formats_in_template(
    script_content: str, structure_formats: list[str]
):
    structure_formats_content = ""

    for fmt in structure_formats:
        structure_formats_content += f"-structure-fmt {fmt} "

    script_content = script_content.replace(
        "{{structure_formats}}", structure_formats_content
    )

    return script_content


def replace_filename_formats_in_template(script_content: str, filename: str):
    script_content = script_content.replace("{{filename}}", f"--filename {filename}")
    return script_content


# Function to generate a script name with a random suffix
def generate_script_name(base_name="pbs-script") -> str:
    """
    Generates a unique PBS script name with a uuid4 suffix.\n
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
    pbs_scripts_dir = os.path.join(settings.MEDIA_ROOT, "pbs_scripts")

    # Generate the script name with a random suffix
    script_name = generate_script_name()

    # Ensure the directory exists, otherwise create it
    os.makedirs(pbs_scripts_dir, exist_ok=True)

    # Full path to the file where the script will be saved
    script_path = os.path.join(pbs_scripts_dir, script_name)

    # Save the script to the file
    with open(script_path, "w") as file:
        file.write(script_content)

    return script_path


def get_pdf2chemicals_pbs_template_path():
    return os.path.join(
        os.path.dirname(__file__), "pbs_template", "pdf2chemicals_pbs_template.pbs"
    )


def get_pdf2chemicals_path():
    return os.path.join(
        settings.BASE_ROOT_DIR, "libs", "pdf2chemicals", "pdf2chemicals.py"
    )


def get_pbs_script_content():
    template_path = get_pdf2chemicals_pbs_template_path()

    # Load the template content
    with open(template_path, "r") as file:
        script_content = file.read()

    return script_content


def generate_pbs_script(
    pdf_path,
    output_dir,
    export_format,
    conf_formats,
    structure_formats,
    filename,
    node_name,
):
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
    script_content = replace_structure_formats_in_template(
        script_content, structure_formats
    )
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
            shell=True,
        )

        # Retorna True se grep encontrou algo, False caso contrário
        return result.returncode == 0

    except FileNotFoundError:
        print("Error: tracejob or grep not found. Check your installation.")
        return False


def get_pbs_job_status(job_id: str) -> str:
    """
    Get the status of a PBS/Torque job.

    Returns 'COMPLETED', 'FAILED', 'RUNNING', or 'QUEUED' based on job state.

    Args:
        job_id (str): Job ID to check

    Returns:
        str: Job status - 'COMPLETED', 'FAILED', 'RUNNING', or 'QUEUED'
    """
    try:
        # Step 1: Check if job has completed using existing function
        if is_pbs_job_completed(job_id):
            # Job finished - check exit status with tracejob
            result = subprocess.run(
                f"tracejob -q -n 30 {job_id} | grep 'Exit_status'",
                shell=True,
                capture_output=True,
                text=True,
            )

            # Parse exit status from tracejob output
            if result.returncode == 0 and result.stdout:
                # Extract exit status value (format: "Exit_status=<number>")
                match = re.search(r"Exit_status=(\d+)", result.stdout)
                if match:
                    exit_code = int(match.group(1))
                    return "COMPLETED" if exit_code == 0 else "FAILED"

            # Default to COMPLETED if can't parse exit status
            return "COMPLETED"

        # Step 2: Job not completed - check current state with qstat
        result = subprocess.run(
            f"qstat {job_id}", shell=True, capture_output=True, text=True
        )

        if result.returncode != 0:
            # Job not found in queue - might be completed
            return "COMPLETED"

        # Parse status from qstat output (status is in column 'S')
        lines = result.stdout.strip().split("\n")
        if len(lines) < 2:  # Header + job line
            return "RUNNING"

        # Get status character from output
        # Format: JobID  Name  User  Time  Use  S  Queue
        job_line = lines[-1]
        parts = job_line.split()
        if len(parts) < 5:  # Doesn't corresponds to the format.
            return "RUNNING"

        status_char = parts[4]  # Status column

        # Map TORQUE status codes to simplified status
        if status_char == "Q":
            return "QUEUED"

        if status_char in ["C", "E"]:
            # Should be caught by is_pbs_job_completed, but handle anyway
            return "COMPLETED"

        # R, H, T, W, S all mapped to RUNNING
        return "RUNNING"

    except FileNotFoundError:
        print("Error: qstat or tracejob not found. Check TORQUE installation.")
        return "UNKNOWN"
    except Exception as e:
        print(f"Error checking job status: {e}")
        return "UNKNOWN"
