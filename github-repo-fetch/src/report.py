def generate_report(repos):
    total = len(repos)
    total_stars = sum(r.get("stargazerCount", 0) for r in repos)
    languages = [r.get("primaryLanguage", {}).get("name") for r in repos if r.get("primaryLanguage")]
    top_languages = {lang: languages.count(lang) for lang in set(languages)}

    report = f"""
RELATÓRIO INICIAL DOS REPOSITÓRIOS

Total de repositórios coletados: {total}
Soma total de stars: {total_stars}
Top linguagens por quantidade de repositórios:
{top_languages}

Hipóteses informais:
1. Repositórios com mais stars tendem a ter mais watchers.
2. Linguagens mais populares possuem mais forks em média.
3. Repositórios antigos tendem a ter mais pull requests fechadas.
"""
    print(report)
    with open("data/report.txt", "w", encoding="utf-8") as f:
        f.write(report)
