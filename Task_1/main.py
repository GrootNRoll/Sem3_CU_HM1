import json
from emulator import VirtualFileSystem, VirtualShell
import unittest
from unittest.mock import patch
from io import StringIO
import os
import json



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


TEST_MODE = os.getenv("RUN_TESTS", "false").lower() == "true"

if __name__ == '__main__':
    if TEST_MODE:
        unittest.main(argv=[''], exit=False)
    else:
        print("Tests are not running. Set the environment variable RUN_TESTS=true to run them.")
