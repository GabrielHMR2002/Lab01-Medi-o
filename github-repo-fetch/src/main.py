from fetch_repos import fetch_repositories
from save_data import save_csv, save_json
from report import generate_report

if __name__ == "__main__":
    repos = fetch_repositories(total_repos=20, per_page=5)
    save_csv(repos, "data/repositories.csv")
    save_json(repos, "data/repositories.json")
    generate_report(repos)
