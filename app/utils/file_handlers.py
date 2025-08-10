from pathlib import Path
from typing import Union
from fastapi import HTTPException
import os

def cleanup_file(file_path: Union[str, Path]):
    try:
        if isinstance(file_path, str):
            file_path = Path(file_path)
        if file_path.exists():
            os.unlink(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File cleanup failed: {str(e)}")