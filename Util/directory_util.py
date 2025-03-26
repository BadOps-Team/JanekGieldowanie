import os
import pathlib
from functools import wraps

def use_absolute_path(func):
    @wraps(func)
    def wrapper(path: pathlib.Path, *args, **kwargs):
        absolute_path = path.resolve() if not path.is_absolute() else path
        return func(absolute_path, *args, **kwargs)
    return wrapper

class DirectoryUtil:
    @staticmethod
    @use_absolute_path
    def directory_exists(path: pathlib.Path, directory: str, create: bool) -> bool|None:
        target_dir = path / directory
        if target_dir.exists() and target_dir.is_dir():
            return True
        
        if not create:
            return False
        
        try:
            target_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f'Error creating directory: {e}')
        finally:
            return None