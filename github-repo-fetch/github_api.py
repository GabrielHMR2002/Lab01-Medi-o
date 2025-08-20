import requests
import time

GITHUB_API_URL = "https://api.github.com/graphql"
GITHUB_TOKEN = "TOKEN"
HEADERS = {
    "Authorization": f"bearer {GITHUB_TOKEN}",
    "Content-Type": "application/json",
}

def run_query(query, variables, max_retries=5):
    for attempt in range(1, max_retries + 1):
        try:
            resp = requests.post(GITHUB_API_URL, json={"query": query, "variables": variables}, headers=HEADERS, timeout=30)
            print(f"HTTP Status: {resp.status_code}")
            if resp.status_code == 200:
                result = resp.json()
                if "errors" in result:
                    print(f"Erro da API: {result['errors']}")
                    raise Exception(result['errors'])
                return result
            elif resp.status_code in [502, 504]:
                print(f"[WARN] HTTP {resp.status_code} - tentativa {attempt}/{max_retries}")
        except requests.exceptions.RequestException as e:
            print(f"[WARN] Timeout ou erro: {e} - tentativa {attempt}/{max_retries}")
        time.sleep(2 ** attempt)
    raise Exception(f"A query falhou após {max_retries} tentativas.")
