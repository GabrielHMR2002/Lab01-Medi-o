from github_api import run_query

GRAPHQL_QUERY = """
query($queryString: String!, $first: Int, $after: String) {
  search(query: $queryString, type: REPOSITORY, first: $first, after: $after) {
    repositoryCount
    pageInfo { endCursor hasNextPage }
    nodes {
      ... on Repository {
        nameWithOwner
        url
        createdAt
        pushedAt
        description
        stargazerCount
        forkCount
        watchers { totalCount }
        issues(states: OPEN) { totalCount }
        issuesClosed: issues(states: CLOSED) { totalCount }
        pullRequests(states: OPEN) { totalCount }
        pullRequestsMerged: pullRequests(states: MERGED) { totalCount }
        pullRequestsClosed: pullRequests(states: CLOSED) { totalCount }
        releases { totalCount }
        primaryLanguage { name }
        diskUsage
        licenseInfo { name spdxId }
        topics: repositoryTopics(first: 10) { nodes { topic { name } } }
      }
    }
  }
}
"""

def fetch_repositories(total_repos=1000, per_page=50):
    all_repos = []
    after_cursor = None
    query_string = "stars:>5000 sort:stars-desc"

    while len(all_repos) < total_repos:
        batch_size = min(per_page, total_repos - len(all_repos))
        variables = {"queryString": query_string, "first": batch_size, "after": after_cursor}

        print(f"Buscando {batch_size} repositórios... já coletados: {len(all_repos)}")
        result = run_query(GRAPHQL_QUERY, variables)
        nodes = result.get("data", {}).get("search", {}).get("nodes", [])
        all_repos.extend(nodes)

        page_info = result.get("data", {}).get("search", {}).get("pageInfo", {})
        if not page_info.get("hasNextPage"):
            break
        after_cursor = page_info.get("endCursor")
    return all_repos[:total_repos]
