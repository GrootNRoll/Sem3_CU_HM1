import os
import sys
import json
import tarfile
import io
from datetime import datetime

class VirtualFileSystem:
    def __init__(self, tar_file_path):
        self.tar_file_path = tar_file_path
        self.current_dir = "/"
        self.fs = {}
        self.files_content = {}
        self.load_tar()

    def load_tar(self):
        """Загружает файловую систему из tar-архива."""
        with tarfile.open(self.tar_file_path, 'r') as t:
            for member in t.getmembers():
                # Разбираем путь файла, чтобы создать иерархию каталогов
                if member.isdir():
                    parts = member.name.split('/')
                    d = self.fs
                    for part in parts[:-1]:
                        d = d.setdefault(part, {})
                    d[parts[-1]] = {}  # Папка
                elif member.isfile():
                    parts = member.name.split('/')
                    d = self.fs
                    for part in parts[:-1]:
                        d = d.setdefault(part, {})
                    d[parts[-1]] = None  # Файл
                    self.files_content[member.name] = t.extractfile(member).read().decode('utf-8')

    def list_dir(self):
        """Возвращает отсортированное содержимое текущего каталога с папками первыми."""
        dirs = self.fs
        for part in self.current_dir.strip("/").split("/"):
            if part:
                dirs = dirs[part]
        # Разделяем на папки и файлы
        folders = sorted([name for name in dirs.keys() if isinstance(dirs[name], dict)])
        files = sorted([name for name in dirs.keys() if dirs[name] is None])
        return folders + files

    def change_dir(self, path):
        """Сменить каталог."""
        if path == "..":
            self.current_dir = "/".join(self.current_dir.split("/")[:-1])
            if not self.current_dir:
                self.current_dir = "/"
        elif path in self.list_dir():
            self.current_dir += f"/{path}".strip("/")
        else:
            raise FileNotFoundError(f"No such directory: {path}")

    def current_path(self):
        """Возвращает текущий путь."""
        return self.current_dir

    def read_file(self, file_path):
        """Читает содержимое файла."""
        full_path = f"{self.current_dir.strip('/')}/{file_path}".strip("/")
        if full_path in self.files_content:
            return self.files_content[full_path].splitlines()
        raise FileNotFoundError(f"No such file: {file_path}")
