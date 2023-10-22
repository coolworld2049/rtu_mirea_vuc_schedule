import argparse
import json
import pathlib
import subprocess
import sys

import toml
import yaml
from fastapi import FastAPI
from loguru import logger
from uvicorn.importer import import_from_string

parser = argparse.ArgumentParser(prog="extract_openapi.py")
parser.add_argument(
    "--app",
    help='App import string. Eg. "main:app"',
    default="src.web.application:get_app",
)
parser.add_argument(
    "--app-dir",
    help="Directory containing the app",
    default="schedule_service",
)
parser.add_argument(
    "--out",
    help="Output file ending in .json or .yaml",
    default="openapi.yaml",
)

if __name__ == "__main__":
    args = parser.parse_args()

    _toml = toml.loads(
        pathlib.Path("../../pyproject.toml").read_text(encoding="utf-8")
    )

    if args.app_dir is not None:
        logger.info(f"adding {args.app_dir} to sys.path")
        sys.path.insert(0, args.app_dir)

    logger.info(f"importing app from {args.app}")
    app: FastAPI = import_from_string(args.app)()
    app.version = _toml["tool"]["poetry"]["version"]
    openapi = app.openapi()

    logger.info(f"writing openapi spec v{app.version}")
    with open(args.out, "w") as f:
        if args.out.endswith(".json"):
            json.dump(openapi, f, indent=2)
        else:
            yaml.dump(openapi, f, sort_keys=False)

    logger.info(f"spec written to {args.out}")
    subprocess.run(["git", "add", "openapi.yaml"], shell=True)
