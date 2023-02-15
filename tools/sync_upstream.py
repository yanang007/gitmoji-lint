import argparse
import warnings
from pathlib import Path
from urllib.request import urlopen
import json


upstream = 'carloscuesta/gitmoji'
upstream_file_path = 'packages/gitmojis/src/gitmojis.json'
web_api = "https://gitmoji.dev/api/gitmojis"
upstream_repo_file_api = f"https://raw.githubusercontent.com/{upstream}/master/{upstream_file_path}"
upstream_repo_commit_api = f"https://api.github.com/repos/{upstream}/commits?path=/{upstream_file_path}"


def update_gitmoji_data():
    local_file = Path('./gitmoji_lint/data/gitmojis.json')
    local = local_file.read_text(encoding='utf-8')

    api = urlopen(web_api)
    remote = api.read().decode(encoding='utf-8')
    remote = json.loads(remote)
    remote_content = json.dumps(remote['gitmojis'], ensure_ascii=False, indent=2)

    remote = json.dumps(remote, ensure_ascii=False, indent=2)

    if hash(local) != hash(remote):
        upstream_repo = urlopen(upstream_repo_file_api)
        upstream = upstream_repo.read().decode(encoding='utf-8')
        upstream = json.loads(upstream)
        upstream_content = json.dumps(upstream['gitmojis'], ensure_ascii=False, indent=2)

        # ensure to sync with both repo and official api.
        if upstream_content == remote_content:
            commits_api = urlopen(upstream_repo_commit_api)
            commits = commits_api.read().decode(encoding='utf-8')
            commits = json.loads(commits)
            if len(commits) > 0:
                latest = commits[0]
                sha = latest['sha']
                local_file.write_text(remote, encoding='utf-8')
                print(sha)
        else:
            warnings.warn('Web-hosted gitmojis.json is updated but different from repository.')
            print('!')
    else:
        warnings.warn('Data file gitmojis.json is up to date.')
        print('?')


def format_subject(sha):
    short_sha = sha[:7]
    print(f':bento: Update gitmojis.json (carloscuesta/gitmoji@{short_sha})')


def format_body(sha):
    print(f'https://github.com/carloscuesta/gitmoji/commit/{sha}')


def format_pr_body(sha):
    commit_link = f'https://github.com/{upstream}/commit/{sha}'
    print(f"Automatically update gitmojis.json"
          f" with upstream [web api]({web_api})"
          f" and [repository change]({commit_link}).")


def format_commit_message(sha):
    format_subject(sha)
    print()
    format_body(sha)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--format-subject",
        type=str,
        help="Format commit subject from specified sha.",
    )

    parser.add_argument(
        "--format-body",
        type=str,
        help="Format commit body from specified sha.",
    )

    parser.add_argument(
        "--format-msg",
        type=str,
        help="Format complete commit message from specified sha.",
    )

    parser.add_argument(
        "--format-pr-body",
        type=str,
        help="Format pull request body from specified sha.",
    )

    parser.add_argument(
        "--fetch-upstream",
        action='store_true',
        default=False,
        help="Fetch upstream repository.",
    )

    args = parser.parse_args()

    if args.format_subject:
        format_subject(args.format_subject)
    elif args.format_body:
        format_body(args.format_body)
    elif args.format_msg:
        format_commit_message(args.format_msg)
    elif args.format_pr_body:
        format_pr_body(args.format_pr_body)
    elif args.fetch_upstream:
        update_gitmoji_data()
    else:
        warnings.warn('No operation selected.')


if __name__ == '__main__':
    main()
