def find_repos_by_topic(client, topic):
    user = client.user
    repos = []
    
    for repo in user.get_repos():
        if topic in repo.get_topics() and repo.permissions.admin:
            repos.append(repo)
    
    return repos
