BLANK_LINE = "\n\n"

COMMITS = "commits"
REPOSITORY = "repository"
HTML_URL = "html_url"
PRIVATE = "private"
COMPARE_URL = "compare_url"

COMMIT_REF = "ref"
COMMIT_BEFORE = "before"
COMMIT_ID = "id"
COMMIT_URL = "url"
COMMIT_MESSAGE = "message"
COMMIT_TIMESTAMP = "timestamp"
COMMIT_AUTHOR = "author"
COMMIT_AUTHOR_NAME = "name"
COMMIT_AUTHOR_EMAIL = "email"
ADDED = "added"
REMOVED = "removed"
MODIFIED = "modified"
FILES = "files"
ADDITIONS = "additions"
DELETIONS = "deletions"
CHANGES = "changes"

GITHUB_EVENT_DESCRIPTIONS = {
    "commit_comment": "{comment[user][login]} commented on " "{comment[commit_id]} in {repository[full_name]}",
    "create": "{sender[login]} created {ref_type} ({ref}) in " "{repository[full_name]}",
    "delete": "{sender[login]} deleted {ref_type} ({ref}) in " "{repository[full_name]}",
    "deployment": "{sender[login]} deployed {deployment[ref]} to "
                  "{deployment[environment]} in {repository[full_name]}",
    "deployment_status": "deployment of {deployement[ref]} to "
                         "{deployment[environment]} "
                         "{deployment_status[state]} in "
                         "{repository[full_name]}",
    "fork": "{forkee[owner][login]} forked {forkee[name]}",
    "gollum": "{sender[login]} edited wiki pages in {repository[full_name]}",
    "issue_comment": "{sender[login]} commented on issue #{issue[number]} " "in {repository[full_name]}",
    "issues": "{sender[login]} {action} issue #{issue[number]} in " "{repository[full_name]}",
    "member": "{sender[login]} {action} member {member[login]} in " "{repository[full_name]}",
    "membership": "{sender[login]} {action} member {member[login]} to team " "{team[name]} in {repository[full_name]}",
    "page_build": "{sender[login]} built pages in {repository[full_name]}",
    "ping": "ping from {sender[login]}",
    "public": "{sender[login]} publicized {repository[full_name]}",
    "pull_request": "{sender[login]} {action} pull #{pull_request[number]} in " "{repository[full_name]}",
    "pull_request_review": "{sender[login]} {action} {review[state]} "
                           "review on pull #{pull_request[number]} in "
                           "{repository[full_name]}",
    "pull_request_review_comment": "{comment[user][login]} {action} comment "
                                   "on pull #{pull_request[number]} in "
                                   "{repository[full_name]}",
    "push": "{pusher[name]} pushed {ref} in {repository[full_name]}",
    "release": "{release[author][login]} {action} {release[tag_name]} in " "{repository[full_name]}",
    "repository": "{sender[login]} {action} repository " "{repository[full_name]}",
    "status": "{sender[login]} set {sha} status to {state} in " "{repository[full_name]}",
    "team_add": "{sender[login]} added repository {repository[full_name]} to " "team {team[name]}",
    "watch": "{sender[login]} {action} watch in repository " "{repository[full_name]}",
}
