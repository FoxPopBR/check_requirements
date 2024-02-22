
# check.py: Ferramenta de Análise de Dependências para Projetos Python

Este projeto oferece um script Python denominado `check.py`, desenvolvido para automatizar a identificação e análise das bibliotecas utilizadas em projetos Python. O principal objetivo é facilitar a replicabilidade do ambiente de desenvolvimento ao gerar um arquivo `requirements.txt` contendo as versões exatas das bibliotecas utilizadas.

## Como Funciona

O script `check.py` executa as seguintes ações:

1. **Identificação de Bibliotecas:** Percorre todos os arquivos `.py` no projeto para identificar bibliotecas importadas.
2. **Registro de Bibliotecas Utilizadas:** Cria um arquivo `bibliotecas_utilizadas.txt` listando todas as bibliotecas identificadas.
3. **Análise de Ambiente:** Executa `pip list` e `conda list` para obter uma lista de todas as bibliotecas instaladas no ambiente atual.
4. **Geração de `requirements.txt`:** Compara as bibliotecas do projeto com as listas obtidas do pip e conda, gerando um arquivo `requirements.txt` com as versões corretas para instalação.

## Utilização

Para utilizar o script em seu projeto, siga os passos abaixo:

- Coloque o arquivo `check.py` na pasta raiz do seu projeto Python.
- Abra um terminal e navegue até a pasta raiz do seu projeto.
- Execute o comando `python check.py`.
- Após a execução, o arquivo `requirements.txt` será gerado na pasta raiz.

## Desenvolvimento

- **Desenvolvedor:** Senhor Fox
- **GitHub:** [check_requirements](https://github.com/FoxPopBR/check_requirements)
- **Objetivo:** Facilitar a gestão de dependências em projetos Python.
- **Nota:** Desenvolvido para fins acadêmicos e aprendizado de programação.

## Observações Importantes

- O script assume que tanto `pip` quanto `conda` estão disponíveis no ambiente de execução.
- A precisão do arquivo `requirements.txt` gerado depende das importações corretas nos arquivos `.py` e da disponibilidade das bibliotecas nos registros do pip e conda.

## Versão

- **Versão Atual:** 1.0.0
- **Última Atualização:** 21/02/2024

Este README fornece as informações essenciais para entender e utilizar o `check.py` em seus projetos Python, garantindo uma gestão eficiente de dependências e facilitando a configuração de ambientes de desenvolvimento consistentes.

Para mais informações e atualizações, visite o repositório no GitHub.
