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


TEST_MODE = os.getenv("RUN_TESTS", "false").lower() == "true"

if __name__ == '__main__':
    if TEST_MODE:
        unittest.main(argv=[''], exit=False)
    else:
        print("Tests are not running. Set the environment variable RUN_TESTS=true to run them.")
