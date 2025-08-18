# fetch_repos_robusto.py

import requests
import json
import time

# --- Configurações ---
GITHUB_API_URL = "https://api.github.com/graphql"
GITHUB_TOKEN = "NAO POSSO COMMITAR MEU TOKEN RS RS RS RS"
HEADERS = {
    "Authorization": f"bearer {GITHUB_TOKEN}",
    "Content-Type": "application/json",
}

# --- A Consulta GraphQL ---
graphql_query = """
query($queryString: String!, $first: Int, $after: String) {
  search(query: $queryString, type: REPOSITORY, first: $first, after: $after) {
    repositoryCount
    pageInfo {
      endCursor
      hasNextPage
    }
    nodes {
      ... on Repository {
        nameWithOwner
        url
        createdAt
        pushedAt
        description
        stargazerCount
        forkCount
        watchers {
          totalCount
        }
        issues(states: OPEN) {
          totalCount
        }
        issuesClosed: issues(states: CLOSED) {
          totalCount
        }
        pullRequests(states: OPEN) {
          totalCount
        }
        pullRequestsMerged: pullRequests(states: MERGED) {
          totalCount
        }
        pullRequestsClosed: pullRequests(states: CLOSED) {
          totalCount
        }
        releases {
          totalCount
        }
        primaryLanguage {
          name
        }
        diskUsage
        licenseInfo {
          name
          spdxId
        }
        topics: repositoryTopics(first: 10) {
          nodes {
            topic {
              name
            }
          }
        }
      }
    }
  }
}
"""

def run_query_robusto(query, variables):
    """Função  para enviar a requisição, com timeout e 3 tentativas. (Refatorar isso aqui depois, tem uma forma melhor de fazer) !!LEMBRETE!!"""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            # Timeout de 30 segundos para a requisição não ficar presa indefinidamente
            request = requests.post(
                GITHUB_API_URL,
                json={"query": query, "variables": variables},
                headers=HEADERS,
                timeout=30
            )
            if request.status_code == 200:
                # Se a resposta contiver erros da API GraphQL, ainda assim tratamos como falha para retry
                response_json = request.json()
                if "errors" in response_json:
                     print(f"Tentativa {attempt + 1}: API do GitHub retornou um erro: {response_json['errors']}")
                     # Damos uma pausa antes de tentar de novo
                     time.sleep(5 * (attempt + 1))
                     continue
                return response_json
                
            elif request.status_code in [502, 504]: # Gateway Timeout ou Bad Gateway
                print(f"Tentativa {attempt + 1} falhou com erro {request.status_code}. Tentando novamente em {5 * (attempt + 1)} segundos...")
                time.sleep(5 * (attempt + 1)) # Espera mais a cada tentativa
                continue
            else:
                raise Exception(f"Query falhou com o código {request.status_code}. {request.text}")

        except requests.exceptions.Timeout:
            print(f"Tentativa {attempt + 1} excedeu o timeout. Tentando novamente em {5 * (attempt + 1)} segundos...")
            time.sleep(5 * (attempt + 1))

    raise Exception(f"A query falhou após {max_retries} tentativas. Verifique a API ou a complexidade da query.")


def fetch_all_repositories(total_repos_to_fetch=100):
    """Busca repositórios em páginas até atingir o número desejado."""
    all_repos = []
    after_cursor = None
    
    query_string = "stars:>5000 sort:stars-desc"
    
    # Buscando em lotes menores para reduzir a chance de timeout
    repos_per_page = 30

    while len(all_repos) < total_repos_to_fetch:
        # Garante que não vamos pedir mais do que o necessário na última página
        remaining = total_repos_to_fetch - len(all_repos)
        current_batch_size = min(remaining, repos_per_page)

        if current_batch_size <= 0:
            break

        variables = {
            "queryString": query_string,
            "first": current_batch_size,
            "after": after_cursor
        }

        print(f"Buscando {current_batch_size} repositórios... (já coletados: {len(all_repos)})")
        result = run_query_robusto(graphql_query, variables)

        data = result.get("data", {}).get("search")
        if not data:
            print("Não foi possível extrair os dados da resposta. Resposta recebida:", result)
            break

        fetched_repos = data["nodes"]
        all_repos.extend(fetched_repos)

        page_info = data["pageInfo"]
        if not page_info["hasNextPage"]:
            print("Chegou ao fim dos resultados da busca.")
            break
        
        after_cursor = page_info["endCursor"]
        
        # Pausa para ser gentil com a API
        time.sleep(2)

    return all_repos[:total_repos_to_fetch]

# --- Execução Principal ---
if __name__ == "__main__":
    if GITHUB_TOKEN == "SEU_TOKEN_AQUI":
        print("ERRO: Por favor, substitua 'SEU_TOKEN_AQUI' pelo seu Token de Acesso Pessoal do GitHub no script.")
    else:
        print("Iniciando a coleta de dados de 100 repositórios (versão robusta)...")
        repositories = fetch_all_repositories(total_repos_to_fetch=100)

        output_filename = "repositories_data_completo.json"
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(repositories, f, ensure_ascii=False, indent=4)

        print(f"\nColeta finalizada! {len(repositories)} repositórios foram salvos em '{output_filename}'.")