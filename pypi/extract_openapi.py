import argparse
import json
import subprocess
import sys

import yaml
from fastapi import FastAPI
from loguru import logger
from uvicorn.importer import import_from_string

parser = argparse.ArgumentParser(prog="extract_openapi.py")
parser.add_argument(
    "--app",
    help='App import string. Eg. "main:app"',
    default="schedule_service.web.application:get_app",
)
parser.add_argument(
    "--app-dir",
    help="Directory containing the app",
    default="..",
)
parser.add_argument(
    "--out",
    help="Output file ending in .json or .yaml",
    default="openapi.yaml",
)

args = parser.parse_args()

if args.app_dir is not None:
    logger.info(f"adding {args.app_dir} to sys.path")
    sys.path.insert(0, args.app_dir)

logger.info(f"importing app from {args.app}")
app: FastAPI = import_from_string(args.app)()
openapi = app.openapi()

logger.info(f"writing openapi spec v{openapi['info']['version']}")
with open(args.out, "w") as f:
    if args.out.endswith(".json"):
        json.dump(openapi, f, indent=2)
    else:
        yaml.dump(openapi, f, sort_keys=False)

logger.info(f"spec written to {args.out}")
subprocess.run(["git", "add", args.out], shell=True)
logger.info(f"file added to repo")
