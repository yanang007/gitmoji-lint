import sys
import re
import json
import importlib.resources as pkg_resources

from gitmoji_lint import data


def check_gitmoji_convention(msg):
    gitmojis = json.loads(pkg_resources.read_text(data, 'gitmojis.json'))['gitmojis']

    valid_gitmojis = set((gitmoji['code'] for gitmoji in gitmojis))

    gitmoji_code_match = re.compile(r'(:\w*?:)(.*)').match(msg)

    if gitmoji_code_match is None:
        print('Commit subject does not starts with a gitmoji.')
        return 1

    if gitmoji_code_match[1] not in valid_gitmojis:
        print(f'Commit subject starts with an invalid gitmoji "{gitmoji_code_match[1]}".')
        return 2

    gitmoji_code_match = re.compile(r'(:\w*?:)').findall(msg)
    for match in gitmoji_code_match:
        if match not in valid_gitmojis:
            print(f'Commit message body contains invalid gitmoji "{match}".')
            return 3

    return 0


def main():
    from pathlib import Path
    msg = Path(sys.argv[1]).read_text(encoding='utf-8')

    exit(check_gitmoji_convention(msg))


if __name__ == '__main__':
    main()
