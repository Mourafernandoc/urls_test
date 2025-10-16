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
Para configurar o ambiente de forma rápida e fácil, siga os passos abaixo.

1.  **Execute o script de configuração**:
    Este comando irá criar um ambiente virtual e instalar todas as dependências necessárias.
    ```bash
    chmod +x setup.sh
    ./setup.sh
    ```

2.  **Ative o ambiente virtual**:
    ```bash
    source venv/bin/activate
    ```
    (No Windows, o comando é `venv\Scripts\activate`)

3.  **Copie e edite o ficheiro de URLs**:
    ```bash
    cp urls.example.txt urls.txt
    ```
    Agora, abra o `urls.txt` e adicione as URLs que deseja testar.

Como Usar
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

Para facilitar a atualização do relatório, foi criado um script que automatiza todo o processo.

**Modo Automatizado (Recomendado):**

1.  **Dê permissão de execução ao script** (só precisa fazer isso uma vez):
    ```bash
    chmod +x update_report.sh
    ```
2.  **Execute o script de automação**:
    ```bash
    ./update_report.sh
    ```
Este único comando irá rodar os testes, gerar o relatório, fazer o commit e enviar para o GitHub.

**Modo Manual:**

Se preferir fazer passo a passo, siga os comandos abaixo: `python3 url_tester.py`, `git add index.html screenshots/`, `git commit -m "Atualiza relatório"` e `git push`.

Após alguns instantes, o seu site no GitHub Pages será automaticamente atualizado com o novo relatório.