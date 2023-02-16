Gitmoji-lint
================

**Gitmoji-lint** is a linter that checks the gitmojis in your commit messages.


### Using Gitmoji-lint with pre-commit
Add this to your `.pre-commit-config.yaml`

```yaml
-   repo: https://github.com/yanang007/gitmoji-lint
    rev: ''  # Use the sha you want to point at
    hooks:
    -   id: gitmoji-lint
```

### Using Gitmoji-lint CLI

#### Installation

Gitmoji-lint can be installed with `pip`.

```shell
pip install gitmoji-lint
```

#### CLI

Checks the last three commits.

```shell
gitmoji-lint --head 3
```

Checks new commits in the branch.

```shell
gitmoji-lint --rev-range origin/HEAD..HEAD
```

Checks the file (to use as `commit-msg` hook).

```shell
gitmoji-lint --commit-msg-file .git/COMMIT_EDITMSG
```

Checks all the commits in current branch.

```shell
gitmoji-lint --all
```

Checks a given string.

```shell
gitmoji-lint --message 'This will fail.'
```
