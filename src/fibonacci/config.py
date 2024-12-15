from typing import Literal

class Config:
    backend: Literal["py", "rs", "cpp"] = "py"


config = Config()
