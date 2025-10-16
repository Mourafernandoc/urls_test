#!/bin/bash

# Este script automatiza a execução dos testes de URL e a publicação dos resultados no GitHub.

# Garante que o script pare imediatamente se algum comando falhar.
set -e

echo "--- 1/4: Executando o script de teste de URL... ---"
python3 url_tester.py

echo "\n--- 2/4: Adicionando arquivos atualizados ao Git... ---"
git add index.html screenshots/

echo "\n--- 3/4: Criando commit com data e hora atuais... ---"
git commit -m "Atualiza relatório de testes - $(date +'%d/%m/%Y %H:%M:%S')"

echo "\n--- 4/4: Enviando atualizações para o repositório remoto... ---"
git push

echo "\n--- ✅ Processo finalizado! O relatório foi atualizado e enviado para o GitHub. ---"