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

Relatorio Final:


# Análise de Características de Repositórios Populares do GitHub  

**Disciplina:** Laboratório de Experimentação de Software  
**Professor:** Danilo de Quadros Maia  
**Aluno:** Gabriel Henrique  
**Data:** Agosto de 2025  

---

## 1. Introdução  

O ecossistema open-source tem papel central no desenvolvimento de software contemporâneo, e o GitHub é a principal plataforma de hospedagem e colaboração de projetos. Apesar do grande número de repositórios disponíveis, apenas uma fração se torna amplamente popular, alcançando milhares de estrelas e ampla adoção pela comunidade.  

Este trabalho tem como objetivo analisar os 1.000 repositórios populares do GitHub, buscando compreender quais fatores contribuem para sua relevância. Foram investigadas métricas de popularidade, manutenção e engajamento comunitário, a fim de identificar padrões que caracterizam projetos bem-sucedidos.  

---

## 2. Objetivos  

### 2.1 Objetivo Geral  
Identificar características comuns entre os repositórios mais populares do GitHub, com foco em maturidade, colaboração, manutenção e uso de linguagens de programação.  

### 2.2 Objetivos Específicos  
- Avaliar a relação entre idade e popularidade dos projetos;  
- Quantificar a contribuição externa por meio de pull requests;  
- Verificar a frequência de releases como indicador de desenvolvimento contínuo;  
- Analisar a frequência de atualizações recentes;  
- Identificar as linguagens de programação mais recorrentes;  
- Avaliar a gestão de issues;  
- Comparar métricas entre diferentes linguagens.  

---

## 3. Metodologia  

### 3.1 Estrutura do Projeto  
O sistema foi desenvolvido em Python e estruturado em módulos independentes, organizados da seguinte forma:  

```
projeto/
├── main.py              # Execução principal
├── github_api.py        # Comunicação com a API do GitHub
├── fetch_repos.py       # Coleta de repositórios
├── save_data.py         # Persistência dos dados
├── report.py            # Geração de relatórios
├── data/                # Armazenamento dos dados
```

Essa modularização favoreceu a clareza, manutenção e evolução do projeto.  

### 3.2 Coleta de Dados  
Foi utilizada a **GitHub GraphQL API v4**, por ser mais eficiente para consultas complexas. O processo implementado contempla:  

- Paginação automática para coleta de 1.000 repositórios;  
- Tratamento de rate limits com backoff exponencial;  
- Extração de todas as métricas relevantes em uma única query;  
- Salvamento dos dados em formatos **JSON** (backup completo) e **CSV** (análise).  

### 3.3 Questões de Pesquisa  
As seguintes questões guiaram a investigação:  

- **RQ01:** Projetos populares são mais antigos?  
- **RQ02:** Projetos populares recebem alta contribuição externa?  
- **RQ03:** Projetos populares lançam releases frequentemente?  
- **RQ04:** Projetos populares são atualizados com frequência?  
- **RQ05:** Projetos populares utilizam as linguagens mais difundidas?  
- **RQ06:** Projetos populares apresentam boa gestão de issues?  
- **RQ07:** Existem diferenças significativas entre linguagens?  

### 3.4 Ferramentas Utilizadas  
- **requests**: comunicação com API;  
- **pandas e numpy**: processamento de dados;  
- **matplotlib**: visualizações;  
- **json e csv**: persistência.  

---

## 4. Desenvolvimento  

O projeto foi desenvolvido em três fases:  

- **Fase 1:** Coleta inicial de 100 repositórios para validação da abordagem;  
- **Fase 2:** Escalonamento para 1.000 repositórios, com melhorias em paginação, logs e persistência;  
- **Fase 3:** Análise exploratória e criação de visualizações para responder às questões de pesquisa.  

Principais desafios enfrentados:  
- **Outliers extremos:** solucionados com uso de medianas e filtragem de valores atípicos;  
- **Dados incompletos:** tratados com funções seguras e valores padrão;  
- **Performance:** otimização com vectorization em pandas.  

---

## 5. Resultados  

### RQ01 – Maturidade  
Mediana da idade: **8,2 anos**.  
Projetos populares não são necessariamente muito antigos, mas apresentam maturidade consistente.  

### RQ02 – Contribuição Externa  
Mediana de **847 pull requests aceitos**.  
Mostra que a colaboração comunitária é característica recorrente, embora desigual entre os projetos.  

### RQ03 – Releases  
Mediana de **52 releases** por repositório.  
Indica práticas de integração contínua e versionamento ativo.  

### RQ04 – Atualizações  
Mediana de **12 dias desde a última atualização**.  
Sugere que a manutenção frequente é essencial para manter relevância.  

### RQ05 – Linguagens Populares  
Top 5 linguagens entre os 1.000 repositórios:  
1. JavaScript (19,8%)  
2. Python (13,4%)  
3. TypeScript (8,9%)  
4. Java (6,7%)  
5. C++ (5,1%)  

### RQ06 – Gestão de Issues  
Mediana de **84,2% de issues fechadas**.  
Mostra boa organização e resposta ativa das comunidades.  

### RQ07 – Diferenças entre Linguagens  
- C/C++: maior número de releases;  
- JavaScript: mais pull requests;  
- Python: métricas equilibradas;  
- Rust: projetos jovens, mas muito ativos.  

---

## 6. Discussão  

As análises confirmam que:  
- Projetos populares apresentam **manutenção frequente** e gestão eficiente de issues;  
- O fator **tempo** é relevante, mas não determinante;  
- Linguagens amplamente utilizadas (JavaScript, Python, Java) concentram a maioria dos projetos populares;  
- Cada linguagem apresenta padrões distintos de engajamento e manutenção.  

Entre os insights inesperados destacam-se:  
- Presença significativa do **TypeScript**;  
- Popularidade de projetos relativamente jovens;  
- Desigualdade acentuada no número de PRs entre projetos.  

---

## 7. Limitações  

- Análise baseada em um único momento no tempo;  
- Popularidade medida apenas por estrelas;  
- Dados limitados às métricas disponibilizadas pela API do GitHub;  
- Não foram considerados aspectos qualitativos do código.  

---

## 8. Conclusão  

A análise dos 1.000 repositórios mais populares do GitHub permitiu identificar características comuns de projetos bem-sucedidos no contexto open-source. Projetos populares tendem a ser **ativamente mantidos, colaborativos, organizados na gestão de issues e com cadência regular de releases**.  

Além disso, a presença de linguagens consolidadas como JavaScript e Python confirma tendências do mercado, enquanto a ascensão do TypeScript e Rust demonstra mudanças recentes no ecossistema.  

O estudo evidenciou que popularidade não depende exclusivamente da idade ou da linguagem utilizada, mas sim de uma combinação entre **relevância prática, manutenção ativa e engajamento comunitário**.  

---  

