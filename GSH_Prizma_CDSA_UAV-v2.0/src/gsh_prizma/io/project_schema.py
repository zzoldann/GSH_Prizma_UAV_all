import json
from dataclasses import dataclass, asdict
from pathlib import Path

@dataclass
class Project:
    schema: str = "1.0"
    name: str = "Untitled"
    link: dict = None
    antenna: dict = None

def save_project(prj: Project, path: str):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    d = asdict(prj)
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")

def load_project(path: str) -> Project:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return Project(**data)
