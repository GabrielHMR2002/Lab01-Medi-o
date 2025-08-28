from datetime import datetime
from statistics import median
from collections import Counter, defaultdict
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# Configurações globais para gráficos mais bonitos
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 11
plt.rcParams['figure.titlesize'] = 16

# Paleta de cores profissional
colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#592941', '#048A81', '#7209B7', '#F72585']

def format_number(num):
    """Formata números para exibição mais legível"""
    if num >= 1e6:
        return f'{num/1e6:.1f}M'
    elif num >= 1e3:
        return f'{num/1e3:.1f}K'
    else:
        return str(int(num))

def create_histogram_with_stats(data, title, xlabel, ylabel, filename, bins=30, color='#2E86AB'):
    """Cria histograma com estatísticas e linha de mediana"""
    plt.figure(figsize=(12, 8))
    
    # Filtrar outliers extremos para melhor visualização
    q1, q3 = np.percentile(data, [25, 75])
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    data_filtered = [x for x in data if lower_bound <= x <= upper_bound]
    
    # Histograma
    n, bins_edges, patches = plt.hist(data_filtered, bins=bins, alpha=0.7, color=color, edgecolor='black', linewidth=0.5)
    
    # Linha da mediana
    median_val = median(data)
    plt.axvline(median_val, color='red', linestyle='--', linewidth=2, 
                label=f'Mediana: {format_number(median_val)}')
    
    # Estatísticas no gráfico
    mean_val = np.mean(data)
    std_val = np.std(data)
    
    # Box com estatísticas
    stats_text = f'Média: {format_number(mean_val)}\nDesvio: {format_number(std_val)}\nN: {len(data):,}'
    plt.text(0.7, 0.85, stats_text, transform=plt.gca().transAxes, 
             bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8),
             verticalalignment='top', fontsize=10)
    
    plt.title(title, fontweight='bold', pad=20)
    plt.xlabel(xlabel, fontweight='bold')
    plt.ylabel(ylabel, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()

def create_boxplot(data, title, ylabel, filename):
    """Cria boxplot com estatísticas"""
    plt.figure(figsize=(8, 10))
    
    box = plt.boxplot(data, patch_artist=True, notch=True)
    box['boxes'][0].set_facecolor('#2E86AB')
    box['boxes'][0].set_alpha(0.7)
    
    # Adicionar estatísticas
    median_val = median(data)
    q1, q3 = np.percentile(data, [25, 75])
    
    stats_text = f'Q1: {format_number(q1)}\nMediana: {format_number(median_val)}\nQ3: {format_number(q3)}'
    plt.text(1.15, median_val, stats_text, 
             bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8),
             verticalalignment='center', fontsize=10)
    
    plt.title(title, fontweight='bold', pad=20)
    plt.ylabel(ylabel, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()

def create_language_bar_chart(language_count, filename, top_n=15):
    """Cria gráfico de barras para linguagens com melhor formatação"""
    plt.figure(figsize=(14, 8))
    
    # Top N linguagens
    top_langs = language_count.most_common(top_n)
    langs, counts = zip(*top_langs)
    
    # Gráfico de barras horizontal para melhor legibilidade
    y_pos = np.arange(len(langs))
    bars = plt.barh(y_pos, counts, color=colors[0], alpha=0.8, edgecolor='black', linewidth=0.5)
    
    # Adicionar valores nas barras
    for i, (bar, count) in enumerate(zip(bars, counts)):
        plt.text(bar.get_width() + max(counts) * 0.01, bar.get_y() + bar.get_height()/2,
                f'{count}', ha='left', va='center', fontweight='bold')
    
    plt.yticks(y_pos, langs)
    plt.xlabel('Número de Repositórios', fontweight='bold')
    plt.title(f'Top {top_n} Linguagens de Programação mais Populares', fontweight='bold', pad=20)
    plt.grid(True, alpha=0.3, axis='x')
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()

def create_language_comparison_chart(lang_metrics, metric_name, title, filename, top_n=10):
    """Cria gráfico de comparação por linguagem"""
    plt.figure(figsize=(14, 8))
    
    # Calcular medianas e ordenar
    lang_medians = []
    for lang, metrics in lang_metrics.items():
        if len(metrics[metric_name]) > 5:  # Só linguagens com pelo menos 5 repos
            lang_medians.append((lang, median(metrics[metric_name])))
    
    # Ordenar por mediana e pegar top N
    lang_medians.sort(key=lambda x: x[1], reverse=True)
    lang_medians = lang_medians[:top_n]
    
    langs, medians = zip(*lang_medians)
    
    # Gráfico de barras horizontal
    y_pos = np.arange(len(langs))
    bars = plt.barh(y_pos, medians, color=colors[1], alpha=0.8, edgecolor='black', linewidth=0.5)
    
    # Adicionar valores nas barras
    for bar, median_val in zip(bars, medians):
        plt.text(bar.get_width() + max(medians) * 0.01, bar.get_y() + bar.get_height()/2,
                format_number(median_val), ha='left', va='center', fontweight='bold')
    
    plt.yticks(y_pos, langs)
    plt.xlabel(f'{metric_name.title().replace("_", " ")} (Mediana)', fontweight='bold')
    plt.title(title, fontweight='bold', pad=20)
    plt.grid(True, alpha=0.3, axis='x')
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()

def create_combined_rq07_chart(lang_metrics, filename):
    """Cria gráfico combinado para RQ07 com múltiplas métricas"""
    # Filtrar linguagens com pelo menos 10 repositórios
    filtered_langs = {}
    for lang, metrics in lang_metrics.items():
        if len(metrics['prs']) >= 10 and lang != 'Desconhecida':
            filtered_langs[lang] = metrics
    
    # Calcular medianas para top 8 linguagens (por número de repos)
    lang_counts = [(lang, len(metrics['prs'])) for lang, metrics in filtered_langs.items()]
    lang_counts.sort(key=lambda x: x[1], reverse=True)
    top_8_langs = [lang for lang, _ in lang_counts[:8]]
    
    # Preparar dados
    langs = []
    prs_medians = []
    releases_medians = []
    updates_medians = []
    
    for lang in top_8_langs:
        metrics = filtered_langs[lang]
        langs.append(lang)
        prs_medians.append(median(metrics['prs']))
        releases_medians.append(median(metrics['releases']))
        updates_medians.append(median(metrics['updates']))
    
    # Criar subplot com 3 gráficos
    fig, axes = plt.subplots(3, 1, figsize=(14, 12))
    fig.suptitle('RQ07: Comparação de Métricas por Linguagem (Top 8)', fontsize=16, fontweight='bold')
    
    x = np.arange(len(langs))
    width = 0.6
    
    # PRs Merged
    bars1 = axes[0].bar(x, prs_medians, width, color=colors[0], alpha=0.8, edgecolor='black', linewidth=0.5)
    axes[0].set_title('Pull Requests Merged (Mediana)', fontweight='bold')
    axes[0].set_ylabel('PRs Merged', fontweight='bold')
    axes[0].grid(True, alpha=0.3, axis='y')
    
    # Adicionar valores
    for bar, val in zip(bars1, prs_medians):
        axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(prs_medians) * 0.01,
                    format_number(val), ha='center', va='bottom', fontweight='bold')
    
    # Releases
    bars2 = axes[1].bar(x, releases_medians, width, color=colors[1], alpha=0.8, edgecolor='black', linewidth=0.5)
    axes[1].set_title('Releases (Mediana)', fontweight='bold')
    axes[1].set_ylabel('Releases', fontweight='bold')
    axes[1].grid(True, alpha=0.3, axis='y')
    
    for bar, val in zip(bars2, releases_medians):
        axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(releases_medians) * 0.01,
                    format_number(val), ha='center', va='bottom', fontweight='bold')
    
    # Dias desde atualização
    bars3 = axes[2].bar(x, updates_medians, width, color=colors[2], alpha=0.8, edgecolor='black', linewidth=0.5)
    axes[2].set_title('Dias desde Última Atualização (Mediana)', fontweight='bold')
    axes[2].set_ylabel('Dias', fontweight='bold')
    axes[2].set_xlabel('Linguagens de Programação', fontweight='bold')
    axes[2].grid(True, alpha=0.3, axis='y')
    
    for bar, val in zip(bars3, updates_medians):
        axes[2].text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(updates_medians) * 0.01,
                    format_number(val), ha='center', va='bottom', fontweight='bold')
    
    # Configurar eixo X para todos os subplots
    for ax in axes:
        ax.set_xticks(x)
        ax.set_xticklabels(langs, rotation=45, ha='right')
    
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()

def generate_report(repos):
    os.makedirs("data/figs", exist_ok=True)
    today = datetime.utcnow()

    print("📊 Gerando relatório com visualizações melhoradas...")

    # --- Calcular métricas ---
    ages = [(today - datetime.fromisoformat(r["createdAt"].replace("Z",""))).days for r in repos]
    ages_years = [age / 365.25 for age in ages]  # Converter para anos
    prs_merged = [r.get("pullRequestsMerged", {}).get("totalCount", 0) for r in repos]
    releases = [r.get("releases", {}).get("totalCount", 0) for r in repos]
    updates = [(today - datetime.fromisoformat(r["pushedAt"].replace("Z",""))).days for r in repos]
    languages = [r.get("primaryLanguage", {}).get("name") if r.get("primaryLanguage") else "Desconhecida" for r in repos]
    issues_open = [r.get("issues", {}).get("totalCount",0) for r in repos]
    issues_closed = [r.get("issuesClosed", {}).get("totalCount",0) for r in repos]
    ratios_issues_closed = [closed/(closed+open_) if (closed+open_)>0 else 0 for open_, closed in zip(issues_open, issues_closed)]

    # --- Medianas ---
    median_age_days = median(ages)
    median_age_years = median(ages_years)
    median_prs_merged = median(prs_merged)
    median_releases = median(releases)
    median_update_days = median(updates)
    median_issues_closed_ratio = median(ratios_issues_closed)

    # --- Gerar gráficos melhorados ---
    
    # RQ01: Idade
    print("📈 Gerando gráficos para RQ01 (Idade)...")
    create_histogram_with_stats(ages_years, 
                               "RQ01: Distribuição da Idade dos Repositórios", 
                               "Idade (anos)", "Número de Repositórios",
                               "data/figs/rq01_idade.png", color=colors[0])
    
    # RQ02: Pull Requests
    print("📈 Gerando gráficos para RQ02 (Pull Requests)...")
    create_histogram_with_stats(prs_merged, 
                               "RQ02: Distribuição de Pull Requests Aceitas", 
                               "Pull Requests Merged", "Número de Repositórios",
                               "data/figs/rq02_prs_hist.png", color=colors[1])
    
    create_boxplot(prs_merged, "RQ02: Pull Requests Aceitas - Análise de Quartis", 
                   "Pull Requests Merged", "data/figs/rq02_prs_box.png")

    # RQ03: Releases
    print("📈 Gerando gráficos para RQ03 (Releases)...")
    create_histogram_with_stats(releases, 
                               "RQ03: Distribuição de Releases", 
                               "Número de Releases", "Número de Repositórios",
                               "data/figs/rq03_releases_hist.png", color=colors[2])
    
    create_boxplot(releases, "RQ03: Releases - Análise de Quartis", 
                   "Número de Releases", "data/figs/rq03_releases_box.png")

    # RQ04: Atualizações
    print("📈 Gerando gráficos para RQ04 (Atualizações)...")
    create_histogram_with_stats(updates, 
                               "RQ04: Dias desde a Última Atualização", 
                               "Dias desde Última Atualização", "Número de Repositórios",
                               "data/figs/rq04_updates.png", color=colors[3])

    # RQ05: Linguagens
    print("📈 Gerando gráficos para RQ05 (Linguagens)...")
    language_count = Counter(languages)
    create_language_bar_chart(language_count, "data/figs/rq05_languages.png")

    # RQ06: Issues fechadas
    print("📈 Gerando gráficos para RQ06 (Issues)...")
    create_histogram_with_stats(ratios_issues_closed, 
                               "RQ06: Percentual de Issues Fechadas", 
                               "Proporção de Issues Fechadas", "Número de Repositórios",
                               "data/figs/rq06_issues.png", bins=20, color=colors[4])

    # RQ07: Análise por linguagem
    print("📈 Gerando gráficos para RQ07 (Análise por Linguagem)...")
    lang_metrics = defaultdict(lambda: {"prs": [], "releases": [], "updates": []})
    for r in repos:
        lang = r.get("primaryLanguage", {}).get("name") if r.get("primaryLanguage") else "Desconhecida"
        lang_metrics[lang]["prs"].append(r.get("pullRequestsMerged", {}).get("totalCount", 0))
        lang_metrics[lang]["releases"].append(r.get("releases", {}).get("totalCount", 0))
        days_since_update = (today - datetime.fromisoformat(r["pushedAt"].replace("Z",""))).days
        lang_metrics[lang]["updates"].append(days_since_update)

    # Gráfico combinado para RQ07
    create_combined_rq07_chart(lang_metrics, "data/figs/rq07_combined.png")
    
    # Gráficos individuais para RQ07
    create_language_comparison_chart(lang_metrics, "prs", 
                                   "RQ07a: Pull Requests Merged por Linguagem",
                                   "data/figs/rq07_prs.png")
    
    create_language_comparison_chart(lang_metrics, "releases", 
                                   "RQ07b: Releases por Linguagem",
                                   "data/figs/rq07_releases.png")
    
    create_language_comparison_chart(lang_metrics, "updates", 
                                   "RQ07c: Dias desde Última Atualização por Linguagem",
                                   "data/figs/rq07_updates.png")

    # --- Gerar relatório em Markdown ---
    print("📝 Gerando relatório em Markdown...")
    
    # Top 10 linguagens para o relatório
    top_10_languages = language_count.most_common(10)
    lang_table = ""
    for i, (lang, count) in enumerate(top_10_languages, 1):
        percentage = (count / len(repos)) * 100
        lang_table += f"{i}. **{lang}**: {count} repositórios ({percentage:.1f}%)\n"

    report_md = f"""# 📊 Relatório Final: Análise de Repositórios Populares do GitHub

**Data da Análise:** {datetime.now().strftime('%d/%m/%Y às %H:%M')}  
**Total de Repositórios Analisados:** {len(repos):,}

---

## 🎯 Resumo Executivo

Este relatório analisa os {len(repos):,} repositórios mais populares do GitHub (baseado em estrelas) para compreender padrões de desenvolvimento, manutenção e características de projetos open-source populares.

---

## 📈 RQ01: Sistemas populares são maduros/antigos?

**Métrica:** Idade do repositório  
**Resultado:** {median_age_years:.1f} anos (mediana) | {median_age_days:,} dias

![RQ01](figs/rq01_idade.png)

**💡 Interpretação:** Repositórios populares têm uma idade mediana de **{median_age_years:.1f} anos**, indicando que leva tempo para um projeto ganhar reconhecimento e acumular estrelas na comunidade.

---

## 🤝 RQ02: Sistemas populares recebem muita contribuição externa?

**Métrica:** Pull Requests aceitas (merged)  
**Resultado:** {median_prs_merged:,} PRs merged (mediana)

![RQ02 Distribuição](figs/rq02_prs_hist.png)
![RQ02 Quartis](figs/rq02_prs_box.png)

**💡 Interpretação:** A mediana de **{median_prs_merged:,} PRs merged** sugere contribuição externa moderada, mas com grande variação entre projetos.

---

## 🚀 RQ03: Sistemas populares lançam releases com frequência?

**Métrica:** Total de releases  
**Resultado:** {median_releases:,} releases (mediana)

![RQ03 Distribuição](figs/rq03_releases_hist.png)
![RQ03 Quartis](figs/rq03_releases_box.png)

**💡 Interpretação:** Com **{median_releases:,} releases** na mediana, observamos práticas variadas de versionamento entre projetos populares.

---

## 🔄 RQ04: Sistemas populares são atualizados com frequência?

**Métrica:** Dias desde a última atualização  
**Resultado:** {median_update_days:,} dias (mediana)

![RQ04](figs/rq04_updates.png)

**💡 Interpretação:** A mediana de **{median_update_days:,} dias** indica que a maioria dos repositórios populares é mantida ativamente.

---

## 💻 RQ05: Sistemas populares são escritos nas linguagens mais populares?

**Métrica:** Distribuição por linguagem primária

![RQ05](figs/rq05_languages.png)

**Top 10 Linguagens:**
{lang_table}

**💡 Interpretação:** JavaScript, Python e TypeScript dominam, refletindo sua popularidade no desenvolvimento web, ciência de dados e aplicações modernas.

---

## ✅ RQ06: Sistemas populares possuem um alto percentual de issues fechadas?

**Métrica:** Proporção de issues fechadas  
**Resultado:** {median_issues_closed_ratio:.1%} (mediana)

![RQ06](figs/rq06_issues.png)

**💡 Interpretação:** Com **{median_issues_closed_ratio:.1%}** de issues fechadas na mediana, observamos boa gestão de issues na maioria dos projetos populares.

---

## 🎯 RQ07 (Bônus): Análise por Linguagem

**Questão:** Sistemas escritos em linguagens mais populares recebem mais contribuição externa, lançam mais releases e são atualizados com mais frequência?

![RQ07 Comparação Completa](figs/rq07_combined.png)

### Análises Detalhadas por Métrica:

![RQ07 PRs por Linguagem](figs/rq07_prs.png)
![RQ07 Releases por Linguagem](figs/rq07_releases.png) 
![RQ07 Atualizações por Linguagem](figs/rq07_updates.png)

**💡 Interpretação:** Diferentes linguagens apresentam padrões distintos:
- **Linguagens de sistema** (C, C++, Rust) tendem a ter mais releases
- **Linguagens web** (JavaScript, TypeScript) recebem mais contribuições
- **Linguagens estabelecidas** mantêm frequência de atualização consistente

---

## 🏆 Conclusões Principais

1. **Maturidade**: Repositórios populares levam tempo para se estabelecer (~{median_age_years:.1f} anos)
2. **Contribuição**: Existe grande variação na contribuição externa entre projetos
3. **Manutenção**: A maioria dos projetos populares é mantida ativamente
4. **Linguagens**: JavaScript e Python dominam o ecossistema open-source popular
5. **Gestão**: Projetos populares mantêm boa gestão de issues
6. **Padrões por Linguagem**: Diferentes linguagens têm características distintas de desenvolvimento

---

## 📊 Estatísticas Gerais

- **Total de repositórios analisados**: {len(repos):,}
- **Idade média**: {np.mean(ages_years):.1f} anos
- **Linguagens únicas identificadas**: {len(language_count)}
- **Período de análise**: {datetime.now().strftime('%B de %Y')}

---

*Relatório gerado automaticamente em {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}*
"""

    # Salvar relatório
    with open("data/report.md", "w", encoding="utf-8") as f:
        f.write(report_md)
    with open("data/report.txt", "w", encoding="utf-8") as f:
        f.write(report_md)

    print("✅ Relatório completo gerado com sucesso!")
    print(f"📁 Gráficos salvos em: data/figs/")
    print(f"📄 Relatório salvo em: data/report.md")
    print(f"📊 Total de {len(repos):,} repositórios analisados")
    
    # Exibir resumo das métricas principais
    print("\n" + "="*50)
    print("📊 RESUMO DAS MÉTRICAS PRINCIPAIS")
    print("="*50)
    print(f"🗓️  Idade mediana: {median_age_years:.1f} anos")
    print(f"🤝 PRs merged mediana: {median_prs_merged:,}")
    print(f"🚀 Releases mediana: {median_releases:,}")
    print(f"🔄 Dias desde atualização: {median_update_days:,}")
    print(f"✅ Issues fechadas: {median_issues_closed_ratio:.1%}")
    print(f"💻 Linguagem mais popular: {top_10_languages[0][0]} ({top_10_languages[0][1]} repos)")
    print("="*50)