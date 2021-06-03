# from datetime import datetime
import os

from git import Repo


def get_repo_remote(repo_owner, repo_name, github_user, github_token):
    return f"https://{github_user}:{github_token}@github.com/{repo_owner}/{repo_name}"


def save_folder_to_repo(folder_path=None, repo_owner=None, repo_name=None,
                        github_user=None, github_token=None):
    url = get_repo_remote(
        repo_owner, repo_name,
        github_user, github_token
    )
    print(f"Repo Folder Path: {folder_path}")

    repo = Repo.init(folder_path, mkdir=False)

    if not len(repo.remotes):
        print(f"Setting up origin => {url}")
        repo.remotes.append(repo.create_remote("origin", url))
        repo.remotes.origin.pull("main")
        print("Checking out main")
        repo.git.checkout("main")

    print("Adding files to index")
    repo.git.add(all=True)

    if not repo.is_dirty():
        print("Nothing changed, exiting!")
        return

    commit = repo.index.commit(f"CSV importer: autocommit")
    repo.git.push("origin", "main")
    print("Commit SHA", commit.hexsha)

    print("Fetching origin")
    repo.remotes.origin.fetch()
    print("Pulling origin")
    repo.remotes.origin.pull("main")
    # print("Hard resetting head")
    # repo.git.reset("origin/main", hard=True)

    # now = datetime.now().strftime("%Y-%m-%d-%H%M")
    # branch_name = f"{filename}-{now}"
    # repo.git.checkout(b=branch_name)
    # print(f"Checked out new branch: {branch_name}")

    assert not repo.is_dirty()

    # newpath = os.path.join(folder_path, "config")
    # os.makedirs(newpath)

    return commit.hexsha
