from datetime import datetime
from statistics import median
from collections import Counter

def generate_report(repos):
    total = len(repos)
    # RQ01: idade
    today = datetime.utcnow()
    ages = [(today - datetime.fromisoformat(r["createdAt"].replace("Z",""))).days for r in repos]
    median_age = median(ages)

    # RQ02: pull requests aceitas
    prs_merged = [r.get("pullRequestsMerged", {}).get("totalCount", 0) if isinstance(r.get("pullRequestsMerged"), dict) else r.get("pullRequestsMerged",0) for r in repos]
    median_prs_merged = median(prs_merged)

    # RQ03: releases
    releases = [r.get("releases", {}).get("totalCount", 0) if isinstance(r.get("releases"), dict) else r.get("releasesCount",0) for r in repos]
    median_releases = median(releases)

    # RQ04: tempo desde última atualização
    updates = [(today - datetime.fromisoformat(r["pushedAt"].replace("Z",""))).days for r in repos]
    median_update_days = median(updates)

    # RQ05: linguagens
    languages = [r.get("primaryLanguage", {}).get("name") if isinstance(r.get("primaryLanguage"), dict) else r.get("primaryLanguage","") for r in repos]
    language_count = Counter([l for l in languages if l])

    # RQ06: percentual de issues fechadas
    issues_open = [r.get("issues", {}).get("totalCount",0) if isinstance(r.get("issues"), dict) else r.get("issuesOpen",0) for r in repos]
    issues_closed = [r.get("issuesClosed", {}).get("totalCount",0) if isinstance(r.get("issuesClosed"), dict) else r.get("issuesClosed",0) for r in repos]
    ratios_issues_closed = [closed/(closed+open_) if (closed+open_)>0 else 0 for open_, closed in zip(issues_open, issues_closed)]
    median_issues_closed_ratio = median(ratios_issues_closed)

    report = f"""
RELATÓRIO DOS REPOSITÓRIOS

RQ01: Sistemas populares são maduros/antigos?
- Idade mediana (dias): {median_age}

RQ02: Sistemas populares recebem muita contribuição externa?
- Pull requests aceitas medianas: {median_prs_merged}

RQ03: Sistemas populares lançam releases com frequência?
- Releases medianos: {median_releases}

RQ04: Sistemas populares são atualizados com frequência?
- Dias desde última atualização (mediana): {median_update_days}

RQ05: Sistemas populares são escritos nas linguagens mais populares?
- Contagem por linguagem: {language_count}

RQ06: Sistemas populares possuem um alto percentual de issues fechadas?
- Percentual mediano de issues fechadas: {median_issues_closed_ratio:.2f}

Hipóteses informais:
1. Repositórios com mais stars tendem a ser mais antigos.
2. Repositórios com mais PRs aceitas são mais populares.
3. Linguagens populares possuem mais repositórios e forks.
4. Repositórios com atualizações recentes estão ativos e mantidos.
5. A maioria das issues é fechada.
"""
    print(report)
    with open("data/report.txt","w",encoding="utf-8") as f:
        f.write(report)
