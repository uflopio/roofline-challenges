import os
import json
from pathlib import Path


MAX_SIZE_BYTES = 500 * 1024 * 1024


folder = Path('./challenges')


def max_size(spec: dict) -> int:
    ...


def check(spec: dict) -> bool:
    return True


for dir in [p for p in folder.iterdir() if p.is_dir()]:
    spec = dir / 'spec.json'

    if not spec.exists():
        print(f"Missing spec.json for challenge  in `{dir}`")
        continue
    
    with open(spec) as f:
        spec = json.load(f)

    ok = True
    try:
        ok &= check(spec)
    except Exception as e:
        print(f"Error while processing spec `{spec}`")
        raise e

    exit(not ok)
