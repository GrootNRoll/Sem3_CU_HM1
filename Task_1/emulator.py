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
