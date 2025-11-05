import os

def get_file_path(file: str) -> str:
    """Retorna o caminho absoluto de um arquivo."""
    base_dir: str = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_dir, file)
