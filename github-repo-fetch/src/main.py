from fetch_repos import fetch_repositories
from save_data import save_csv, save_json
from report import generate_report
import pandas as pd

if __name__ == "__main__":
    repos = fetch_repositories(total_repos=50, per_page=10)
    save_csv(repos, "data/repositories.csv")
    save_json(repos, "data/repositories.json")
    generate_report(repos)