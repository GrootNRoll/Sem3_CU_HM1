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


class VirtualShell:
    def __init__(self, vfs, log_file_path):
        self.vfs = vfs
        self.log_file_path = log_file_path

    def start(self):
        while True:
            command = input(f"{self.vfs.current_path()} # ")
            if command.strip() == "exit":
                break
            self.process_command(command)

    def process_command(self, command):
        parts = command.split()
        if not parts:
            return
        cmd = parts[0]

        # Логируем команду
        self.log_action(command)

        try:
            if cmd == "ls":
                print("\n".join(self.vfs.list_dir()))
            elif cmd == "pwd":
                print(self.vfs.current_path())
            elif cmd == "cd":
                if len(parts) > 1:
                    self.vfs.change_dir(parts[1])
                else:
                    print("Usage: cd <directory>")
            elif cmd == "wc":
                self.handle_wc(parts)
            elif cmd == "touch":
                self.handle_touch(parts)
            else:
                print(f"Command not found: {cmd}")
        except FileNotFoundError as e:
            print(str(e))
        except Exception as e:
            print(f"Error: {e}")

    def handle_wc(self, parts):
        """Обрабатывает команду wc (word count)."""
        if len(parts) < 2:
            print("Usage: wc <file>")
            return

        file_name = parts[1]

        try:
            file_content = self.vfs.read_file(file_name)
            num_lines = len(file_content)
            num_words = sum(len(line.split()) for line in file_content)
            num_chars = sum(len(line) for line in file_content)

            print(f"{num_lines} {num_words} {num_chars} {file_name}")
        except FileNotFoundError as e:
            print(str(e))

    def handle_touch(self, parts):
        """Обрабатывает команду touch (создаёт пустой файл и добавляет его в архив)."""
        if len(parts) < 2:
            print("Usage: touch <file>")
            return

        file_name = parts[1]

        # Пытаемся создать новый пустой файл
        try:
            full_path = f"{self.vfs.current_path().strip('/')}/{file_name}".strip("/")
            if full_path in self.vfs.files_content:
                print(f"File {file_name} already exists.")
            else:
                # Создаем пустой файл в виртуальной файловой системе
                self.vfs.files_content[full_path] = ""  # Создаем пустой файл
                # Для имитации создания файла в виртуальной файловой системе
                dirs = self.vfs.fs
                parts = full_path.split('/')
                for part in parts[:-1]:
                    dirs = dirs.setdefault(part, {})
                dirs[parts[-1]] = None  # Добавляем файл в виртуальную файловую систему
                print(f"File {file_name} created in virtual file system.")

                # Добавляем файл в .tar архив
                self.add_file_to_tar(file_name)
                print(f"File {file_name} added to the archive.")

        except Exception as e:
            print(f"Error: {e}")




if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <path_to_tar> <path_to_log_file>")
        sys.exit(1)

    tar_file_path = sys.argv[1]
    log_file_path = sys.argv[2]

    vfs = VirtualFileSystem(tar_file_path)
    shell = VirtualShell(vfs, log_file_path)

    shell.start()
