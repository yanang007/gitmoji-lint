from __future__ import annotations

import re
import json
import importlib.resources as pkg_resources

from gitmoji_lint import data


def check_gitmoji_convention(msg):
    lines = msg.splitlines()
    subject = lines[0]
    lines.pop(0)

    gitmojis = json.loads(pkg_resources.read_text(data, 'gitmojis.json'))['gitmojis']
    valid_gitmojis = set((gitmoji['code'] for gitmoji in gitmojis))

    accepted = True

    # check subject
    gitmoji_code_match = re.compile(r'(:\w*?:)(.*)').match(subject)
    if gitmoji_code_match is None:
        print(f'Commit subject does not starts with a gitmoji: "{subject}"')
        accepted = False
    elif gitmoji_code_match[1] not in valid_gitmojis:
        print(f'Commit subject starts with an invalid gitmoji "{gitmoji_code_match[1]}": "{subject}"')
        accepted = False

    # check body
    for line in lines:
        gitmoji_code_match = re.compile(r'(:\w*?:)').findall(line)
        for match in gitmoji_code_match:
            if match not in valid_gitmojis:
                print(f'Commit message body contains invalid gitmoji "{match}": "{line}"')
                accepted = False

    return 0 if accepted else 1


def check_msg_file(msg_file):
    from pathlib import Path
    msg = Path(msg_file).read_text(encoding='utf-8')
    return check_gitmoji_convention(msg)


def check_rev_range(rev_range: str | int | None):
    from commitizen.git import get_commits

    if isinstance(rev_range, str):
        if '..' in rev_range:
            # fetch commits in the rev_range
            splits = rev_range.split('..')
            assert len(splits) == 2, f'Invalid range syntax `{rev_range}`.'

            splits = [split if len(split) > 0 else None for split in splits]
            commits = get_commits(*splits)
        else:
            # fetch the specified commit
            commits = get_commits(None, rev_range, args='-1')
    elif isinstance(rev_range, int):
        # fetch the last n commits
        commits = get_commits(None, f'-{rev_range}')
    else:
        commits = get_commits()

    ret = 0
    for commit in commits:
        i_ret = check_gitmoji_convention(commit.title + '\n\n' + commit.body)
        ret = ret if i_ret == 0 else i_ret

    return ret
