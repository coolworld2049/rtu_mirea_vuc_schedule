import os
import pathlib
import subprocess
import time

import yaml
from dotenv import load_dotenv
from loguru import logger

load_dotenv()


def publish_package(pypi_username: str, pypi_password: str):
    subprocess.run(
        ["python", "setup.py", "sdist"],
        cwd="./rtu_mirea_vuc_schedule_client",
    )
    subprocess.run(
        [
            "twine",
            "upload",
            "dist/*",
            "--username",
            pypi_username,
            "--password",
            pypi_password,
        ],
        cwd="./rtu_mirea_vuc_schedule_client",
    )


def update_version(new_version, setup_py_path):
    setup_py_text = setup_py_path.read_text().replace(
        'VERSION = "1.0.0"',
        'VERSION = "{}"'.format(new_version),
    )
    setup_py_path.write_text(setup_py_text)
    logger.info(f"VERSION in {setup_py_path} has been updated to {new_version}")


def generate_client():
    subprocess.run(
        ["docker-compose", "-f", "docker-compose.yml", "up", "-d", "openapi-generator"],
    )


def main():
    cwd = pathlib.Path("rtu_mirea_vuc_schedule_client")
    if cwd.exists():
        raise Exception(f"Remove dir {cwd}")

    subprocess.run(["python", "extract_openapi.py"], shell=True)
    generate_client()

    time.sleep(5)
    openapi_yaml = yaml.safe_load(pathlib.Path("openapi.yaml").open("r"))
    update_version(
        new_version=openapi_yaml["info"]["version"],
        setup_py_path=cwd.joinpath("setup.py"),
    )
    publish_package(
        pypi_username=os.getenv("SCHEDULE_SERVICE_PYPI_USERNAME"),
        pypi_password=os.getenv("SCHEDULE_SERVICE_PYPI_PASSWORD"),
    )
    subprocess.run(
        ["docker-compose", "-f", "docker-compose.yml", "down", "openapi-generator"],
    )


if __name__ == "__main__":
    main()
