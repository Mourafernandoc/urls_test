#!/bin/bash

# Este script configura o ambiente de desenvolvimento para o projeto URL Tester.

# Garante que o script pare imediatamente se algum comando falhar.
set -e

echo "--- Iniciando a configuração do ambiente ---"

# 1. Verifica se o Python 3 está instalado
if ! command -v python3 &> /dev/null
then
    echo "[ERRO] Python 3 não encontrado. Por favor, instale o Python 3 e tente novamente."
    exit 1
fi
echo "-> Python 3 encontrado."

# 2. Cria o ambiente virtual
VENV_DIR="venv"
echo "-> A criar ambiente virtual em '$VENV_DIR'..."
python3 -m venv $VENV_DIR

# 3. Instala as dependências usando o pip do ambiente virtual
echo "-> A instalar dependências do requirements.txt..."
$VENV_DIR/bin/pip install -r requirements.txt

echo ""
echo "--- ✅ Configuração concluída com sucesso! ---"
echo ""
echo "Para executar os testes, siga os passos:"
echo "1. Ative o ambiente virtual: source $VENV_DIR/bin/activate"
echo "2. Edite o ficheiro 'urls.txt' com as URLs que deseja testar."
echo "3. Execute o script de teste: python3 url_tester.py"
echo ""