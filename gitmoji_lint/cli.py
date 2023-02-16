from __future__ import annotations

from click import option, command

from .gitmoji_convention import check_msg_file, check_rev_range, check_gitmoji_convention


@option("--commit-msg-file", help="A temporal file that contains the commit message to check.")
@option("--rev-range",
        help="A range of git rev to check. e.g, `master..HEAD`, `HEAD`, `HEAD~3..` or `..HEAD~3`.")
@option("--message", help="A temporal file that contains the commit message to check.")
@option("--all", help="Check all the commits in current repository.")
@option("--head", type=int, help="Check the last n commits.")
def main(commit_msg_file=None, rev_range=None, message=None, all=False, head: int | None = None):
    specified_ranges = (commit_msg_file, rev_range, message, all, head)
    n_specified_ranges = len([p for p in specified_ranges if p])

    if n_specified_ranges > 1:
        raise RuntimeError('At most one of'
                           ' [--commit-msg-file, --rev-range, --message, --all, --head]'
                           ' can be specified.')

    if commit_msg_file:
        ret = check_msg_file(commit_msg_file)
    elif rev_range:
        ret = check_rev_range(rev_range)
    elif message:
        ret = check_gitmoji_convention(message)
    elif all:
        ret = check_rev_range(None)
    elif head:
        ret = check_rev_range(head)
    else:
        ret = check_rev_range(1)

    if ret == 0:
        print('Passed.')

    exit(ret)


cli = command()(main)

if __name__ == '__main__':
    cli()
