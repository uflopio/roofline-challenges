import sys
import copy
import importlib.util
import random
from pathlib import Path

import numpy as np
try:
    from simpleeval import SimpleEval
    import yaml
except ImportError:
    print(
        "Missing dependency: simpleeval yaml\n"
        "Install with:\n"
        "    pip install simpleeval pyyaml"
    )
    exit(2)

from utils import extract_frontmatter, folder

DTYPE_NUMPY = {
    "f32": np.float32,
    "f64": np.float64,
    "i8":  np.int8,
    "i16": np.int16,
    "i32": np.int32,
    "i64": np.int64,
    "u8":  np.uint8,
    "u16": np.uint16,
    "u32": np.uint32,
    "u64": np.uint64,
    "bool": np.bool_,
}


def normalize_dtype(dtype: str) -> str:
    return dtype.rstrip("*") if isinstance(dtype, str) else dtype


def eval_expr(expr, env: dict):
    ev = SimpleEval()
    ev.names = {k: v for k, v in env.items() if isinstance(v, (int, float))}
    ev.functions = {}
    return ev.eval(str(expr))


def resolve_shape(shape, const_env: dict):
    if shape is None:
        return None
    if isinstance(shape, int):
        return shape
    if isinstance(shape, str):
        resolved = const_env.get(shape)
        if isinstance(resolved, list):
            return [int(x) for x in resolved]
        return int(eval_expr(shape, const_env))
    if isinstance(shape, list):
        result = []
        for dim in shape:
            if isinstance(dim, int):
                result.append(dim)
            else:
                result.append(int(eval_expr(dim, const_env)))
        return result
    return shape


def parse_init(init_str: str, dtype_str: str, shape, const_env: dict):
    init_str = init_str.strip()

    if init_str.startswith("uniform("):
        inner = init_str[len("uniform("):-1]
        parts = inner.split(",")
        lo = eval_expr(parts[0].strip(), const_env)
        hi = eval_expr(parts[1].strip(), const_env)
        return sample_uniform(lo, hi, dtype_str, shape)

    raise ValueError(f"Unsupported init expression: {init_str!r}")


def sample_uniform(lo, hi, dtype_str: str, shape):
    dtype = DTYPE_NUMPY.get(dtype_str)
    if dtype is None:
        raise ValueError(f"Unknown dtype: {dtype_str!r}")

    if shape is None:
        num_elements = 1
        scalar = True
    elif isinstance(shape, int):
        num_elements = shape
        scalar = False
    elif isinstance(shape, list):
        num_elements = 1
        for d in shape:
            num_elements *= d
        scalar = False
    else:
        raise ValueError(f"Unexpected shape: {shape!r}")

    if np.issubdtype(dtype, np.integer):
        arr = np.random.randint(int(lo), int(hi) + 1, size=num_elements, dtype=dtype)
    elif np.issubdtype(dtype, np.floating):
        arr = (np.random.random(num_elements) * (hi - lo) + lo).astype(dtype)
    elif dtype == np.bool_:
        arr = np.random.randint(0, 2, size=num_elements, dtype=np.uint8).astype(np.bool_)
    else:
        raise ValueError(f"Unsupported dtype for sampling: {dtype_str!r}")

    if scalar:
        return arr[0].item()
    if isinstance(shape, list):
        return arr.reshape(shape).tolist()
    return arr.tolist()


def build_const_env(inp: dict) -> dict:
    return dict(inp)


def generate_inputs(spec: dict, inp: dict) -> dict:
    const_env = build_const_env(inp)
    result = {}

    for entry in spec.get("signature", []):
        name = entry["name"]
        kind = entry.get("kind")

        if kind == "const":
            val = inp.get(name)
            if val is not None:
                result[name] = val
            continue

        if kind not in ("in", "inout"):
            continue

        if name in inp:
            result[name] = inp[name]
            continue

        dtype_str = normalize_dtype(entry.get("dtype", ""))
        shape = resolve_shape(entry.get("shape"), const_env)
        init = entry.get("init")

        if init is None:
            raise ValueError(f"Entry '{name}' has no init and no value in input config.")

        result[name] = parse_init(init, dtype_str, shape, const_env)

    return result


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location("challenge", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_solve(mod, spec: dict, generated: dict):
    kwargs = dict(generated)

    out_names = [
        entry["name"]
        for entry in spec.get("signature", [])
        if entry.get("kind") == "out"
    ]
    inout_names = [
        entry["name"]
        for entry in spec.get("signature", [])
        if entry.get("kind") == "inout"
    ]

    result = mod.solve(**kwargs)

    outputs = {}

    if result is not None:
        if isinstance(result, dict):
            outputs.update(result)
        elif len(out_names) == 1:
            outputs[out_names[0]] = result
        else:
            raise ValueError(f"solve() returned a non-dict but multiple outputs exist: {out_names}")

    for name in inout_names:
        val = kwargs[name]
        outputs[name] = val.tolist() if isinstance(val, np.ndarray) else val

    return outputs


def to_npz(d: dict) -> dict:
    result = {}
    for k, v in d.items():
        if isinstance(v, np.ndarray):
            result[k] = v
        elif isinstance(v, list):
            result[k] = np.array(v)
        elif isinstance(v, bool):
            result[k] = np.array(v, dtype=np.bool_)
        elif isinstance(v, int):
            result[k] = np.array(v, dtype=np.int64)
        elif isinstance(v, float):
            result[k] = np.array(v, dtype=np.float64)
        else:
            result[k] = np.array(v)
    return result


def process_challenge(challenge_dir: Path, num_pairs: int):
    readme = challenge_dir / "README.md"
    a_py = challenge_dir / "challenge.py"

    if not readme.exists():
        return
    if not a_py.exists():
        print(f"[SKIP] {challenge_dir.name}: no challenge.py")
        return

    with open(readme) as f:
        frontmatter = extract_frontmatter(f.read())
    if frontmatter is None:
        print(f"[SKIP] {challenge_dir.name}: no frontmatter")
        return

    spec = frontmatter["spec"]
    inputs_list = spec.get("inputs", [])
    if not inputs_list:
        print(f"[SKIP] {challenge_dir.name}: no inputs in spec")
        return

    pairs_dir = challenge_dir / "tests"

    existing = sorted([p for p in pairs_dir.glob("*/input.npz")]) if pairs_dir.exists() else []
    if len(existing) >= num_pairs:
        print(f"[SKIPPED] {challenge_dir.name}: {len(existing)} pairs already exist")
        return

    mod = load_module(a_py)
    has_generate = hasattr(mod, "generate")

    pairs_dir.mkdir(exist_ok=True)
    start = len(existing)

    for i in range(start, num_pairs):
        inp = inputs_list[i % len(inputs_list)]
        pair_dir = pairs_dir / f"{i:03d}"
        pair_dir.mkdir(exist_ok=True)

        if has_generate:
            consts = {k: v for k, v in inp.items()}
            generated = mod.generate(**consts)
        else:
            generated = generate_inputs(spec, inp)

        outputs = run_solve(mod, spec, generated)

        np.savez(pair_dir / "input.npz", **to_npz(generated))
        np.savez(pair_dir / "output.npz", **to_npz(outputs))

        print(f"[GEN]  {challenge_dir.name}: pair {i:03d}")

    print(f"[DONE] {challenge_dir.name}: {num_pairs} pairs ready")


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <num_pairs>")
        exit(1)
    try:
        num_pairs = int(sys.argv[1])
    except ValueError:
        print(f"Error: num_pairs must be an integer, got {sys.argv[1]!r}")
        exit(1)

    for challenge_dir in sorted(p for p in folder.iterdir() if p.is_dir()):
        try:
            process_challenge(challenge_dir, num_pairs)
        except Exception as e:
            print(f"[ERR]  {challenge_dir.name}: {e}")
            raise


if __name__ == "__main__":
    main()
