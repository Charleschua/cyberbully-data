from pathlib import Path
from subprocess import CalledProcessError

from cyberbully.utils.utils import get_logger, run_shell_command

DATA_UTILS_LOGGER = get_logger(Path(__file__).name)


def is_dvc_initialized() -> bool:
    return (Path().cwd() / ".dvc").exists()


def initialize_dvc() -> None:
    if is_dvc_initialized():
        DATA_UTILS_LOGGER.info("DVC is already initialized")
        return

    DATA_UTILS_LOGGER.info("Initializing DVC")
    run_shell_command("dvc init")
    run_shell_command("dvc config core.analytics false")
    run_shell_command("dvc config core.autostage true")
    run_shell_command("git add .dvc")
    run_shell_command("git commit -nm 'Initialized DVC'")


def initialize_dvc_storage(dvc_remote_name: str, dvc_remote_url: str) -> None:
    if not run_shell_command("dvc remote list"):
        DATA_UTILS_LOGGER.info("Initializing DVC storage...")
        run_shell_command(f"dvc remote add -d {dvc_remote_name} {dvc_remote_url}")
        run_shell_command("git add .dvc/config")
        run_shell_command(f"git commit -nm 'Configured remote storage at: {dvc_remote_url}'")
    else:
        DATA_UTILS_LOGGER.info("DVC storage was already initialized...")


def commit_to_dvc(dvc_raw_data_folder: str, dvc_remote_name: str) -> None:
    current_version = run_shell_command("git tag --list | sort -t v -k 2 -g | tail -1 | sed 's/v//'").strip()
    if not current_version:
        current_version = "0"
    next_version = f"v{int(current_version)+1}"
    run_shell_command(f"dvc add {dvc_raw_data_folder}")
    print("5")
    run_shell_command("git add .")
    print("6")
    run_shell_command(f"git commit -nm 'Updated version of the data from v{current_version} to {next_version}'")
    print("7")
    run_shell_command(f"git tag -a {next_version} -m 'Data version {next_version}'")
    print("1")
    run_shell_command(f"dvc push {dvc_raw_data_folder}.dvc --remote {dvc_remote_name}")
    print("2")
    run_shell_command("git push --follow-tags")
    print("3")
    run_shell_command("git push -f --tags")
    print("4")


def make_new_data_version(dvc_raw_data_folder: str, dvc_remote_name: str) -> None:
    try:
        status = run_shell_command(f"dvc status {dvc_raw_data_folder}.dvc")
        print("8")
        if status == "Data and pipelines are up to date.\n":
            DATA_UTILS_LOGGER.info("Data and pipelines are up to date.")
            print("11")
            return
        print("9")
        commit_to_dvc(dvc_raw_data_folder, dvc_remote_name)
        print("10")
    except CalledProcessError:
        commit_to_dvc(dvc_raw_data_folder, dvc_remote_name)
