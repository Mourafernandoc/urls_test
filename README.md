Automatizador de Testes de URL
Este script Python automatiza a verificação de uma lista de URLs, diferenciando entre páginas web (das quais tira um screenshot) e APIs (das quais verifica o código de status).

Funcionalidades
Lê uma lista de URLs de um arquivo urls.txt.

Tenta classificar automaticamente se a URL é uma página web ou uma API.

Para páginas web:

Abre a página em um navegador Chrome (em modo headless, sem interface gráfica).

Tira um screenshot e o salva na pasta screenshots/.

Para APIs:

Faz uma requisição GET.

Verifica se o código de status da resposta é de sucesso (entre 200 e 299).

Gera um relatório final no console com o resumo de sucessos e falhas.

Gera um relatório web moderno e interativo (`index.html`) com os resultados detalhados e screenshots.

Requisitos
Python 3.6+
Google Chrome instalado na sua máquina.

Como Configurar o Ambiente
Clone ou baixe os arquivos para uma pasta no seu computador.

Instale os pré-requisitos do sistema (para Debian/Ubuntu e derivados):

sudo apt update
sudo apt install python3-venv

Crie um ambiente virtual (recomendado):

python3 -m venv venv

Ative o ambiente:

Windows: venv\Scripts\activate

macOS/Linux: source venv/bin/activate

Instale as bibliotecas Python necessárias:

pip install -r requirements.txt

Como Usar
Edite o arquivo urls.txt: Abra o arquivo em um editor de texto e adicione todas as URLs que você deseja testar. Coloque uma URL por linha.

Execute o script: Abra o seu terminal ou prompt de comando, navegue até a pasta onde salvou os arquivos e execute o seguinte comando:

python3 url_tester.py

Verifique os resultados:

O progresso será exibido no terminal.

Ao final, um arquivo `index.html` será criado (ou atualizado) na pasta do projeto. Abra-o no seu navegador para ver o relatório completo.

Os screenshots das páginas web que funcionaram estarão na pasta screenshots/.

Como Publicar os Relatórios com GitHub Pages
Este projeto foi preparado para funcionar perfeitamente com o GitHub Pages, permitindo que você tenha uma página web pública e sempre atualizada com o último relatório de testes.

1. Habilite o GitHub Pages no seu Repositório:

Vá para o seu repositório no GitHub.
Clique em "Settings" (Configurações).
No menu lateral, vá para "Pages".
Em "Source", selecione a branch que você está a usar (ex: main) e a pasta /(root).
Clique em "Save". O GitHub irá fornecer a URL do seu site (algo como https://seu-usuario.github.io/seu-repositorio/).

2. Fluxo de Trabalho para Atualização:

Após cada execução do script localmente (`python3 url_tester.py`), novos resultados serão gerados. O arquivo `index.html` e a pasta `screenshots/` serão atualizados.

Adicione e "commite" as alterações no Git:

git add index.html screenshots/
git commit -m "Atualiza relatório de testes - $(date)"

Envie as alterações para o GitHub:

git push

Após alguns instantes, o seu site no GitHub Pages será automaticamente atualizado com o novo relatório.