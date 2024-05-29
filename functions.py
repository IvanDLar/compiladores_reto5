import os

def get_file_lines(file_path):
    commands_to_exec = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            commands_to_exec.append(line.strip())
    return commands_to_exec