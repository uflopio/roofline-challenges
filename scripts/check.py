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
}


def check_max_input_size(spec: dict) -> int:
    signature = spec.get("signature", [])
    const_env = {}

    for entry in signature:
        if entry.get("kind") != "const":
            continue

        name = entry["name"]
        values = entry.get("values", [])

        evaluated = [
            eval_shape(v, const_env)
            for v in values
        ]

        const_env[name] = max(evaluated)

    total_bytes = 0

    for entry in signature:
        kind = entry.get("kind")

        if kind not in ("in", "out", "inout"):
            continue

        dtype = entry["dtype"]
        shape = entry.get("shape", 1)

        if dtype not in DTYPE_SIZE:
            raise ValueError(f"Unknown dtype: {dtype}")

        element_size = DTYPE_SIZE[dtype]

        num_elements = eval_shape(shape, const_env)

        total_bytes += num_elements * element_size

    return total_bytes


def check(label: str, spec: dict) -> bool:
    print(f"Processing {label}...")
    max_bytes = check_max_input_size(spec)

    if max_bytes > MAX_SIZE_BYTES:
        diff_bytes = max_bytes - MAX_SIZE_BYTES

        print(
            f"[ERR] Spec too large: "
            f"{format_bytes(max_bytes)} > {format_bytes(MAX_SIZE_BYTES)} "
            f"(excess: {format_bytes(diff_bytes)})"
        )
        return False

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
