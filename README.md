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
