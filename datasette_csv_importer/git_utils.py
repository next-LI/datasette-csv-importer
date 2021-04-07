# from datetime import datetime
import os

from git import Repo


def get_repo_remote(repo_owner, repo_name, github_user, github_token):
    return f"https://{github_user}:{github_token}@github.com/{repo_owner}/{repo_name}"


def write_csv_to_repo(filename, data, plugin_config):
    url = get_repo_remote(
        plugin_config["repo_owner"],
        plugin_config["repo_name"],
        plugin_config["github_user"],
        plugin_config["github_token"]
    )
    repo_dir = plugin_config.get("repo_dir", "/tmp/nextli-datasette")
    repo_path = os.path.abspath(repo_dir)
    print(f"Repo Path: {repo_path}")

    if not os.path.exists(repo_path):
        os.makedirs(repo_path, exist_ok=True)

    repo = Repo.init(repo_path, mkdir=True)

    if not len(repo.remotes):
        print(f"Setting up origin => {url}")
        repo.remotes.append(repo.create_remote("origin", url))

    assert not repo.bare

    print("Fetching origin")
    repo.remotes.origin.fetch()
    print("Pulling origin")
    repo.remotes.origin.pull("main")
    print("Checking out main")
    repo.git.checkout("main")
    print("Hard resetting head")
    repo.git.reset("origin/main", hard=True)

    # now = datetime.now().strftime("%Y-%m-%d-%H%M")
    # branch_name = f"{filename}-{now}"
    # repo.git.checkout(b=branch_name)
    # print(f"Checked out new branch: {branch_name}")

    assert not repo.is_dirty()

    # newpath = os.path.join(repo_path, "config")
    # os.makedirs(newpath)

    print("Writing CSV")
    newfilepath = os.path.join(repo_path, "csvs", filename)
    print(f"Writing file {newfilepath}")
    with open(newfilepath, "w") as f:
        f.write(data.decode("utf-8"))

    # if not repo.is_dirty() and not len(repo.untracked_files):
    #     print("No changes! Exiting.")
    #     return

    print("We have unstaged changes, creating commit")
    repo.index.add([newfilepath])
    commit = repo.index.commit(f"Git importer: {filename}")
    repo.git.push("origin", "main")
    print("Commit SHA", commit.hexsha)
    return commit.hexsha


if __name__ == "__main__":
    head_sha = write_csv_to_repo("test.csv", "name,species\nbrandon,human\nkai,human")
    print(f"HEAD SHA: {head_sha}")
