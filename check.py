"""
check.py: Python Project Dependency Analysis Tool.

This script automates the process of identifying libraries imported into a Python project,
comparing these libraries with those installed in the current environment (via pip and conda) and generating
a requirements.txt file with the correct versions of the libraries used in the project, to guarantee the replicability of the environment.

Use:
- Place this script in the root folder of your Python project.
- Run the script in the terminal with Python 3. Example: python check.py
- The script will go through all .py files in the project to identify imports.
- It creates a file 'bibliotecas_utilizados.txt' with all identified libraries.
- Runs 'pip list' and 'conda list' to capture all libraries installed in the environment.
- Compares project libraries with pip and conda lists, generating 'requirements.txt'.
- Note: This process was tested with libraries installed via pip and conda only!

The generated 'requirements.txt' file contains the libraries used in the project with their respective
installed versions, ready to be used in another environment to replicate the setup.

Developer: Mr Fox
GitHub: https://github.com/FoxPopBR/check_requirements
This script is part of the SomFox project, intended to facilitate dependency management in Python projects.
Developed for academic programming learning purposes, developed by a beginner programmer!

Comments:
- The script assumes access to both pip and conda package managers at runtime.
- Accuracy in generating requirements.txt depends on the accuracy of imports in the project files
and the availability of libraries in pip and conda registries.

Version: 1.0.0
Last updated: [02/21/2024]
"""
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

"""
check.py: Ferramenta de Análise de Dependências de Projetos Python.

Este script automatiza o processo de identificação de bibliotecas importadas em um projeto Python,
comparando essas bibliotecas com as instaladas no ambiente atual (via pip e conda) e gerando
um arquivo requirements.txt com as versões corretas das bibliotecas utilizadas no projeto, para garantir a replicabilidade do ambiente.

Utilização:
- Coloque este script na pasta raiz do seu projeto Python.
- Execute o script no terminal com Python 3. Exemplo: python check.py
- O script irá percorrer todos os arquivos .py do projeto para identificar importações.
- Ele cria um arquivo 'bibliotecas_utilizadas.txt' com todas as bibliotecas identificadas.
- Executa 'pip list' e 'conda list' para capturar todas as bibliotecas instaladas no ambiente.
- Compara as bibliotecas do projeto com as listas do pip e conda, gerando 'requirements.txt'.
- Observação: Esse processo foi testado com bibliotecas instaladas via pip e conda somente!

O arquivo 'requirements.txt' gerado contém as bibliotecas utilizadas no projeto com suas respectivas
versões instaladas, pronto para ser usado em outro ambiente para replicar o setup.

Desenvolvedor: Senhor Fox
GitHub: https://github.com/FoxPopBR/check_requirements
Este script faz parte do projeto SomFox, destinado a facilitar a gestão de dependências em projetos Python.
Desenvolvido com finalidades acadêmicas de aprendizado de programação, desenvolvido por um programador inciante!

Observações:
- O script assume acesso a ambos os gerenciadores de pacotes pip e conda no ambiente de execução.
- A precisão na geração do requirements.txt depende da exatidão das importações nos arquivos do projeto
e da disponibilidade das bibliotecas nos registros do pip e conda.

Versão: 1.0.0
Última atualização: [21/02/2024]
"""