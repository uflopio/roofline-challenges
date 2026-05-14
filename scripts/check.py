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
    """Strip pointer suffix (*) from dtype strings like 'f32*' -> 'f32'."""
    return dtype.rstrip("*") if isinstance(dtype, str) else dtype


def eval_total_elements(shape, const_env: dict) -> int:
    if shape is None:
        return 1

    dims = shape if isinstance(shape, list) else [shape]

    missing = set()
    for dim in dims:
        if isinstance(dim, str):
            # Extract bare identifiers (variable names) from the expression.
            for token in re.findall(r"[A-Za-z_][A-Za-z0-9_]*", dim):
                if token not in const_env:
                    missing.add(token)
    if missing:
        raise ValueError(
            f"Shape expression references variable(s) {sorted(missing)} "
            f"that are not defined in any 'const' entry's 'values' list "
            f"or in the spec's 'inputs' configurations. "
            f"Available names: {sorted(const_env.keys())}"
        )

    if isinstance(shape, list):
        total = 1
        for dim in dims:
            total *= eval_shape(dim, const_env)
        return total

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


def nearest_prime(n: int) -> int:
    if n < 2:
        return 2
    if isprime(n):
        return n
    return prevprime(n)


def check_prime_test_inputs(spec: dict) -> bool:
    """
    Verify that at least one input configuration has every const value set to
    a prime number, so the total element count is a product of primes and is
    guaranteed not to be a power of two.

    Returns True if satisfied, False with a printed diagnostic otherwise.
    """
    inputs = spec.get("inputs", [])
    if not inputs:
        return True

    # Only integer-typed const params are meaningful dimension values.
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
        if all(isprime(v) for v in relevant.values()):
            return True  # Found a qualifying configuration.

    # No qualifying configuration — build a helpful suggestion from the first
    # input config: replace each non-prime value with its nearest prime.
    example = inputs[0]
    relevant_example = {k: v for k, v in example.items() if k in const_names}
    non_prime = {k: v for k, v in relevant_example.items() if not isprime(v)}
    suggestions = {k: nearest_prime(v) for k, v in non_prime.items()}

    print(
        f" ERR  No input configuration has all-prime const values.\n"
        f"      Non-prime values in first config: {non_prime}\n"
        f"      Suggested prime replacements:     {suggestions}"
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
