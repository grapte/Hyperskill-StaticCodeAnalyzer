import ast
import os
import re
import sys

def is_snake_case(name: str) -> bool:
    return all(
        c.islower() or c == '_' or c.isdigit()
        for c in name
    ) and not name[0].isdigit()

def check_code(file_path):
    f = open(file_path, 'r')
    prev1, prev2, prev3 = 'a', 'a', 'a'
    for no, line in enumerate(f, start=1):
        if len(line.rstrip('\n')) > 79:
            print(f'{file_path}: Line {no}: S001 Too long')
        if line.strip() and (len(line) - len(line.lstrip())) % 4 != 0:
            print(f'{file_path}: Line {no}: S002 Indentation is not a multiple of four')
        if (
                ';' in line and  # Check if there's a semicolon in the line
                ('#' not in line or line.find(';') < line.find(
                    '#')) and  # Ensure the semicolon is before the comment (if any)
                not re.search(r"(\".*?;.*?\"|'.*?;.*?')", line)  # Ensure ; is not inside quotes
        ):
            print(f'{file_path}: Line {no}: S003 Unnecessary semicolon')
        if (pos := line.find('#')) > 1 and line[pos - 2:pos] != '  ':
            print(f'{file_path}: Line {no}: S004 Less than two spaces before inline comments')
        if (pos := line.find('#')) != -1 and 'todo' in line[pos:].lower():
            print(f'{file_path}: Line {no}: S005 TODO found')
        if line.strip() and (prev1.strip() == prev2.strip() == prev3.strip() == ''):
            print(f'{file_path}: Line {no}: S006 More than two blank lines used before this line')
        if m := re.match(r'^\s*(class|def)\s{2,}(\w+)', line):  # Matches two or more spaces after class or def
            print(f'{file_path}: Line {no}: S007 Too many spaces after {m.group(2)}')
        if (
            (m := re.match(r'^\s*(class|def)\s+(\w+)', line))
            and m.group(1) == 'class'
            and not (m.group(2)[0].isupper() and '_' not in m.group(2))
        ):
            print(f'{file_path}: Line {no}: S008 Class name {m.group(2)} should be written in CamelCase')
        if (
            (m := re.match(r'^\s*(class|def)\s+(\w+)', line))
            and m.group(1) == 'def'
            and not m.group(2).islower()
        ):
            print(f'{file_path}: Line {no}: S009 Function name {m.group(2)} should be written in snake_case')
        prev1, prev2, prev3 = prev2, prev3, line

    s = open(file_path, 'r')
    source = s.read()
    tree = ast.parse(source)

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            for arg in node.args.args:
                if not is_snake_case(arg.arg):
                    print(f'{file_path}: Line {arg.lineno}: S010 Argument name {arg.arg} should be written in snake_case')
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    var_name = target.id
                    if not is_snake_case(var_name):
                        print(
                            f'{file_path}: Line {target.lineno}: S011 Variable {var_name} should be written in snake_case')
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            func_name = node.name
            for default in node.args.defaults:
                if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                    print(
                        f'{file_path}: Line {node.lineno}: S012 The default argument value is mutable')

def main():
    path = sys.argv[1]
    if os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            for file in sorted(files):
                file_path = os.path.join(root, file)
                check_code(file_path)
    elif os.path.isfile(path):
        file_path = path
        check_code(file_path)

if __name__ == '__main__':
    main()