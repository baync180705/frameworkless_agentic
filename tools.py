from typing import List

def read_file(path: str) -> str :
    with open(path, "r") as f:
        return f.read()
    
def list_files(path: str = ".") -> List[str]:
    import os
    return os.listdir(path)

def write_file(path: str, content: str) -> str:
    with open(path, "w") as f:
        f.write(content)
    return f"Wrote {len(content)} characters to {path}"

def append_file(path: str, content: str) -> str:
    with open(path, "a") as f:
        f.write(content)
    return f"Appended to {path}"

def file_exists(path: str) -> bool:
    import os
    return os.path.exists(path)

def get_current_time() -> str:
    from datetime import datetime
    return datetime.now().isoformat()

def fetch_url(url: str) -> str:
    import requests
    return requests.get(url, timeout=10).text[:5000]

def remember(note: str) -> str:
    with open("memory.txt", "a") as f:
        f.write(note + "\n")
    return "Saved to memory"

def ask_user(question: str) -> str:
    return question

TOOLS = {
    "read_file": read_file,
    "list_files": list_files,
    "write_file": write_file,
    "append_file": append_file,
    "file_exists": file_exists,
    "get_current_time": get_current_time,
    "fetch_url": fetch_url,
    "remember": remember,
    "ask_user": ask_user
}