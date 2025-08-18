import subprocess

def open_file(file_path: str):
    subprocess.run(['xdg-open', file_path])
