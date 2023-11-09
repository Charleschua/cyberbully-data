from pathlib import Path

from cyberbully.config_schemas.config_schema import Config
from cyberbully.utils.config_utils import get_config
from cyberbully.utils.data_utils import initialize_dvc
from cyberbully.utils.utils import get_logger


@get_config(config_path="../configs", config_name="config")
def version_data(config: Config) -> None:
    # logger = get_logger(Path(__file__).name)
    # logger.info()
    
    initialize_dvc()


if __name__ == "__main__":
    version_data()  # type: ignore
