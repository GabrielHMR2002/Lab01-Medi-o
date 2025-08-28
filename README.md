# GitHub Repo Fetch
---

## Descrição

O **GitHub Repo Fetch** é uma ferramenta em Python que coleta informações detalhadas de repositórios públicos do GitHub usando a API GraphQL.  
Os dados são salvos em **CSV** e **JSON**, e também são processados em um **relatório automático** que responde às **Questões de Pesquisa (RQs)** definidas no laboratório:

- **RQ01:** Idade do repositório  
- **RQ02:** Total de pull requests aceitas  
- **RQ03:** Total de releases  
- **RQ04:** Tempo desde a última atualização  
- **RQ05:** Linguagem primária de cada repositório  
- **RQ06:** Percentual de issues fechadas  

---

## Funcionalidades

- Busca repositórios públicos em lotes configuráveis (até 1000 repositórios)  
- Coleta dados detalhados:
  - Nome do repositório e URL
  - Datas de criação e último push
  - Descrição
  - Estrelas, forks, watchers
  - Issues abertas e fechadas
  - Pull requests abertas, fechadas e mescladas
  - Contagem de releases
  - Linguagem principal
  - Uso de disco
  - Licença (nome e SPDX)
  - Tópicos associados
- Gera arquivos:
  - `CSV` (excel-friendly)
  - `JSON` (para manipulação programática)
- Gera **relatório final com estatísticas (RQs 01–06)**  
- Tratamento automático de campos ausentes (evita erros `NoneType`)

---

## Estrutura do Projeto

```
github-repo-fetch/
├── data/                  # Arquivos gerados (CSV, JSON, relatórios)
├── src/
│   ├── save_data.py       # Funções para salvar CSV e JSON
│   ├── github_api.py      # Consulta à API GraphQL
│   └── report.py          # Geração de relatórios e análise das RQs
├── main.py                # Script principal de execução
└── README.md
```

---

## Requisitos

- **Python 3.10+**
- Bibliotecas Python:
  ```bash
  pip install requests python-dotenv pandas
  ```
- **GitHub Personal Access Token** com permissão de leitura de repositórios públicos

---

## Configuração

1. Crie um arquivo `.env` na raiz do projeto:
   ```
   GITHUB_TOKEN=seu_token_aqui
   ```

2. Certifique-se de que a pasta `data/` existe (ou será criada automaticamente).  

3. Configure o número de repositórios por lote no `main.py`.  

---

## Como Executar

No terminal, execute:

```bash
python main.py
```

O script buscará repositórios e salvará os dados em:

- `data/repositories.csv`
- `data/repositories.json`
- `data/repos_full.csv` (com métricas das RQs)

01 a 06**.

---

## Relatórios

- **CSV compatível com Excel**  
  - Usa **ponto e vírgula `;` como separador**  
  - Codificação **UTF-8 com BOM (`utf-8-sig`)**  
  - Ideal para análises rápidas em planilhas  

- **JSON estruturado**  
  - Mantém a hierarquia dos dados  
  - Útil para uso em scripts, dashboards e integrações  

- **Relatório Automático (RQs)**  
  - Gera estatísticas em formato tabular  
  - Inclui medianas e distribuições  
  - Ajuda a responder diretamente às perguntas do laboratório  

---

## Boas Práticas

- Sempre utilize seu **token de forma segura**, nunca publique em repositórios públicos  
- Para grandes volumes, ajuste o número de repositórios buscados conforme os limites da API  
- Use os relatórios para comparar métricas entre linguagens e projetos  

