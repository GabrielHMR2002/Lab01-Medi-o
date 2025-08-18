Perfeito! Aqui está o seu `README.md` completo, corrigido e pronto para GitHub:

````markdown
# 📦 Coleta Robusta de Repositórios do GitHub  

Este projeto realiza uma **consulta GraphQL na API do GitHub** para coletar dados completos de até **100 repositórios populares** (ordenados por número de estrelas).  

O script foi implementado de forma **robusta**, incluindo tratamento de erros, retries automáticos e pausas entre requisições para evitar bloqueios.  

---

## 🚀 Funcionalidades  
- Consulta até **100 repositórios** via GraphQL.  
- Coleta informações detalhadas como:  
  - Nome e URL  
  - Datas de criação e último push  
  - Estrelas ⭐, forks 🍴, watchers 👀  
  - Issues abertas/fechadas  
  - Pull requests (abertos, fechados e mesclados)  
  - Releases publicadas  
  - Linguagem principal  
  - Licença  
  - Tópicos associados  
  - Uso em disco (diskUsage)  
- Retry automático em caso de falha ou timeout.  
- Salva os resultados em um arquivo `.json`.  

---

## ⚙️ Requisitos  

- Python 3.8+  
- Bibliotecas:  
  ```bash
  pip install requests
````

---

## 🔑 Configuração do Token

1. Gere um **Personal Access Token (PAT)** no GitHub:

   * Acesse [https://github.com/settings/tokens](https://github.com/settings/tokens)
   * Crie um token com permissão **`read:public_repo`**

2. Abra o arquivo `fetch_repos_robusto.py` e substitua a linha:

   ```python
   GITHUB_TOKEN = "SEU_TOKEN_AQUI"
   ```

   pelo seu token pessoal.

⚠️ **Importante:** nunca commite seu token no GitHub.

---

## 🏃‍♂️ Execução

Durante a execução, o script exibirá logs como:

```text
Iniciando a coleta de dados de 100 repositórios (versão robusta)...
Buscando 30 repositórios... (já coletados: 0)
Buscando 30 repositórios... (já coletados: 30)
Buscando 30 repositórios... (já coletados: 60)
Buscando 10 repositórios... (já coletados: 90)

Coleta finalizada! 100 repositórios foram salvos em 'repositories_data_completo.json'.
```

---

## 📂 Saída

<img width="1918" height="1078" alt="image" src="https://github.com/user-attachments/assets/ee9df3ad-4650-418e-b355-bf4ac965e68a" />

Os dados serão salvos em:

```
repositories_data_completo.json
```

Formato JSON com todos os repositórios coletados, por exemplo:

```json
{
  "nameWithOwner": "freeCodeCamp/freeCodeCamp",
  "url": "https://github.com/freeCodeCamp/freeCodeCamp",
  "createdAt": "2014-12-24T17:49:19Z",
  "pushedAt": "2025-08-17T15:50:38Z",
  "description": "freeCodeCamp.org's open-source codebase and curriculum. Learn math, programming, and computer science for free.",
  "stargazerCount": 425921,
  "forkCount": 41219,
  "watchers": {
    "totalCount": 8587
  },
  "issues": {
    "totalCount": 198
  },
  "issuesClosed": {
    "totalCount": 19621
  },
  "pullRequests": {
    "totalCount": 112
  },
  "pullRequestsMerged": {
    "totalCount": 25699
  },
  "pullRequestsClosed": {
    "totalCount": 15338
  },
  "releases": {
    "totalCount": 0
  },
  "primaryLanguage": {
    "name": "TypeScript"
  },
  "diskUsage": 510767,
  "licenseInfo": {
    "name": "BSD 3-Clause \"New\" or \"Revised\" License",
    "spdxId": "BSD-3-Clause"
  },
  "topics": {
    "nodes": [
      {"topic": {"name": "learn-to-code"}},
      {"topic": {"name": "nonprofits"}},
      {"topic": {"name": "programming"}},
      {"topic": {"name": "nodejs"}},
      {"topic": {"name": "react"}},
      {"topic": {"name": "d3"}},
      {"topic": {"name": "careers"}},
      {"topic": {"name": "education"}},
      {"topic": {"name": "teachers"}},
      {"topic": {"name": "javascript"}}
    ]
  }
}
```

---

## 📌 Observações

* A API GraphQL do GitHub possui limites de **rate limit**. O script adiciona **pausas automáticas** para evitar bloqueios.
* Caso precise coletar **mais de 100 repositórios**, ajuste o parâmetro `total_repos_to_fetch`.
* Esse script é parte da **Sprint 1** da tarefa, com foco na coleta inicial de dados.
