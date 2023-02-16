from click.testing import CliRunner

from gitmoji_lint.cli import cli


def test_default():
    runner = CliRunner()
    ret = runner.invoke(cli, [])

    print(ret.output)
    assert ret.exit_code == 0


def test_head():
    runner = CliRunner()
    ret = runner.invoke(cli, ['--head', '2'])

    print(ret.output)
    assert ret.exit_code == 0


def test_commit_msg_file():
    from pathlib import Path
    from os import fspath

    runner = CliRunner()
    with runner.isolated_filesystem():
        tmp_msg = Path('./COMMIT_EDITMSG')
        tmp_msg.write_text("sparkles: Failed!")

        ret = runner.invoke(cli, ['--commit-msg-file', fspath(tmp_msg)])

    print(ret.output)
    assert ret.exit_code == 1
