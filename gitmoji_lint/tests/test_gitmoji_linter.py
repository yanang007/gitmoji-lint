from gitmoji_lint.gitmoji_convention import check_gitmoji_convention


def test_check_gitmoji_convention():
    cases = {}
    cases["""
:sparkles: Add feature

:recycle: Refactor logic
:boom: Deprecated something
""".strip()] = 0

    cases["""
sparkles: Add feature

:recycle: Refactor logic
""".strip()] = 1  # does not start with a gitmoji

    cases["""
:sparklas: Add feature

:recycle: Refactor logic
""".strip()] = 1  # wrong subject gitmoji

    cases["""
:sparkles: Add feature

:what_the_fuck_is_this_gitmoji: Refactor logic
""".strip()] = 1  # wrong subject in message body

    for msg, expected_code in cases.items():
        ret = check_gitmoji_convention(msg)

        assert ret == expected_code
