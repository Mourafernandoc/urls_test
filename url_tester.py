# -*- coding: utf-8 -*-

import os
import re
import time
from datetime import datetime
import requests
import warnings
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from urllib3.exceptions import InsecureRequestWarning

# --- Configurações ---
# Ficheiro que contém a lista de URLs para testar
URL_FILE = 'urls.txt'
# Pasta para guardar os screenshots das páginas web
SCREENSHOT_DIR = 'screenshots'
# Ficheiro de saída para o relatório HTML
REPORT_FILE = 'index.html'
# Prefixo para as pastas de perfil do Chrome de automação
CHROME_PROFILE_DIR = 'chrome_data'
# Tempo de espera (em segundos) para a página carregar antes de tirar o screenshot
WAIT_TIME = 5 # Aumentado para dar mais tempo a sistemas lentos
# Timeout para requisições de API
API_TIMEOUT = 15
# Ignorar erros de certificado SSL (MUITO útil para ambientes de homologação/teste)
IGNORE_SSL_ERRORS = True

# Suprimir avisos sobre não verificar SSL, para manter a consola limpa
if IGNORE_SSL_ERRORS:
    warnings.filterwarnings("ignore", category=InsecureRequestWarning)


def sanitize_filename(url):
    """
    Limpa uma URL para criar um nome de ficheiro válido.
    Remove o protocolo e substitui caracteres inválidos por '_'.
    """
    # Remove http:// ou https://
    sanitized = re.sub(r'https?://', '', url)
    # Substitui caracteres não alfanuméricos por underscore
    sanitized = re.sub(r'[^a-zA-Z0-9\-_\.]', '_', sanitized)
    # Trunca o nome do ficheiro para evitar que seja muito longo
    return sanitized[:100]

def extract_system_name(url):
    """Extrai um nome de sistema legível a partir da URL."""
    try:
        # Pega a primeira parte do hostname (ex: 'homcetas' de 'homcetas.oci.ibama.gov.br')
        hostname = re.search(r'https?://([^/]+)', url).group(1)
        return hostname.split('.')[0].replace('-', ' ').title()
    except (AttributeError, IndexError):
        return "Sistema Desconhecido"

def test_web_url(driver, url):
    """
    Testa uma URL de página web: acede e tira um screenshot.
    Retorna True se bem-sucedido, False caso contrário.
    """
    try:
        print(f"  -> A aceder à página: {url}")
        driver.get(url)
        # Espera um tempo fixo para elementos dinâmicos carregarem
        time.sleep(WAIT_TIME)

        filename = f"{sanitize_filename(url)}.png"
        filepath = os.path.join(SCREENSHOT_DIR, filename)

        driver.save_screenshot(filepath)
        print(f"  [SUCESSO] Screenshot guardado em: {filepath}")
        return {'status': 'success', 'screenshot': filepath, 'details': f'Screenshot salvo em {filepath}'}
    except WebDriverException as e:
        print(f"  [FALHA] Não foi possível aceder à URL ou tirar o screenshot.")
        # Simplifica a mensagem de erro para ser mais legível
        error_message = str(e).split('\n')[0]
        print(f"  Erro: {error_message}")
        return {'status': 'failure', 'screenshot': None, 'details': error_message}

def test_api_url(url):
    """
    Testa uma URL de API: verifica o status code da resposta.
    Retorna True se o status for 2xx, False caso contrário.
    """
    try:
        print(f"  -> A verificar API: {url}")
        # Usamos stream=True e um cabeçalho de User-Agent para simular um navegador
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, timeout=API_TIMEOUT, headers=headers, allow_redirects=True, verify=not IGNORE_SSL_ERRORS)

        # Verifica se o código de status é de sucesso (200-299)
        if 200 <= response.status_code < 300:
            print(f"  [SUCESSO] API respondeu com status: {response.status_code}")
            return {'status': 'success', 'status_code': response.status_code, 'details': f'Status Code: {response.status_code}'}
        else:
            print(f"  [FALHA] API respondeu com status de erro: {response.status_code}")
            return {'status': 'failure', 'status_code': response.status_code, 'details': f'Status Code: {response.status_code}'}
    except requests.RequestException as e:
        print(f"  [FALHA] Erro ao conectar com a API.")
        error_message = str(e).split('\n')[0]
        print(f"  Erro: {error_message}")
        return {'status': 'failure', 'status_code': None, 'details': error_message}

def classify_and_test_url(driver, url):
    """
    Classifica a URL como Web ou API e chama a função de teste apropriada.
    """
    print(f"\nA testar URL: {url}")
    result = {}
    try:
        # Faz uma requisição HEAD para ser mais rápido e obter o Content-Type
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.head(url, timeout=API_TIMEOUT, headers=headers, allow_redirects=True, verify=not IGNORE_SSL_ERRORS)
        content_type = response.headers.get('Content-Type', '').lower()

        # Classificação: se o conteúdo for HTML, tratamos como página web.
        if 'text/html' in content_type:
            print("  -> URL classificada como PÁGINA WEB.")
            result = test_web_url(driver, url)
            result['type'] = 'web'
        else:
            print(f"  -> URL classificada como API (Content-Type: {content_type}).")
            result = test_api_url(url)
            result['type'] = 'api'
            
    except requests.RequestException:
        # Se o HEAD falhar, pode ser uma aplicação web complexa. Tentamos como página web.
        print("  -> Não foi possível classificar com HEAD. A tentar como PÁGINA WEB por padrão.")
        result = test_web_url(driver, url)
        result['type'] = 'web'
    
    result['url'] = url
    result['system_name'] = extract_system_name(url)
    return result

def generate_html_report(results, start_time_str, duration):
    """Gera um relatório HTML a partir dos resultados dos testes."""
    
    success_count = sum(1 for r in results if r['status'] == 'success')
    failure_count = len(results) - success_count
    
    # --- CSS para um design moderno e profissional ---
    css_style = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
        body { font-family: 'Roboto', sans-serif; background-color: #f4f7f9; color: #333; margin: 0; padding: 20px; }
        .container { max-width: 1200px; margin: auto; background: #fff; padding: 30px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
        h1, h2 { color: #2c3e50; border-bottom: 2px solid #e0e0e0; padding-bottom: 10px; }
        h1 { font-size: 2em; }
        h2 { font-size: 1.5em; margin-top: 40px; }
        .summary { display: flex; justify-content: space-around; text-align: center; margin: 20px 0; padding: 20px; background: #ecf0f1; border-radius: 8px; }
        .summary-item { flex-grow: 1; }
        .summary-item h3 { margin: 0 0 10px 0; font-weight: 400; color: #7f8c8d; }
        .summary-item .value { font-size: 2.5em; font-weight: 700; }
        .summary-item .value.success { color: #27ae60; }
        .summary-item .value.failure { color: #c0392b; }
        .results-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); gap: 20px; }
        .card { background: #fff; border: 1px solid #e0e0e0; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); overflow: hidden; transition: transform 0.2s, box-shadow 0.2s; }
        .card:hover { transform: translateY(-5px); box-shadow: 0 8px 20px rgba(0,0,0,0.1); }
        .card-header { padding: 15px; display: flex; justify-content: space-between; align-items: center; }
        .card-header.success { background-color: #e8f5e9; border-left: 5px solid #27ae60; }
        .card-header.failure { background-color: #fbe9e7; border-left: 5px solid #c0392b; }
        .card-title { font-weight: 700; font-size: 1.1em; margin: 0; }
        .status-icon { font-size: 1.5em; }
        .status-icon.success { color: #27ae60; }
        .status-icon.failure { color: #c0392b; }
        .card-body { padding: 15px; font-size: 0.9em; }
        .card-body a { color: #3498db; text-decoration: none; word-break: break-all; }
        .card-body a:hover { text-decoration: underline; }
        .card-body p { margin: 0 0 10px 0; }
        .screenshot { margin-top: 15px; }
        .screenshot img { max-width: 100%; border-radius: 4px; border: 1px solid #ddd; cursor: pointer; }
        .footer { text-align: center; margin-top: 40px; font-size: 0.8em; color: #95a5a6; }
    </style>
    """

    # --- Corpo do HTML ---
    html_body = f"""
    <div class="container">
        <h1>Relatório de Testes de URL</h1>
        <div class="summary">
            <div class="summary-item">
                <h3>Data da Execução</h3>
                <div class="value" style="font-size: 1.5em;">{start_time_str}</div>
            </div>
            <div class="summary-item">
                <h3>Total de URLs</h3>
                <div class="value">{len(results)}</div>
            </div>
            <div class="summary-item">
                <h3>Sucessos</h3>
                <div class="value success">{success_count}</div>
            </div>
            <div class="summary-item">
                <h3>Falhas</h3>
                <div class="value failure">{failure_count}</div>
            </div>
            <div class="summary-item">
                <h3>Duração</h3>
                <div class="value" style="font-size: 1.5em;">{duration:.2f}s</div>
            </div>
        </div>

        <h2>Resultados Detalhados</h2>
        <div class="results-grid">
    """

    # Ordena os resultados para mostrar as falhas primeiro
    sorted_results = sorted(results, key=lambda x: x['status'] == 'success')

    for result in sorted_results:
        status_class = result['status']
        icon = '✔' if status_class == 'success' else '✖'
        
        card_content = f"""
        <div class="card">
            <div class="card-header {status_class}">
                <h3 class="card-title">{result['system_name']}</h3>
                <span class="status-icon {status_class}">{icon}</span>
            </div>
            <div class="card-body">
                <p><strong>URL:</strong> <a href="{result['url']}" target="_blank">{result['url']}</a></p>
                <p><strong>Tipo:</strong> {result['type'].upper()}</p>
                <p><strong>Detalhes:</strong> {result['details']}</p>
        """
        
        if result['type'] == 'web' and result.get('screenshot'):
            card_content += f"""
                <div class="screenshot">
                    <a href="{result['screenshot']}" target="_blank">
                        <img src="{result['screenshot']}" alt="Screenshot de {result['url']}" loading="lazy">
                    </a>
                </div>
            """
        
        card_content += "</div></div>"
        html_body += card_content

    html_body += """
        </div>
        <div class="footer">
            Relatório gerado automaticamente por URL Tester.
        </div>
    </div>
    """

    # --- Montagem final do HTML ---
    html_content = f"<!DOCTYPE html><html lang='pt-br'><head><meta charset='UTF-8'><title>Relatório de Testes</title>{css_style}</head><body>{html_body}</body></html>"

    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"\n[SUCESSO] Relatório HTML gerado em: {os.path.abspath(REPORT_FILE)}")

def main():
    """
    Função principal que orquestra a execução dos testes.
    """
    print("--- A iniciar o Automatizador de Testes de URL ---")

    start_time = time.time()
    start_time_str = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

    # 1. Verifica se o ficheiro de URLs existe
    if not os.path.exists(URL_FILE):
        print(f"[ERRO] Ficheiro '{URL_FILE}' não encontrado!")
        print("Por favor, crie este ficheiro e adicione as URLs que deseja testar, uma por linha.")
        return

    # 2. Lê as URLs do ficheiro
    with open(URL_FILE, 'r', encoding='utf-8') as f:
        urls_to_test = [line.strip() for line in f if line.strip() and not line.startswith('#')]

    if not urls_to_test:
        print("[AVISO] O ficheiro de URLs está vazio. Nenhum teste a ser executado.")
        return

    # 3. Cria as pastas necessárias se elas não existirem
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)

    # 4. Configura o Selenium WebDriver (Chrome)
    chrome_options = Options()
    
    # --- PARA DEPURAR: Comente a linha abaixo para o navegador abrir e você ver o que acontece ---
    chrome_options.add_argument("--headless")
    
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--log-level=3") 
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    # **CORREÇÃO**: Adiciona um diretório de utilizador único para evitar conflitos com o Chrome já aberto
    # Criamos um perfil único para cada execução para garantir um ambiente limpo.
    unique_profile_path = os.path.join(os.getcwd(), f"{CHROME_PROFILE_DIR}_{int(time.time())}")
    chrome_options.add_argument(f"--user-data-dir={unique_profile_path}")
    
    if IGNORE_SSL_ERRORS:
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--allow-insecure-localhost')

    # **CORREÇÃO AVANÇADA PARA LINUX**: Adiciona flags de estabilidade
    # Essencial para execução em ambientes CI/CD ou servidores sem interface gráfica.
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")


    driver = None
    try:
        # **NOVA ABORDAGEM**: O webdriver-manager encontra e baixa o driver correto automaticamente.
        print("  -> A verificar e a instalar a versão correta do ChromeDriver...")
        service = Service(ChromeDriverManager().install())
        
        print("  -> A iniciar o WebDriver...")
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        results = []

        # 5. Itera sobre as URLs e executa os testes
        for url in urls_to_test:
            result = classify_and_test_url(driver, url)
            results.append(result)
        
        # 6. Gera o relatório HTML
        duration = time.time() - start_time
        generate_html_report(results, start_time_str, duration)

    except WebDriverException as e:
        print("\n[ERRO CRÍTICO] Ocorreu um erro com o WebDriver.")
        print("Ocorreu um problema ao iniciar o Selenium. Verifique a sua ligação à internet ou se existem restrições de firewall que possam impedir o download do ChromeDriver.")
        print(f"Detalhes do erro: {e}")
        # Mesmo em caso de erro crítico, tenta gerar um relatório parcial se houver resultados.
        if 'results' in locals() and results:
            generate_html_report(results, start_time_str, time.time() - start_time)

    finally:
        # 7. Garante que o navegador seja fechado no final
        if driver:
            driver.quit()
            print("\n--- Testes Finalizados ---")


if __name__ == '__main__':
    main()
