from datetime import datetime
from statistics import median
from collections import Counter, defaultdict
import matplotlib.pyplot as plt
import os

def generate_report(repos):
    os.makedirs("data/figs", exist_ok=True)
    today = datetime.utcnow()

    # --- Métricas ---
    ages = [(today - datetime.fromisoformat(r["createdAt"].replace("Z",""))).days for r in repos]
    prs_merged = [r.get("pullRequestsMerged", {}).get("totalCount", 0) for r in repos]
    releases = [r.get("releases", {}).get("totalCount", 0) for r in repos]
    updates = [(today - datetime.fromisoformat(r["pushedAt"].replace("Z",""))).days for r in repos]
    languages = [r.get("primaryLanguage", {}).get("name") if r.get("primaryLanguage") else "Desconhecida" for r in repos]
    issues_open = [r.get("issues", {}).get("totalCount",0) for r in repos]
    issues_closed = [r.get("issuesClosed", {}).get("totalCount",0) for r in repos]
    ratios_issues_closed = [closed/(closed+open_) if (closed+open_)>0 else 0 for open_, closed in zip(issues_open, issues_closed)]

    # --- Medianas ---
    median_age = median(ages)
    median_prs_merged = median(prs_merged)
    median_releases = median(releases)
    median_update_days = median(updates)
    median_issues_closed_ratio = median(ratios_issues_closed)

    # --- Gráficos RQ01 ---
    plt.hist(ages, bins=30)
    plt.title("RQ01 - Distribuição da Idade dos Repositórios (dias)")
    plt.xlabel("Dias")
    plt.ylabel("Frequência")
    plt.savefig("data/figs/rq01_idade.png")
    plt.close()

    # --- Gráficos RQ02 ---
    plt.hist(prs_merged, bins=30)
    plt.title("RQ02 - Distribuição de Pull Requests Aceitas")
    plt.xlabel("Pull Requests Merged")
    plt.ylabel("Frequência")
    plt.savefig("data/figs/rq02_prs_hist.png")
    plt.close()

    plt.boxplot(prs_merged)
    plt.title("RQ02 - Boxplot de Pull Requests Aceitas")
    plt.savefig("data/figs/rq02_prs_box.png")
    plt.close()

    # --- Gráficos RQ03 ---
    plt.hist(releases, bins=30)
    plt.title("RQ03 - Distribuição de Releases")
    plt.xlabel("Releases")
    plt.ylabel("Frequência")
    plt.savefig("data/figs/rq03_releases_hist.png")
    plt.close()

    plt.boxplot(releases)
    plt.title("RQ03 - Boxplot de Releases")
    plt.savefig("data/figs/rq03_releases_box.png")
    plt.close()

    # --- Gráficos RQ04 ---
    plt.hist(updates, bins=30)
    plt.title("RQ04 - Dias desde a Última Atualização")
    plt.xlabel("Dias")
    plt.ylabel("Frequência")
    plt.savefig("data/figs/rq04_updates.png")
    plt.close()

    # --- Gráficos RQ05 ---
    language_count = Counter(languages)
    langs, counts = zip(*language_count.most_common(20))  
    plt.bar(langs, counts)
    plt.xticks(rotation=90)
    plt.title("RQ05 - Linguagens Primárias mais comuns")
    plt.ylabel("Quantidade de Repositórios")
    plt.savefig("data/figs/rq05_languages.png")
    plt.close()

    # --- Gráficos RQ06 ---
    plt.hist(ratios_issues_closed, bins=20, range=(0,1))
    plt.title("RQ06 - Percentual de Issues Fechadas")
    plt.xlabel("Proporção de Issues Fechadas")
    plt.ylabel("Frequência")
    plt.savefig("data/figs/rq06_issues.png")
    plt.close()

    # --- RQ07: análise por linguagem ---
    lang_metrics = defaultdict(lambda: {"prs": [], "releases": [], "updates": []})
    for r in repos:
        lang = r.get("primaryLanguage", {}).get("name") if r.get("primaryLanguage") else "Desconhecida"
        lang_metrics[lang]["prs"].append(r.get("pullRequestsMerged", {}).get("totalCount", 0))
        lang_metrics[lang]["releases"].append(r.get("releases", {}).get("totalCount", 0))
        days_since_update = (today - datetime.fromisoformat(r["pushedAt"].replace("Z",""))).days
        lang_metrics[lang]["updates"].append(days_since_update)

    langs = []
    prs_medians, releases_medians, updates_medians = [], [], []
    for lang, vals in lang_metrics.items():
        langs.append(lang)
        prs_medians.append(median(vals["prs"]) if vals["prs"] else 0)
        releases_medians.append(median(vals["releases"]) if vals["releases"] else 0)
        updates_medians.append(median(vals["updates"]) if vals["updates"] else 0)

    # PRs por linguagem
    plt.bar(langs, prs_medians)
    plt.xticks(rotation=90)
    plt.title("RQ07 - PRs Aceitas (Mediana) por Linguagem")
    plt.savefig("data/figs/rq07_prs.png")
    plt.close()

    # Releases por linguagem
    plt.bar(langs, releases_medians)
    plt.xticks(rotation=90)
    plt.title("RQ07 - Releases (Mediana) por Linguagem")
    plt.savefig("data/figs/rq07_releases.png")
    plt.close()

    # Dias até última atualização por linguagem
    plt.bar(langs, updates_medians)
    plt.xticks(rotation=90)
    plt.title("RQ07 - Dias desde Última Atualização (Mediana) por Linguagem")
    plt.savefig("data/figs/rq07_updates.png")
    plt.close()

    # --- Relatório em Markdown ---
    report_md = f"""
# Relatório dos Repositórios Populares do GitHub

## RQ01: Sistemas populares são maduros/antigos?
- Idade mediana (dias): **{median_age}**
![RQ01](figs/rq01_idade.png)

## RQ02: Sistemas populares recebem muita contribuição externa?
- Pull requests aceitas medianas: **{median_prs_merged}**
![RQ02 Histograma](figs/rq02_prs_hist.png)
![RQ02 Boxplot](figs/rq02_prs_box.png)

## RQ03: Sistemas populares lançam releases com frequência?
- Releases medianos: **{median_releases}**
![RQ03 Histograma](figs/rq03_releases_hist.png)
![RQ03 Boxplot](figs/rq03_releases_box.png)

## RQ04: Sistemas populares são atualizados com frequência?
- Dias desde última atualização (mediana): **{median_update_days}**
![RQ04](figs/rq04_updates.png)

## RQ05: Sistemas populares são escritos nas linguagens mais populares?
- Contagem por linguagem (Top 20 exibidas no gráfico):
![RQ05](figs/rq05_languages.png)

## RQ06: Sistemas populares possuem um alto percentual de issues fechadas?
- Percentual mediano de issues fechadas: **{median_issues_closed_ratio:.2f}**
![RQ06](figs/rq06_issues.png)

---

## RQ07 (Bônus): Análise por linguagem
- Comparação de PRs, Releases e Atualizações por linguagem:
![RQ07 PRs](figs/rq07_prs.png)
![RQ07 Releases](figs/rq07_releases.png)
![RQ07 Updates](figs/rq07_updates.png)

---

# Hipóteses Informais
1. Repositórios com mais stars tendem a ser mais antigos.
2. Repositórios com mais PRs aceitas são mais populares.
3. Linguagens populares possuem mais repositórios e forks.
4. Repositórios com atualizações recentes estão ativos e mantidos.
5. A maioria das issues é fechada.

# Discussão
(Preencher analisando os gráficos e valores obtidos. Exemplo: confirmamos que a maioria dos repositórios populares tem idade elevada, indicando maturidade.)
"""

    with open("data/report.md", "w", encoding="utf-8") as f:
        f.write(report_md)
    with open("data/report.txt", "w", encoding="utf-8") as f:
        f.write(report_md)

    print(" Gráficos e relatório gerados em data/")
