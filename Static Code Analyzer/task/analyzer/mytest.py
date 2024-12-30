import re
import subprocess
import unittest

class MyTestCase(unittest.TestCase):
    def run_command(self, *args):
        command = ['python', 'code_analyzer.py'] + list(args)
        return subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

    def test_single_file(self):
        result = self.run_command(f'mycode4.py')
        expected_line_no = [1, 3]
        expected_errors = ['S004', 'S004']
        matches = re.findall(r"Line (\d+): (S\d+)", result.stdout)
        actual_line_no = [int(line) for line, _ in matches]
        actual_errors = [code for _, code in matches]
        self.assertEqual(expected_errors, actual_errors)
        self.assertEqual(expected_line_no, actual_line_no)

    def test_multiple_files(self):
        result = self.run_command('.')
        expected_path = (['./code_analyzer.py'] * 18 + ['./mycode1.py'] * 9 + ['./mycode2.py'] * 4 +
                         ['./mycode3.py'] * 3 + ['./mycode4.py'] * 2 + ['./mycode5.py'] * 3 + ['./mytest.py'] * 8)
        expected_line_no = [20, 23, 24, 24, 25, 28, 29, 30, 30, 32, 33, 34, 35, 41, 47, 58, 65, 73, 1, 2, 3, 3, 6, 11,
                            13, 13, 13, 1, 5, 6, 5, 1, 4, 14, 1, 3, 1, 4, 15, 27, 28, 28, 29, 30, 31, 32, 33]
        expected_errors = ['S001', 'S004'] * 4 + ['S005'] + ['S001'] * 9 + ['S004', 'S003', 'S001', 'S003', 'S001',
                            'S006', 'S003', 'S004', 'S005', 'S011', 'S010', 'S011', 'S012', 'S007', 'S008', 'S009',
                            'S004', 'S004', 'S007', 'S008', 'S009', 'S001', 'S001', 'S002'] + ['S001'] * 5
        matches = re.findall(r"(\S+): Line (\d+): (S\d+)", result.stdout)
        actual_path = [path for path, _, _ in matches]
        actual_line_no = [int(line) for _, line, _ in matches]
        actual_errors = [code for _, _, code in matches]
        self.assertEqual(expected_path, actual_path)
        self.assertEqual(expected_errors, actual_errors)
        self.assertEqual(expected_line_no, actual_line_no)

if __name__ == '__main__':
    unittest.main()
