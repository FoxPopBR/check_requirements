
# check.py: Python Project Dependency Analysis Tool

This script automates the process of identifying libraries imported in a Python project, comparing these libraries with those installed in the current environment (via pip and conda), and generating a `requirements.txt` file with the correct versions of the libraries used in the project to ensure replicability of the environment.

## How It Works

The `check.py` script performs the following actions:

1. **Library Identification:** Scans all `.py` files in the project to identify imported libraries.
2. **Library Usage Recording:** Creates a `bibliotecas_utilizadas.txt` file listing all identified libraries.
3. **Environment Analysis:** Executes `pip list` and `conda list` to capture all libraries installed in the current environment.
4. **`requirements.txt` Generation:** Compares project libraries with pip and conda lists, generating a `requirements.txt`.
- Note: This process has been tested with libraries installed via pip and conda only!

The generated `requirements.txt` file contains the libraries used in the project with their respective installed versions, ready to be used in another environment to replicate the setup.

## Usage

To use this script in your project, follow the steps below:

- Place the `check.py` file in the root folder of your Python project.
- Open a terminal and navigate to the root folder of your project.
- Run the command `python check.py`.
- After execution, the `requirements.txt` file will be generated in the root folder.

## Development

- **Developer:** Senhor Fox
- **GitHub:** [check_requirements](https://github.com/FoxPopBR/check_requirements)
- **Purpose:** To facilitate dependency management in Python projects.
- **Note:** Developed for academic purposes and programming learning by a beginner programmer.

## Important Observations

- The script assumes access to both pip and conda package managers in the execution environment.
- The accuracy of the generated `requirements.txt` file depends on the correct imports in the `.py` files and the availability of the libraries in the pip and conda registries.

## Version

- **Current Version:** 1.0.0
- **Last Update:** 21/02/2024

This README provides essential information to understand and utilize the `check.py` in your Python projects, ensuring efficient dependency management and facilitating the setup of consistent development environments.

For more information and updates, visit the GitHub repository.
