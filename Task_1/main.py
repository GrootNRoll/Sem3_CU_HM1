import json
from emulator import VirtualFileSystem, VirtualShell
import unittest
from unittest.mock import patch
from io import StringIO
import os
import json
#tmp


class TestVirtualShell(unittest.TestCase):
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_ls(self, mock_stdout):
        if TEST_MODE:
            # Тест для команды ls
            vfs = VirtualFileSystem("test.tar")
            shell = VirtualShell(vfs, "test_log.json")
            shell.vfs.fs = {'folder': {}, 'file1.txt': None, 'file2.txt': None}
            shell.vfs.current_dir = "/"
            shell.process_command("ls")
            
            # Проверяем, что вывод соответствует ожидаемому
            self.assertIn('folder', mock_stdout.getvalue())
            self.assertIn('file1.txt', mock_stdout.getvalue())
            self.assertIn('file2.txt', mock_stdout.getvalue())
        
        print("Test for 'ls' passed successfully")

    @patch('sys.stdout', new_callable=StringIO)
    def test_ls_empty(self, mock_stdout):
        if TEST_MODE:
            # Тест для команды ls, когда каталог пуст
            vfs = VirtualFileSystem("test.tar")
            shell = VirtualShell(vfs, "test_log.json")
            shell.vfs.fs = {}
            shell.vfs.current_dir = "/"
            shell.process_command("ls")
            
            # Проверяем, что каталог пуст
            self.assertEqual(mock_stdout.getvalue().strip(), "")
        
        print("Test for 'ls' with empty directory passed successfully")
    
    @patch('sys.stdout', new_callable=StringIO)  
    def test_pwd(self, mock_stdout):
        if TEST_MODE:
            # Тест для команды pwd
            vfs = VirtualFileSystem("test.tar")
            shell = VirtualShell(vfs, "test_log.json")
            shell.vfs.current_dir = "/home/user"
            shell.process_command("pwd")
            
            # Проверяем, что вывод соответствует текущему пути
            self.assertEqual(mock_stdout.getvalue().strip(), '/home/user')
        
        print("Test for 'pwd' passed successfully")

    @patch('sys.stdout', new_callable=StringIO)  
    def test_pwd_root(self, mock_stdout):
        if TEST_MODE:
            # Тест для команды pwd в корне
            vfs = VirtualFileSystem("test.tar")
            shell = VirtualShell(vfs, "test_log.json")
            shell.vfs.current_dir = "/"
            shell.process_command("pwd")
            
            # Проверяем, что вывод соответствует корневому пути
            self.assertEqual(mock_stdout.getvalue().strip(), '/')
        
        print("Test for 'pwd' at root passed successfully")
    
    @patch('sys.stdout', new_callable=StringIO)  
    def test_cd(self, mock_stdout):
        if TEST_MODE:
            # Тест для команды cd
            vfs = VirtualFileSystem("test.tar")
            shell = VirtualShell(vfs, "test_log.json")
            shell.vfs.fs = {'folder': {}, 'file1.txt': None}
            shell.vfs.current_dir = "/"
            shell.process_command("cd folder")
            self.assertEqual(shell.vfs.current_dir, "/folder")
            
            shell.process_command("pwd")
            self.assertEqual(mock_stdout.getvalue().strip(), '/folder')
        
        print("Test for 'cd' passed successfully")

    @patch('sys.stdout', new_callable=StringIO)  
    def test_cd_invalid(self, mock_stdout):
        if TEST_MODE:
            # Тест для команды cd, когда папка не существует
            vfs = VirtualFileSystem("test.tar")
            shell = VirtualShell(vfs, "test_log.json")
            shell.vfs.fs = {'folder': {}, 'file1.txt': None}
            shell.vfs.current_dir = "/"
            shell.process_command("cd non_existent_folder")
            
            # Проверяем, что ошибка была выведена
            self.assertIn("No such directory: non_existent_folder", mock_stdout.getvalue())
        
        print("Test for invalid 'cd' passed successfully")

    @patch('sys.stdout', new_callable=StringIO)  
    def test_wc(self, mock_stdout):
        if TEST_MODE:
            # Тест для команды wc
            vfs = VirtualFileSystem("test.tar")
            shell = VirtualShell(vfs, "test_log.json")
            shell.vfs.files_content = {'test.txt': "Hello world\nThis is a test file\n"}
            shell.process_command("wc test.txt")
            
            # Проверяем правильность вывода
            self.assertIn("2 5 31 test.txt", mock_stdout.getvalue())
        
        print("Test for 'wc' passed successfully")
    
    @patch('sys.stdout', new_callable=StringIO)  
    def test_wc_empty(self, mock_stdout):
        if TEST_MODE:
            # Тест для команды wc с пустым файлом
            vfs = VirtualFileSystem("test.tar")
            shell = VirtualShell(vfs, "test_log.json")
            shell.vfs.files_content = {'empty.txt': ""}
            shell.process_command("wc empty.txt")
            
            # Проверяем правильность вывода для пустого файла
            self.assertIn("0 0 0 empty.txt", mock_stdout.getvalue())
        
        print("Test for 'wc' with empty file passed successfully")
    
    @patch('sys.stdout', new_callable=StringIO)  
    def test_wc_invalid(self, mock_stdout):
        if TEST_MODE:
            # Тест для команды wc с несуществующим файлом
            vfs = VirtualFileSystem("test.tar")
            shell = VirtualShell(vfs, "test_log.json")
            shell.vfs.files_content = {'test.txt': "Hello world\n"}
            shell.process_command("wc non_existent.txt")
            
            # Проверяем, что ошибка была выведена
            self.assertIn("No such file: non_existent.txt", mock_stdout.getvalue())
        
        print("Test for invalid 'wc' passed successfully")
    
    @patch('sys.stdout', new_callable=StringIO)  
    def test_touch(self, mock_stdout):
        if TEST_MODE:
            # Тест для команды touch
            vfs = VirtualFileSystem("test.tar")
            shell = VirtualShell(vfs, "test_log.json")
            shell.vfs.files_content = {}
            shell.vfs.fs = {}
            shell.process_command("touch newfile.txt")
            
            # Проверяем, что новый файл добавлен
            self.assertIn("File newfile.txt created in virtual file system.", mock_stdout.getvalue())
        
        print("Test for 'touch' passed successfully")

    @patch('sys.stdout', new_callable=StringIO)
    def test_touch_existing(self, mock_stdout):
        if TEST_MODE:
            # Тест для команды touch, когда файл уже существует
            vfs = VirtualFileSystem("test.tar")
            shell = VirtualShell(vfs, "test_log.json")
            shell.vfs.files_content = {'existing.txt': "content"}
            shell.process_command("touch existing.txt")
            
            # Проверяем, что файл не создан снова
            self.assertIn("File existing.txt already exists.", mock_stdout.getvalue())
        
        print("Test for 'touch' with existing file passed successfully")

    @patch('sys.stdout', new_callable=StringIO)  
    def test_add_file_to_tar(self, mock_stdout):
        if TEST_MODE:
            # Тест для добавления файла в архив
            vfs = VirtualFileSystem("test.tar")
            shell = VirtualShell(vfs, "test_log.json")
            shell.process_command("touch added_file.txt")
            
            # Проверяем, что вывод содержит сообщение о добавлении файла
            self.assertIn("File added_file.txt added to the archive.", mock_stdout.getvalue())
        
        print("Test for 'add_file_to_tar' passed successfully")

    @patch('sys.stdout', new_callable=StringIO)  
    def test_log_action(self, mock_stdout):
        if TEST_MODE:
            # Тест для логирования действия
            vfs = VirtualFileSystem("test.tar")
            shell = VirtualShell(vfs, "test_log.json")
            shell.process_command("ls")
            
            # Проверяем, что лог записан
            with open("test_log.json", "r", encoding="utf-8") as log_file:
                log_data = json.load(log_file)
                self.assertEqual(len(log_data), 1)  
                self.assertIn("ls", log_data[0]["command"])
        
        print("Test for 'log_action' passed successfully")
TEST_MODE = os.getenv("RUN_TESTS", "false").lower() == "true"

if __name__ == '__main__':
    if TEST_MODE:
        unittest.main(argv=[''], exit=False)
    else:
        print("Tests are not running. Set the environment variable RUN_TESTS=true to run them.")
