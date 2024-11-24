"""
check.py: Python Project Dependency Analysis Tool.

This script automates the process of identifying libraries imported into a Python project,
comparing these libraries with those installed in the current environment (via pip and conda) and generating
a requirements.txt file with the correct versions of the libraries used in the project, to ensure the replicability of the environment.

Usage:
- Place this script in the root folder of your Python project.
- At the end of the code, add files or folders that should be ignored, including this file. excluded_files = ['check.py']
- Run the script in the terminal with Python 3. Example: python check.py
- The script will go through all the .py files in the project to identify imports.
- It creates a file 'libraries_used.txt' with all the identified libraries.
- Run 'pip list' and 'conda list' to capture all the libraries installed in the environment. - Compares the project libraries with the pip and conda lists, generating 'requirements.txt'.
- Note: This process was tested with libraries installed via pip and conda only!

The generated 'requirements.txt' file contains the libraries used in the project with their respective
installed versions, ready to be used in another environment to replicate the setup.

Developer: Mr. Fox
GitHub: https://github.com/FoxPopBR/check_requirements
This script is part of the SomFox project, designed to facilitate dependency management in Python projects.
Developed for academic purposes of learning programming, developed by a beginner programmer!

Notes:
- The script assumes access to both pip and conda package managers in the execution environment.
- The accuracy in generating requirements.txt depends on the accuracy of the imports in the project files
and the availability of the libraries in the pip and conda registries.

Version: 1.0.0
- Update: [21/02/2024]
Version: 1.0.1
Last Updated [24/11/2024]
"""
import os
import ast
import subprocess
import re


def normalize_library_name(name):
    """Remove ou substitui caracteres especiais para comparação"""
    return re.sub(r'[-._]', '', name.lower())


def find_imported_libraries(file_path):
    """Encontra bibliotecas importadas em um arquivo Python"""
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


def find_all_imported_libraries_in_directory(directory, excluded_files=None, excluded_extensions=None, excluded_directories=None):
    """
    Encontra todas as bibliotecas importadas nos arquivos de um diretório.

    :param directory: Diretório raiz para buscar bibliotecas.
    :param excluded_files: Lista de nomes de arquivos a serem ignorados.
    :param excluded_extensions: Lista de extensões de arquivos a serem ignorados.
    :param excluded_directories: Lista de diretórios a serem ignorados.
    :return: Conjunto de bibliotecas importadas.
    """
    all_libraries = set()
    excluded_files = excluded_files or []
    excluded_extensions = excluded_extensions or []
    excluded_directories = excluded_directories or []

    for root, _, files in os.walk(directory):
        # Ignorar diretórios na lista excluída
        if any(excluded_dir in root for excluded_dir in excluded_directories):
            continue
        for file in files:
            # Ignorar arquivos pelo nome ou extensão
            if file in excluded_files or any(file.endswith(ext) for ext in excluded_extensions):
                continue
            # Processar apenas arquivos .py
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                imported_libraries = find_imported_libraries(file_path)
                all_libraries.update(map(normalize_library_name, imported_libraries))  # Normaliza nomes
    return all_libraries


def save_libraries_to_file(libraries, output_file):
    """Salva as bibliotecas em um arquivo de texto"""
    with open(output_file, 'w') as file:
        for library in sorted(libraries):
            file.write(library + '\n')


def read_libraries_from_file(input_file):
    """Lê bibliotecas de um arquivo de texto"""
    with open(input_file, 'r') as file:
        return [line.strip() for line in file.readlines()]


def get_pip_and_conda_list(temp_dir):
    """
    Gera listas de pacotes instalados (pip e conda) e combina em um único arquivo.
    :param temp_dir: Diretório temporário para salvar os arquivos.
    """
    pip_file = os.path.join(temp_dir, 'pip_list.txt')
    conda_file = os.path.join(temp_dir, 'conda_list.txt')
    list_file = os.path.join(temp_dir, 'list.txt')

    os.makedirs(temp_dir, exist_ok=True)

    with open(pip_file, 'w') as pip_output:
        subprocess.run(['pip', 'list'], stdout=pip_output)

    with open(conda_file, 'w') as conda_output:
        subprocess.run(['conda', 'list'], stdout=conda_output)

    with open(pip_file, 'r') as pip_input, open(conda_file, 'r') as conda_input, open(list_file, 'w') as combined_output:
        combined_output.write(pip_input.read())
        combined_output.write('\n')
        combined_output.write(conda_input.read())

    return list_file


def compare_and_generate_requirements(libraries, list_file, output_file):
    """
    Compara as bibliotecas encontradas no projeto com as instaladas no ambiente e gera requirements.txt.

    :param libraries: Conjunto de bibliotecas encontradas no projeto.
    :param list_file: Arquivo contendo a lista de pacotes instalados.
    :param output_file: Arquivo de saída para requirements.txt.
    """
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


# Diretório do projeto
project_directory = os.getcwd()

# Configuração de exclusões
excluded_files = ['check.py']  # Nomes de arquivos específicos
excluded_extensions = ['.exe', '.txt']  # Extensões de arquivo
excluded_directories = ['NameFolder']  # Diretórios

# Encontrar todas as bibliotecas importadas
imported_libraries = find_all_imported_libraries_in_directory(
    project_directory,
    excluded_files=excluded_files,
    excluded_extensions=excluded_extensions,
    excluded_directories=excluded_directories
)

# Salvar bibliotecas em um arquivo
bibliotecas_file = 'bibliotecas_utilizadas.txt'
save_libraries_to_file(imported_libraries, bibliotecas_file)
print("Bibliotecas utilizadas foram salvas em", bibliotecas_file)

# Gerar pip list e conda list
temp_dir = os.path.join(project_directory, 'temp')
list_file = get_pip_and_conda_list(temp_dir)
print("Arquivos pip list e conda list foram salvos em", list_file)

# Comparar e gerar requirements.txt
compare_and_generate_requirements(imported_libraries, list_file, 'requirements.txt')
print(f"Arquivo requirements.txt gerado com sucesso!")


"""
check.py: Ferramenta de Análise de Dependências de Projetos Python.

Este script automatiza o processo de identificação de bibliotecas importadas em um projeto Python,
comparando essas bibliotecas com as instaladas no ambiente atual (via pip e conda) e gerando
um arquivo requirements.txt com as versões corretas das bibliotecas utilizadas no projeto, para garantir a replicabilidade do ambiente.

Utilização:
- Coloque este script na pasta raiz do seu projeto Python.
- No final do código adicione arquivos ou pastas que devem ser ignorados, incluindo esse arquivo. excluded_files = ['check.py']
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
- atualização: [21/02/2024]
Versão: 1.0.1
Ultima atualização [24/11/2024]
"""