import os
import ast
import subprocess
import re

def normalize_library_name(name):
    # Remove ou substitui caracteres especiais para comparação
    return re.sub(r'[-._]', '', name.lower())

def find_imported_libraries(file_path):
    libraries = set()
    with open(file_path, 'r', encoding='utf-8') as file:
        tree = ast.parse(file.read(), filename=file_path)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    libraries.add(alias.name)
            elif isinstance(node, ast.ImportFrom):
                libraries.add(node.module)
    return libraries

def find_all_imported_libraries_in_directory(directory):
    all_libraries = set()
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                imported_libraries = find_imported_libraries(file_path)
                all_libraries.update(imported_libraries)
    return all_libraries

def save_libraries_to_file(libraries, output_file):
    with open(output_file, 'w') as file:
        for library in sorted(libraries):
            file.write(library + '\n')

def read_libraries_from_file(input_file):
    with open(input_file, 'r') as file:
        return [line.strip() for line in file.readlines()]

def get_pip_and_conda_list():
    subprocess.run(['pip', 'list', '>', 'pip_list.txt'], shell=True)
    subprocess.run(['conda', 'list', '>', 'conda_list.txt'], shell=True)
    with open('pip_list.txt', 'r') as pip_file, open('conda_list.txt', 'r') as conda_file, open('list.txt', 'w') as output_file:
        output_file.write(pip_file.read())
        output_file.write('\n')
        output_file.write(conda_file.read())

def compare_and_generate_requirements(libraries, list_file, output_file):
    with open(list_file, 'r') as file:
        installed_packages = file.read()

    found_libraries = set()
    with open(output_file, 'w') as file:
        for library in libraries:
            normalized_library_name = normalize_library_name(library)
            for line in installed_packages.split('\n'):
                if normalized_library_name in normalize_library_name(line):
                    parts = line.split()
                    if len(parts) >= 2:
                        version = parts[1]
                        file.write(f"{library}=={version}\n")
                        found_libraries.add(library)
                        break

    not_found_libraries = set(libraries) - found_libraries
    for lib in not_found_libraries:
        print(f"Biblioteca {lib} não encontrada no pip ou no conda.")

# Diretório do seu projeto
project_directory = os.getcwd()  # Obtém o diretório atual do script

# Encontrar todas as bibliotecas importadas nos arquivos do projeto
imported_libraries = find_all_imported_libraries_in_directory(project_directory)

# Salvar as bibliotecas em um arquivo de texto
bibliotecas_file = 'bibliotecas_utilizadas.txt'
save_libraries_to_file(imported_libraries, bibliotecas_file)
print("Bibliotecas utilizadas foram salvas em", bibliotecas_file)

# Gerar pip list e conda list e salvar em list.txt
get_pip_and_conda_list()
print("Arquivos pip list e conda list foram salvos em list.txt")

# Comparar as bibliotecas e gerar requirements.txt
compare_and_generate_requirements(imported_libraries, 'list.txt', 'requirements.txt')
print(f"Arquivo requirements.txt gerado com sucesso!")
