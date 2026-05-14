import re
try:
    from sympy import isprime, prevprime
except ImportError:
    print(
        "Missing dependency: sympy\n"
        "Install it with:\n"
        "    pip install sympy\n"
        "Or from the requirements file:\n"
        "    pip install -r requirements.txt"
    )
    exit(2)
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
    return dtype.rstrip("*") if isinstance(dtype, str) else dtype


def build_const_env(inp: dict) -> dict:
    return dict(inp)


def eval_total_elements(shape, const_env: dict) -> int:
    if shape is None:
        return 1

    if isinstance(shape, str):
        resolved = const_env.get(shape)
        if isinstance(resolved, list):
            total = 1
            for dim in resolved:
                total *= dim
            return total
        dims = [shape]
    elif isinstance(shape, list):
        dims = shape
    else:
        return eval_shape(shape, const_env)

    missing = set()
    for dim in dims:
        if isinstance(dim, str):
            for token in re.findall(r"[A-Za-z_][A-Za-z0-9_]*", dim):
                if token not in const_env:
                    missing.add(token)
    if missing:
        raise ValueError(
            f"Shape expression references variable(s) {sorted(missing)} "
            f"not in inputs. Available names: {sorted(const_env.keys())}"
        )

    total = 1
    for dim in dims:
        total *= eval_shape(dim, const_env)
    return total


def calc_input_size(spec: dict, inp: dict) -> int:
    const_env = build_const_env(inp)
    total_bytes = 0
    for entry in spec.get("signature", []):
        kind = entry.get("kind")
        if kind not in ("in", "out", "inout"):
            continue
        dtype = normalize_dtype(entry.get("dtype", ""))
        if dtype not in DTYPE_SIZE:
            raise ValueError(
                f"Unknown dtype '{entry.get('dtype')}' in entry '{entry.get('name')}'."
            )
        element_size = DTYPE_SIZE[dtype]
        shape = entry.get("shape", None)
        num_elements = eval_total_elements(shape, const_env)
        total_bytes += num_elements * element_size
    return total_bytes


def check_max_input_size(spec: dict) -> int:
    inputs = spec.get("inputs", [])
    if not inputs:
        return 0
    return max(calc_input_size(spec, inp) for inp in inputs)


def nearest_prime(n: int) -> int:
    if n < 2:
        return 2
    if isprime(n):
        return n
    return prevprime(n)


def all_prime_values(inp: dict, const_names: set) -> bool:
    for k, v in inp.items():
        if k not in const_names:
            continue
        if isinstance(v, list):
            if not all(isprime(x) for x in v):
                return False
        elif not isprime(v):
            return False
    return True


def check_prime_test_inputs(spec: dict) -> bool:
    inputs = spec.get("inputs", [])
    if not inputs:
        return True

    INT_DTYPES = {"i8", "i16", "i32", "i64", "u8", "u16", "u32", "u64"}
    const_names = {
        entry["name"]
        for entry in spec.get("signature", [])
        if entry.get("kind") == "const"
        and normalize_dtype(entry.get("dtype", "")) in INT_DTYPES
    }

    for inp in inputs:
        relevant = {k: v for k, v in inp.items() if k in const_names}
        if not relevant:
            continue
        if all_prime_values(inp, const_names) and calc_input_size(spec, inp) <= MAX_SIZE_BYTES:
            return True

    example = inputs[-1]
    relevant_example = {k: v for k, v in example.items() if k in const_names}
    non_prime = {}
    for k, v in relevant_example.items():
        if isinstance(v, list):
            if not all(isprime(x) for x in v):
                non_prime[k] = v
        elif not isprime(v):
            non_prime[k] = v
    suggestions = {}
    for k, v in non_prime.items():
        if isinstance(v, list):
            suggestions[k] = [nearest_prime(x) for x in v]
        else:
            suggestions[k] = nearest_prime(v)

    print(
        f" ERR  No input configuration has all-prime const values.\n"
        f"      Non-prime values in last config: {non_prime}\n"
        f"      Suggested prime replacements:    {suggestions}"
    )
    return False


def check(label: str, spec: dict) -> bool:
    print(f"Processing {label}...")
    ok = True

    max_bytes = check_max_input_size(spec)
    if max_bytes > MAX_SIZE_BYTES:
        diff_bytes = max_bytes - MAX_SIZE_BYTES
        print(
            f" ERR  Spec too large: "
            f"{format_bytes(max_bytes)} > {format_bytes(MAX_SIZE_BYTES)} "
            f"(excess: {format_bytes(diff_bytes)})"
        )
        ok = False
    else:
        print(f"  OK  size: {format_bytes(max_bytes)}")

    if not check_prime_test_inputs(spec):
        ok = False
    elif ok:
        print(f"  OK  prime-input check passed")

    return ok


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
