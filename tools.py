from typing import List

def read_file(path: str) -> str :
    with open(path, "r") as f:
        return f.read()
    
def list_files(path: str = ".") -> List[str]:
    import os
    return os.listdir(path)

TOOLS = {
    "read_file": read_file,
    "list_files": list_files
}