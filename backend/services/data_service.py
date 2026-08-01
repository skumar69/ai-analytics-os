from pathlib import Path


def get_uploaded_files(upload_dir: str) -> list[str]:
    directory = Path(upload_dir)
    if not directory.exists():
        return []
    return sorted(str(path.name) for path in directory.iterdir() if path.is_file())
