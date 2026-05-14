from utils import extract_frontmatter, generate_cuda_snippet, folder


if __name__ == '__main__':
    for dir_path in [p for p in folder.iterdir() if p.is_dir()]:
        readme_md = dir_path / "README.md"

        if not readme_md.exists():
            continue

        with open(readme_md, "r", encoding="utf-8") as f:
            frontmatter = extract_frontmatter(f.read())

        if frontmatter is None:
            print(f"[WARN] No frontmatter in {readme_md}")
            continue

        spec = frontmatter.get("spec")
        if spec is None:
            print(f"[WARN] No spec in {readme_md}")
            continue

        label = dir_path.name

        try:
            (dir_path / "templates").mkdir(parents=True, exist_ok=True)
            output_file = dir_path / "templates" / "cuda.cu"

            cuda_code = generate_cuda_snippet(spec)

            output_file.write_text(cuda_code, encoding="utf-8")

            print(f"[OK] Generated {output_file}")

        except Exception as e:
            print(f"[ERROR] Failed processing {dir_path}: {e}")
            raise
