# Here's how we find the run matching head_sha with our commit
# GET /repos/{owner}/{repo}/actions/workflows/{workflow_id}/runs
# workflow_id = build.yml
# Response:
# {
#   "total_count": 1,
#   "workflow_runs": [
#     {
#       "id": 30433642,
#       "name": "Build",
#       "node_id": "MDEyOldvcmtmbG93IFJ1bjI2OTI4OQ==",
#       "head_branch": "master",
#       "head_sha": "acb5820ced9479c074f688cc328bf03f341a511d",
#       "run_number": 562,
#       "event": "push",
#       "status": "queued",
#       "conclusion": null,
#       "workflow_id": 159038,
#       "url": "https://api.github.com/repos/octo-org/octo-repo/actions/runs/30433642",
#       "html_url": "https://github.com/octo-org/octo-repo/actions/runs/30433642",
#       "pull_requests": [],
#       "created_at": "2020-01-22T19:33:08Z",
#       "updated_at": "2020-01-22T19:33:08Z",
#       "jobs_url": "https://api.github.com/repos/octo-org/octo-repo/actions/runs/30433642/jobs",
#       "logs_url": "https://api.github.com/repos/octo-org/octo-repo/actions/runs/30433642/logs",
#       "check_suite_url": "https://api.github.com/repos/octo-org/octo-repo/check-suites/414944374",
#       "artifacts_url": "https://api.github.com/repos/octo-org/octo-repo/actions/runs/30433642/artifacts",
#       "cancel_url": "https://api.github.com/repos/octo-org/octo-repo/actions/runs/30433642/cancel",
#       "rerun_url": "https://api.github.com/repos/octo-org/octo-repo/actions/runs/30433642/rerun",
#       "workflow_url": "https://api.github.com/repos/octo-org/octo-repo/actions/workflows/159038",
#       "head_commit": {
#         "id": "acb5820ced9479c074f688cc328bf03f341a511d",
#         "tree_id": "d23f6eedb1e1b9610bbc754ddb5197bfe7271223",
#         "message": "Create linter.yaml",
#         "timestamp": "2020-01-22T19:33:05Z",
#         "author": {
#           "name": "Octo Cat",
#           "email": "octocat@github.com"
#         },
#         "committer": {
#           "name": "GitHub",
#           "email": "noreply@github.com"
#         }
#       },
#       "repository": {
#         "id": 1296269,
#         "node_id": "MDEwOlJlcG9zaXRvcnkxMjk2MjY5",
#         "name": "Hello-World",
#         "full_name": "octocat/Hello-World",
#         "owner": {
#           "login": "octocat",
#           "id": 1,
#           "node_id": "MDQ6VXNlcjE=",
#           "avatar_url": "https://github.com/images/error/octocat_happy.gif",
#           "gravatar_id": "",
#           "url": "https://api.github.com/users/octocat",
#           "html_url": "https://github.com/octocat",
#           "followers_url": "https://api.github.com/users/octocat/followers",
#           "following_url": "https://api.github.com/users/octocat/following{/other_user}",
#           "gists_url": "https://api.github.com/users/octocat/gists{/gist_id}",
#           "starred_url": "https://api.github.com/users/octocat/starred{/owner}{/repo}",
#           "subscriptions_url": "https://api.github.com/users/octocat/subscriptions",
#           "organizations_url": "https://api.github.com/users/octocat/orgs",
#           "repos_url": "https://api.github.com/users/octocat/repos",
#           "events_url": "https://api.github.com/users/octocat/events{/privacy}",
#           "received_events_url": "https://api.github.com/users/octocat/received_events",
#           "type": "User",
#           "site_admin": false
#         },
#         "private": false,
#         "html_url": "https://github.com/octocat/Hello-World",
#         "description": "This your first repo!",
#         "fork": false,
#         "url": "https://api.github.com/repos/octocat/Hello-World",
#         "archive_url": "https://api.github.com/repos/octocat/Hello-World/{archive_format}{/ref}",
#         "assignees_url": "https://api.github.com/repos/octocat/Hello-World/assignees{/user}",
#         "blobs_url": "https://api.github.com/repos/octocat/Hello-World/git/blobs{/sha}",
#         "branches_url": "https://api.github.com/repos/octocat/Hello-World/branches{/branch}",
#         "collaborators_url": "https://api.github.com/repos/octocat/Hello-World/collaborators{/collaborator}",
#         "comments_url": "https://api.github.com/repos/octocat/Hello-World/comments{/number}",
#         "commits_url": "https://api.github.com/repos/octocat/Hello-World/commits{/sha}",
#         "compare_url": "https://api.github.com/repos/octocat/Hello-World/compare/{base}...{head}",
#         "contents_url": "https://api.github.com/repos/octocat/Hello-World/contents/{+path}",
#         "contributors_url": "https://api.github.com/repos/octocat/Hello-World/contributors",
#         "deployments_url": "https://api.github.com/repos/octocat/Hello-World/deployments",
#         "downloads_url": "https://api.github.com/repos/octocat/Hello-World/downloads",
#         "events_url": "https://api.github.com/repos/octocat/Hello-World/events",
#         "forks_url": "https://api.github.com/repos/octocat/Hello-World/forks",
#         "git_commits_url": "https://api.github.com/repos/octocat/Hello-World/git/commits{/sha}",
#         "git_refs_url": "https://api.github.com/repos/octocat/Hello-World/git/refs{/sha}",
#         "git_tags_url": "https://api.github.com/repos/octocat/Hello-World/git/tags{/sha}",
#         "git_url": "git:github.com/octocat/Hello-World.git",
#         "issue_comment_url": "https://api.github.com/repos/octocat/Hello-World/issues/comments{/number}",
#         "issue_events_url": "https://api.github.com/repos/octocat/Hello-World/issues/events{/number}",
#         "issues_url": "https://api.github.com/repos/octocat/Hello-World/issues{/number}",
#         "keys_url": "https://api.github.com/repos/octocat/Hello-World/keys{/key_id}",
#         "labels_url": "https://api.github.com/repos/octocat/Hello-World/labels{/name}",
#         "languages_url": "https://api.github.com/repos/octocat/Hello-World/languages",
#         "merges_url": "https://api.github.com/repos/octocat/Hello-World/merges",
#         "milestones_url": "https://api.github.com/repos/octocat/Hello-World/milestones{/number}",
#         "notifications_url": "https://api.github.com/repos/octocat/Hello-World/notifications{?since,all,participating}",
#         "pulls_url": "https://api.github.com/repos/octocat/Hello-World/pulls{/number}",
#         "releases_url": "https://api.github.com/repos/octocat/Hello-World/releases{/id}",
#         "ssh_url": "git@github.com:octocat/Hello-World.git",
#         "stargazers_url": "https://api.github.com/repos/octocat/Hello-World/stargazers",
#         "statuses_url": "https://api.github.com/repos/octocat/Hello-World/statuses/{sha}",
#         "subscribers_url": "https://api.github.com/repos/octocat/Hello-World/subscribers",
#         "subscription_url": "https://api.github.com/repos/octocat/Hello-World/subscription",
#         "tags_url": "https://api.github.com/repos/octocat/Hello-World/tags",
#         "teams_url": "https://api.github.com/repos/octocat/Hello-World/teams",
#         "trees_url": "https://api.github.com/repos/octocat/Hello-World/git/trees{/sha}",
#         "hooks_url": "http://api.github.com/repos/octocat/Hello-World/hooks"
#       },
#       "head_repository": {
#         "id": 217723378,
#         "node_id": "MDEwOlJlcG9zaXRvcnkyMTc3MjMzNzg=",
#         "name": "octo-repo",
#         "full_name": "octo-org/octo-repo",
#         "private": true,
#         "owner": {
#           "login": "octocat",
#           "id": 1,
#           "node_id": "MDQ6VXNlcjE=",
#           "avatar_url": "https://github.com/images/error/octocat_happy.gif",
#           "gravatar_id": "",
#           "url": "https://api.github.com/users/octocat",
#           "html_url": "https://github.com/octocat",
#           "followers_url": "https://api.github.com/users/octocat/followers",
#           "following_url": "https://api.github.com/users/octocat/following{/other_user}",
#           "gists_url": "https://api.github.com/users/octocat/gists{/gist_id}",
#           "starred_url": "https://api.github.com/users/octocat/starred{/owner}{/repo}",
#           "subscriptions_url": "https://api.github.com/users/octocat/subscriptions",
#           "organizations_url": "https://api.github.com/users/octocat/orgs",
#           "repos_url": "https://api.github.com/users/octocat/repos",
#           "events_url": "https://api.github.com/users/octocat/events{/privacy}",
#           "received_events_url": "https://api.github.com/users/octocat/received_events",
#           "type": "User",
#           "site_admin": false
#         },
#         "html_url": "https://github.com/octo-org/octo-repo",
#         "description": null,
#         "fork": false,
#         "url": "https://api.github.com/repos/octo-org/octo-repo",
#         "forks_url": "https://api.github.com/repos/octo-org/octo-repo/forks",
#         "keys_url": "https://api.github.com/repos/octo-org/octo-repo/keys{/key_id}",
#         "collaborators_url": "https://api.github.com/repos/octo-org/octo-repo/collaborators{/collaborator}",
#         "teams_url": "https://api.github.com/repos/octo-org/octo-repo/teams",
#         "hooks_url": "https://api.github.com/repos/octo-org/octo-repo/hooks",
#         "issue_events_url": "https://api.github.com/repos/octo-org/octo-repo/issues/events{/number}",
#         "events_url": "https://api.github.com/repos/octo-org/octo-repo/events",
#         "assignees_url": "https://api.github.com/repos/octo-org/octo-repo/assignees{/user}",
#         "branches_url": "https://api.github.com/repos/octo-org/octo-repo/branches{/branch}",
#         "tags_url": "https://api.github.com/repos/octo-org/octo-repo/tags",
#         "blobs_url": "https://api.github.com/repos/octo-org/octo-repo/git/blobs{/sha}",
#         "git_tags_url": "https://api.github.com/repos/octo-org/octo-repo/git/tags{/sha}",
#         "git_refs_url": "https://api.github.com/repos/octo-org/octo-repo/git/refs{/sha}",
#         "trees_url": "https://api.github.com/repos/octo-org/octo-repo/git/trees{/sha}",
#         "statuses_url": "https://api.github.com/repos/octo-org/octo-repo/statuses/{sha}",
#         "languages_url": "https://api.github.com/repos/octo-org/octo-repo/languages",
#         "stargazers_url": "https://api.github.com/repos/octo-org/octo-repo/stargazers",
#         "contributors_url": "https://api.github.com/repos/octo-org/octo-repo/contributors",
#         "subscribers_url": "https://api.github.com/repos/octo-org/octo-repo/subscribers",
#         "subscription_url": "https://api.github.com/repos/octo-org/octo-repo/subscription",
#         "commits_url": "https://api.github.com/repos/octo-org/octo-repo/commits{/sha}",
#         "git_commits_url": "https://api.github.com/repos/octo-org/octo-repo/git/commits{/sha}",
#         "comments_url": "https://api.github.com/repos/octo-org/octo-repo/comments{/number}",
#         "issue_comment_url": "https://api.github.com/repos/octo-org/octo-repo/issues/comments{/number}",
#         "contents_url": "https://api.github.com/repos/octo-org/octo-repo/contents/{+path}",
#         "compare_url": "https://api.github.com/repos/octo-org/octo-repo/compare/{base}...{head}",
#         "merges_url": "https://api.github.com/repos/octo-org/octo-repo/merges",
#         "archive_url": "https://api.github.com/repos/octo-org/octo-repo/{archive_format}{/ref}",
#         "downloads_url": "https://api.github.com/repos/octo-org/octo-repo/downloads",
#         "issues_url": "https://api.github.com/repos/octo-org/octo-repo/issues{/number}",
#         "pulls_url": "https://api.github.com/repos/octo-org/octo-repo/pulls{/number}",
#         "milestones_url": "https://api.github.com/repos/octo-org/octo-repo/milestones{/number}",
#         "notifications_url": "https://api.github.com/repos/octo-org/octo-repo/notifications{?since,all,participating}",
#         "labels_url": "https://api.github.com/repos/octo-org/octo-repo/labels{/name}",
#         "releases_url": "https://api.github.com/repos/octo-org/octo-repo/releases{/id}",
#         "deployments_url": "https://api.github.com/repos/octo-org/octo-repo/deployments"
#       }
#     }
#   ]
# }

# Once we know which run our commit is associated with:
# GET /repos/{owner}/{repo}/actions/runs/{run_id}
# Response:
# {
#   "id": 30433642,
#   "name": "Build",
#   "node_id": "MDEyOldvcmtmbG93IFJ1bjI2OTI4OQ==",
#   "head_branch": "master",
#   "head_sha": "acb5820ced9479c074f688cc328bf03f341a511d",
#   "run_number": 562,
#   "event": "push",
#   "status": "queued",
#   "conclusion": null,
#   "workflow_id": 159038,
#   "url": "https://api.github.com/repos/octo-org/octo-repo/actions/runs/30433642",
#   "html_url": "https://github.com/octo-org/octo-repo/actions/runs/30433642",
#   "pull_requests": [],
#   "created_at": "2020-01-22T19:33:08Z",
#   "updated_at": "2020-01-22T19:33:08Z",
#   "jobs_url": "https://api.github.com/repos/octo-org/octo-repo/actions/runs/30433642/jobs",
#   "logs_url": "https://api.github.com/repos/octo-org/octo-repo/actions/runs/30433642/logs",
#   "check_suite_url": "https://api.github.com/repos/octo-org/octo-repo/check-suites/414944374",
#   "artifacts_url": "https://api.github.com/repos/octo-org/octo-repo/actions/runs/30433642/artifacts",
#   "cancel_url": "https://api.github.com/repos/octo-org/octo-repo/actions/runs/30433642/cancel",
#   "rerun_url": "https://api.github.com/repos/octo-org/octo-repo/actions/runs/30433642/rerun",
#   "workflow_url": "https://api.github.com/repos/octo-org/octo-repo/actions/workflows/159038",
#   "head_commit": {
#     "id": "acb5820ced9479c074f688cc328bf03f341a511d",
#     "tree_id": "d23f6eedb1e1b9610bbc754ddb5197bfe7271223",
#     "message": "Create linter.yaml",
#     "timestamp": "2020-01-22T19:33:05Z",
#     "author": {
#       "name": "Octo Cat",
#       "email": "octocat@github.com"
#     },
#     "committer": {
#       "name": "GitHub",
#       "email": "noreply@github.com"
#     }
#   },
#   "repository": {
#     "id": 1296269,
#     "node_id": "MDEwOlJlcG9zaXRvcnkxMjk2MjY5",
#     "name": "Hello-World",
#     "full_name": "octocat/Hello-World",
#     "owner": {
#       "login": "octocat",
#       "id": 1,
#       "node_id": "MDQ6VXNlcjE=",
#       "avatar_url": "https://github.com/images/error/octocat_happy.gif",
#       "gravatar_id": "",
#       "url": "https://api.github.com/users/octocat",
#       "html_url": "https://github.com/octocat",
#       "followers_url": "https://api.github.com/users/octocat/followers",
#       "following_url": "https://api.github.com/users/octocat/following{/other_user}",
#       "gists_url": "https://api.github.com/users/octocat/gists{/gist_id}",
#       "starred_url": "https://api.github.com/users/octocat/starred{/owner}{/repo}",
#       "subscriptions_url": "https://api.github.com/users/octocat/subscriptions",
#       "organizations_url": "https://api.github.com/users/octocat/orgs",
#       "repos_url": "https://api.github.com/users/octocat/repos",
#       "events_url": "https://api.github.com/users/octocat/events{/privacy}",
#       "received_events_url": "https://api.github.com/users/octocat/received_events",
#       "type": "User",
#       "site_admin": false
#     },
#     "private": false,
#     "html_url": "https://github.com/octocat/Hello-World",
#     "description": "This your first repo!",
#     "fork": false,
#     "url": "https://api.github.com/repos/octocat/Hello-World",
#     "archive_url": "https://api.github.com/repos/octocat/Hello-World/{archive_format}{/ref}",
#     "assignees_url": "https://api.github.com/repos/octocat/Hello-World/assignees{/user}",
#     "blobs_url": "https://api.github.com/repos/octocat/Hello-World/git/blobs{/sha}",
#     "branches_url": "https://api.github.com/repos/octocat/Hello-World/branches{/branch}",
#     "collaborators_url": "https://api.github.com/repos/octocat/Hello-World/collaborators{/collaborator}",
#     "comments_url": "https://api.github.com/repos/octocat/Hello-World/comments{/number}",
#     "commits_url": "https://api.github.com/repos/octocat/Hello-World/commits{/sha}",
#     "compare_url": "https://api.github.com/repos/octocat/Hello-World/compare/{base}...{head}",
#     "contents_url": "https://api.github.com/repos/octocat/Hello-World/contents/{+path}",
#     "contributors_url": "https://api.github.com/repos/octocat/Hello-World/contributors",
#     "deployments_url": "https://api.github.com/repos/octocat/Hello-World/deployments",
#     "downloads_url": "https://api.github.com/repos/octocat/Hello-World/downloads",
#     "events_url": "https://api.github.com/repos/octocat/Hello-World/events",
#     "forks_url": "https://api.github.com/repos/octocat/Hello-World/forks",
#     "git_commits_url": "https://api.github.com/repos/octocat/Hello-World/git/commits{/sha}",
#     "git_refs_url": "https://api.github.com/repos/octocat/Hello-World/git/refs{/sha}",
#     "git_tags_url": "https://api.github.com/repos/octocat/Hello-World/git/tags{/sha}",
#     "git_url": "git:github.com/octocat/Hello-World.git",
#     "issue_comment_url": "https://api.github.com/repos/octocat/Hello-World/issues/comments{/number}",
#     "issue_events_url": "https://api.github.com/repos/octocat/Hello-World/issues/events{/number}",
#     "issues_url": "https://api.github.com/repos/octocat/Hello-World/issues{/number}",
#     "keys_url": "https://api.github.com/repos/octocat/Hello-World/keys{/key_id}",
#     "labels_url": "https://api.github.com/repos/octocat/Hello-World/labels{/name}",
#     "languages_url": "https://api.github.com/repos/octocat/Hello-World/languages",
#     "merges_url": "https://api.github.com/repos/octocat/Hello-World/merges",
#     "milestones_url": "https://api.github.com/repos/octocat/Hello-World/milestones{/number}",
#     "notifications_url": "https://api.github.com/repos/octocat/Hello-World/notifications{?since,all,participating}",
#     "pulls_url": "https://api.github.com/repos/octocat/Hello-World/pulls{/number}",
#     "releases_url": "https://api.github.com/repos/octocat/Hello-World/releases{/id}",
#     "ssh_url": "git@github.com:octocat/Hello-World.git",
#     "stargazers_url": "https://api.github.com/repos/octocat/Hello-World/stargazers",
#     "statuses_url": "https://api.github.com/repos/octocat/Hello-World/statuses/{sha}",
#     "subscribers_url": "https://api.github.com/repos/octocat/Hello-World/subscribers",
#     "subscription_url": "https://api.github.com/repos/octocat/Hello-World/subscription",
#     "tags_url": "https://api.github.com/repos/octocat/Hello-World/tags",
#     "teams_url": "https://api.github.com/repos/octocat/Hello-World/teams",
#     "trees_url": "https://api.github.com/repos/octocat/Hello-World/git/trees{/sha}",
#     "hooks_url": "http://api.github.com/repos/octocat/Hello-World/hooks"
#   },
#   "head_repository": {
#     "id": 217723378,
#     "node_id": "MDEwOlJlcG9zaXRvcnkyMTc3MjMzNzg=",
#     "name": "octo-repo",
#     "full_name": "octo-org/octo-repo",
#     "private": true,
#     "owner": {
#       "login": "octocat",
#       "id": 1,
#       "node_id": "MDQ6VXNlcjE=",
#       "avatar_url": "https://github.com/images/error/octocat_happy.gif",
#       "gravatar_id": "",
#       "url": "https://api.github.com/users/octocat",
#       "html_url": "https://github.com/octocat",
#       "followers_url": "https://api.github.com/users/octocat/followers",
#       "following_url": "https://api.github.com/users/octocat/following{/other_user}",
#       "gists_url": "https://api.github.com/users/octocat/gists{/gist_id}",
#       "starred_url": "https://api.github.com/users/octocat/starred{/owner}{/repo}",
#       "subscriptions_url": "https://api.github.com/users/octocat/subscriptions",
#       "organizations_url": "https://api.github.com/users/octocat/orgs",
#       "repos_url": "https://api.github.com/users/octocat/repos",
#       "events_url": "https://api.github.com/users/octocat/events{/privacy}",
#       "received_events_url": "https://api.github.com/users/octocat/received_events",
#       "type": "User",
#       "site_admin": false
#     },
#     "html_url": "https://github.com/octo-org/octo-repo",
#     "description": null,
#     "fork": false,
#     "url": "https://api.github.com/repos/octo-org/octo-repo",
#     "forks_url": "https://api.github.com/repos/octo-org/octo-repo/forks",
#     "keys_url": "https://api.github.com/repos/octo-org/octo-repo/keys{/key_id}",
#     "collaborators_url": "https://api.github.com/repos/octo-org/octo-repo/collaborators{/collaborator}",
#     "teams_url": "https://api.github.com/repos/octo-org/octo-repo/teams",
#     "hooks_url": "https://api.github.com/repos/octo-org/octo-repo/hooks",
#     "issue_events_url": "https://api.github.com/repos/octo-org/octo-repo/issues/events{/number}",
#     "events_url": "https://api.github.com/repos/octo-org/octo-repo/events",
#     "assignees_url": "https://api.github.com/repos/octo-org/octo-repo/assignees{/user}",
#     "branches_url": "https://api.github.com/repos/octo-org/octo-repo/branches{/branch}",
#     "tags_url": "https://api.github.com/repos/octo-org/octo-repo/tags",
#     "blobs_url": "https://api.github.com/repos/octo-org/octo-repo/git/blobs{/sha}",
#     "git_tags_url": "https://api.github.com/repos/octo-org/octo-repo/git/tags{/sha}",
#     "git_refs_url": "https://api.github.com/repos/octo-org/octo-repo/git/refs{/sha}",
#     "trees_url": "https://api.github.com/repos/octo-org/octo-repo/git/trees{/sha}",
#     "statuses_url": "https://api.github.com/repos/octo-org/octo-repo/statuses/{sha}",
#     "languages_url": "https://api.github.com/repos/octo-org/octo-repo/languages",
#     "stargazers_url": "https://api.github.com/repos/octo-org/octo-repo/stargazers",
#     "contributors_url": "https://api.github.com/repos/octo-org/octo-repo/contributors",
#     "subscribers_url": "https://api.github.com/repos/octo-org/octo-repo/subscribers",
#     "subscription_url": "https://api.github.com/repos/octo-org/octo-repo/subscription",
#     "commits_url": "https://api.github.com/repos/octo-org/octo-repo/commits{/sha}",
#     "git_commits_url": "https://api.github.com/repos/octo-org/octo-repo/git/commits{/sha}",
#     "comments_url": "https://api.github.com/repos/octo-org/octo-repo/comments{/number}",
#     "issue_comment_url": "https://api.github.com/repos/octo-org/octo-repo/issues/comments{/number}",
#     "contents_url": "https://api.github.com/repos/octo-org/octo-repo/contents/{+path}",
#     "compare_url": "https://api.github.com/repos/octo-org/octo-repo/compare/{base}...{head}",
#     "merges_url": "https://api.github.com/repos/octo-org/octo-repo/merges",
#     "archive_url": "https://api.github.com/repos/octo-org/octo-repo/{archive_format}{/ref}",
#     "downloads_url": "https://api.github.com/repos/octo-org/octo-repo/downloads",
#     "issues_url": "https://api.github.com/repos/octo-org/octo-repo/issues{/number}",
#     "pulls_url": "https://api.github.com/repos/octo-org/octo-repo/pulls{/number}",
#     "milestones_url": "https://api.github.com/repos/octo-org/octo-repo/milestones{/number}",
#     "notifications_url": "https://api.github.com/repos/octo-org/octo-repo/notifications{?since,all,participating}",
#     "labels_url": "https://api.github.com/repos/octo-org/octo-repo/labels{/name}",
#     "releases_url": "https://api.github.com/repos/octo-org/octo-repo/releases{/id}",
#     "deployments_url": "https://api.github.com/repos/octo-org/octo-repo/deployments"
#   }
# }

# Authentication:
# curl --header "Authorization: token {token}"

# Using cURL to do API Requests
# curl \
#       -H "Accept: application/vnd.github.v3+json" \
#       https://api.github.com/{URL}

import json
import sys

import requests


def pprint(*args):
    pp_args = []
    for data in args:
        if isinstance(data, str):
            pp_args.append(data)
            continue
        pp_args.append(json.dumps(data, indent=2))
    print(" ".join(pp_args))


def get_headers(github_token):
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json",
    }
    return headers


def get_repo_base(repo_owner, repo_name):
    api_base = "https://api.github.com"
    repo_base = f"{api_base}/repos/{repo_owner}/{repo_name}"
    return repo_base


def get_workflow_runs(repo_owner, repo_name, github_token, workflow_id):
    headers = get_headers(github_token)
    repo_base = get_repo_base(repo_owner, repo_name)
    response = requests.get(
        f"{repo_base}/actions/workflows/{workflow_id}/runs",
        headers=headers,
    )
    return response.json()


def get_workflow_run(repo_owner, repo_name, github_token, workflow_id, run_id):
    headers = get_headers(github_token)
    repo_base = get_repo_base(repo_owner, repo_name)
    response = requests.get(
        f"{repo_base}/actions/runs/{run_id}",
        headers=headers,
    )
    return response.json()


def find_run(head_sha, plugin_config, run_id=None):
    repo_owner=plugin_config["repo_owner"]
    repo_name=plugin_config["repo_name"]
    github_token=plugin_config["github_token"]
    workflow_id = plugin_config.get("workflow_id", "build.yml")

    if run_id is not None:
        run = get_workflow_run(
            repo_owner, repo_name, github_token, workflow_id, run_id
        )
        pprint("Run:", run)
        return run

    workflow = get_workflow_runs(
        repo_owner, repo_name, github_token, workflow_id
    )
    runs = workflow["workflow_runs"]

    match = None
    for run in runs:
        if head_sha != run["head_sha"]:
            continue
        # if we find there are neve multiple commit-runs we can break after
        # the first match we come across
        if match is None:
            match = run
        else:
            print(f"Warning: Multiple matches for head_sha {head_sha}")
            break

    pprint("Workflow runs match:",  match)
    return match


if __name__ == "__main__":
    head_sha = sys.argv[1]
    run = find_run(head_sha)
    assert run, f"Run not found for head_sha {head_sha}"

    preamble = f"Action run for head_sha {head_sha}"
    status = run["status"]
    conclusion = run["conclusion"]
    if status == "completed" and conclusion == "success":
        print(f"{preamble} has successfully completed!")
    else:
        print(f"{preamble} status: {status} conclusion: {conclusion}")
