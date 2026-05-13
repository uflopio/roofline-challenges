import json
from pathlib import Path
import re


try:
    from simpleeval import SimpleEval
except ImportError:
    print(
        "Missing dependency: simpleeval\n"
        "Install it with:\n"
        "    pip install simpleeval\n"
        "Or from the requirements file:\n"
        "    pip install -r requirements.txt"
    )
    exit(2)


_BINARY = {
    "kib": 1024,
    "mib": 1024 ** 2,
    "gib": 1024 ** 3,
    "tib": 1024 ** 4,
}


_DECIMAL = {
    "kb": 10**3,
    "mb": 10**6,
    "gb": 10**9,
    "tb": 10**12,
}


def parse_size(value):
    if isinstance(value, (int, float)):
        return int(value)

    if not isinstance(value, str):
        raise TypeError(f"Unsupported type: {type(value)}")

    s = value.strip().lower()

    m = re.fullmatch(r"(\d+(?:\.\d+)?)\s*([a-z]*)", s)

    if not m:
        raise ValueError(f"Invalid size format: {value}")

    number = float(m.group(1))
    suffix = m.group(2)

    if suffix == "":
        return int(number)

    if suffix in _BINARY:
        return int(number * _BINARY[suffix])

    if suffix in _DECIMAL:
        return int(number * _DECIMAL[suffix])

    raise ValueError(f"Unknown suffix: {suffix}")


MAX_SIZE_BYTES = parse_size("500 Mib")
folder = Path('./challenges')


DTYPE_SIZE = {
    "f32": 4,
    "f64": 8,
    "i32": 4,
    "i64": 8,
    "i8": 1,
    "u8": 1,
}


def eval_shape(shape_expr, env):
    evaluator = SimpleEval()
    if isinstance(shape_expr, int):
        return shape_expr
    evaluator.names = env
    return int(evaluator.eval(shape_expr))


def check_max_input_size(spec) -> int:
    max_bytes = 0

    for s in spec["sizes"]:
        env = dict(s)

        total_elems = 0
        for item in spec["signature"]:
            if item["kind"] != "in":
                continue

            shape = item["shape"]

            numel = 1
            for dim in shape:
                numel *= eval_shape(dim, env)

            dtype = item["dtype"]
            size_per = DTYPE_SIZE.get(dtype, 4)

            total_elems += numel * size_per

        max_bytes = max(max_bytes, total_elems)

    return max_bytes


def check(label: str, spec: dict) -> bool:
    print(f"Processing {label}...")
    max_bytes = check_max_input_size(spec)

    if max_bytes > MAX_SIZE_BYTES:
        print(f"[ERR] Spec too large: {max_bytes / (1024**2):.2f} Mib > limit")
        return False
    else:
        print(f"[OK] Max input size: {max_bytes / (1024**2):.2f} Mib")

    return True


for dir in [p for p in folder.iterdir() if p.is_dir()]:
    spec_path = dir / 'spec.json'

    if not spec_path.exists():
        print(f"Missing spec.json for challenge in `{dir}`")
        continue

    with open(spec_path) as f:
        spec = json.load(f)

    label = dir.name

    ok = True
    try:
        ok &= check(label, spec)
    except Exception as e:
        print(f"Error while processing spec `{dir}`")
        raise e

    exit(not ok)
