import re
from pathlib import Path

try:
    from simpleeval import SimpleEval
    import yaml
except ImportError:
    print(
        "Missing dependency: simpleeval numpy yaml\n"
        "Install it with:\n"
        "    pip install simpleeval numpy yaml\n"
        "Or from the requirements file:\n"
        "    pip install -r requirements.txt"
    )
    exit(2)


folder = Path('./challenges')


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


def eval_shape(shape_expr, env):
    evaluator = SimpleEval()
    if isinstance(shape_expr, int):
        return shape_expr
    evaluator.names = env
    return int(evaluator.eval(shape_expr))


def format_bytes(num_bytes: int, precision: int = 2) -> str:
    abs_bytes = abs(num_bytes)

    for unit, factor in reversed(_BINARY.items()):
        if abs_bytes >= factor:
            value = num_bytes / factor
            return f"{value:.{precision}f} {unit}"

    return f"{num_bytes} B"


def extract_frontmatter(content: str) -> dict | None:
    if not content.startswith("---"):
        return None

    parts = content.split("---", 2)

    if len(parts) < 3:
        return None

    frontmatter = parts[1]

    return yaml.safe_load(frontmatter)


def generate_cuda_snippet(spec: dict) -> str:
    dtype_map = {
        "f32": "float",
        "f64": "double",
        "i32": "int",
        "i64": "long long",
        "u32": "unsigned int",
        "u64": "unsigned long long",
    }

    sig = spec.get("signature", [])

    def cpp_type(entry):
        dt = dtype_map.get(entry["dtype"], entry["dtype"])

        shape = entry.get("shape", None)
        if shape:
            return f"const {dt}*" if entry["kind"] == "in" else f"{dt}*"
        return dt

    kind_order = {"in": 0, "inout": 1, "out": 2, "const": 3}
    sig_sorted = sorted(sig, key=lambda x: kind_order.get(x["kind"], 99))

    args = []

    for entry in sig_sorted:
        name = entry["name"]
        kind = entry["kind"]
        ctype = cpp_type(entry)

        if kind == "const" and not entry.get("shape"):
            args.append(f"{ctype} {name}")
        else:
            args.append(f"{ctype} {name}")

    args_str = ", ".join(args)

    return f"""#include <cuda_runtime.h>

void solve({args_str}) {{
  // Solution goes here.
  // Keep in mind: the pointers are on the GPU!
}}
"""


if __name__ == '__main__':
    print("This script is not intended for running!")
    print("It only containers helper functions for other scripts")
    exit(-2)
