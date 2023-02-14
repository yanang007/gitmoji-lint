from pathlib import Path
from urllib.request import urlopen
import json


def update_gitmoji_data():
    local_file = Path('./gitmoji_lint/data/gitmojis.json')
    local = local_file.read_text(encoding='utf-8')

    api = urlopen("https://gitmoji.dev/api/gitmojis")
    remote = api.read().decode(encoding='utf-8')
    remote = json.loads(remote)
    remote_content = json.dumps(remote['gitmojis'], ensure_ascii=False, indent=2)

    remote = json.dumps(remote, ensure_ascii=False, indent=2)

    if hash(local) != hash(remote):
        upstream_repo = urlopen(
            "https://raw.githubusercontent.com/carloscuesta/gitmoji/master/packages/gitmojis/src/gitmojis.json")
        upstream = upstream_repo.read().decode(encoding='utf-8')
        upstream = json.loads(upstream)
        upstream_content = json.dumps(upstream['gitmojis'], ensure_ascii=False, indent=2)

        if upstream_content == remote_content:
            # ensure to sync with both repo and official api.
            commits_api = urlopen(
                "https://api.github.com/repos/carloscuesta/gitmoji/commits?path=/packages/gitmojis/src/gitmojis.json")
            commits = commits_api.read().decode(encoding='utf-8')
            commits = json.loads(commits)
            if len(commits) > 0:
                latest = commits[0]
                sha = latest['sha']
                short_sha = sha[:7]
                link = latest['html_url']

                local_file.write_text(remote, encoding='utf-8')
                print(f':bento: Update gitmojis.json (carloscuesta/gitmoji@{short_sha})\n\n{link}')
    else:
        print('Data file gitmojis.json is up to date.')


def main():
    update_gitmoji_data()


if __name__ == '__main__':
    main()
