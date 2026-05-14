from utils import extract_frontmatter, parse_size, eval_shape, format_bytes
from utils import folder

MAX_SIZE_BYTES = parse_size("512 Mib")

DTYPE_SIZE = {
    "f32": 4,
    "f64": 8,
    "i32": 4,
    "i64": 8,
    "i8": 1,
    "u8": 1,
    "u32": 4,
    "u64": 8,
    "u16": 2,
    "i16": 2,
    "f16": 2,
    "bf16": 2,
    "bool": 1,
}


def normalize_dtype(dtype: str) -> str:
    """Strip pointer suffix (*) from dtype strings like 'f32*' -> 'f32'."""
    return dtype.rstrip("*") if isinstance(dtype, str) else dtype


def eval_total_elements(shape, const_env: dict) -> int:
    """
    Evaluate total number of elements from a shape spec.

    Shape can be:
      - An int literal                  -> that value
      - A string expression             -> evaluated against const_env
      - A list of int/string dimensions -> product of each dimension
      - Missing (None / 1)              -> 1  (scalar)
    """
    if shape is None:
        return 1
    if isinstance(shape, list):
        total = 1
        for dim in shape:
            total *= eval_shape(dim, const_env)
        return total
    # scalar int or expression string
    return eval_shape(shape, const_env)


def check_max_input_size(spec: dict) -> int:
    signature = spec.get("signature", [])

    const_env: dict = {}
    for entry in signature:
        if entry.get("kind") != "const":
            continue
        name = entry["name"]
        values = entry.get("values", [])
        if values:
            evaluated = [eval_shape(v, const_env) for v in values]
            const_env[name] = max(evaluated)

    inputs = spec.get("inputs", [])
    if inputs:

        input_env: dict = {}
        for inp in inputs:
            for k, v in inp.items():
                if k not in input_env or v > input_env[k]:
                    input_env[k] = v
        for k, v in input_env.items():
            if k not in const_env:
                const_env[k] = v

    total_bytes = 0
    for entry in signature:
        kind = entry.get("kind")
        if kind not in ("in", "out", "inout"):
            continue

        raw_dtype = entry.get("dtype", "")
        dtype = normalize_dtype(raw_dtype)

        if dtype not in DTYPE_SIZE:
            raise ValueError(
                f"Unknown dtype '{raw_dtype}' (normalized: '{dtype}') "
                f"in entry '{entry.get('name')}'. "
                f"Add it to DTYPE_SIZE if intentional."
            )

        element_size = DTYPE_SIZE[dtype]
        shape = entry.get("shape", None)
        num_elements = eval_total_elements(shape, const_env)
        total_bytes += num_elements * element_size

    return total_bytes


def check(label: str, spec: dict) -> bool:
    print(f"Processing {label}...")
    max_bytes = check_max_input_size(spec)
    if max_bytes > MAX_SIZE_BYTES:
        diff_bytes = max_bytes - MAX_SIZE_BYTES
        print(
            f"  ERR too large: "
            f"{format_bytes(max_bytes)} > {format_bytes(MAX_SIZE_BYTES)} "
            f"(excess: {format_bytes(diff_bytes)})"
        )
        return False
    print(f"  OK  size: {format_bytes(max_bytes)}")
    return True


if __name__ == '__main__':
    ok = True
    for dir in [p for p in folder.iterdir() if p.is_dir()]:
        readme_md = dir / 'README.md'
        if not readme_md.exists():
            continue
        with open(readme_md) as f:
            frontmatter = extract_frontmatter(f.read())
        if frontmatter is None:
            print(f"No frontmatter in {readme_md}")
            ok = False
            continue
        spec = frontmatter['spec']
        label = dir.name
        try:
            ok &= check(label, spec)
        except Exception as e:
            print(f"Error while processing spec `{dir}`")
            raise e
    exit(not ok)
