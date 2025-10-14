# Contributing Guide

We’re excited that you’re interested in contributing to this project!  
Please follow these steps to ensure a smooth review process.



## 🧩 1. Open an Issue

Before starting any work, **open an issue** describing the feature or fix you want to implement.

**Issue Title:**  
Use a short, clear title that describes the feature.

**Issue Description:**  
- Feature name  
- Short explanation of what it does  
- Outline of how you plan to implement it

Example:

```markdown
# Title: Add user profile picture upload

## Description:
- Implement profile picture upload using Django FileField.

Store images in media/pfp/ and display them in user profile templates.
```


## 🌱 2. Fork and Branch

After your issue is created:

1. **Fork** this repository.
2. Create a **new branch** using the following format:

```text
issue-<issue-number>-<short-feature-summary>
```

Example:
```text
issue-42-add-profile-pictures
```

## 🧹 3. Follow PEP 8

All Python code **must follow [PEP 8](https://peps.python.org/pep-0008/)**.  
Use `flake8` or `black` before committing:

```bash
.venv/bin/black .
.venv/bin/flake8 --exclude .venv/
```
## 🧪 4. Testing

All tests should be written using **pytest**.

Add your test files under the `/tests/` directory, organized by app -> feature.  
Make sure all tests pass before submitting your pull request.

Run tests:
```bash
.venv/bin/pytest
```
You can also run with detailed output:
```bash
.venv/bin/pytest -v
```

All tests must pass before you submit a pull request.

## 📬 5. Submit a Pull Request

Once your branch is ready:

1. Push your branch to your fork.

2. Open a Pull Request (PR) to the main repository.

**PR Title:**
Match the issue title.

**PR Description:**
Reference the issue (e.g. Closes #42) and summarize your changes.

## ✅ 6. Review Process

All pull requests will be reviewed for:

- Code quality (PEP 8 compliance)

- Readability and maintainability

- Proper documentation and tests

When requested changes are addressed, your PR will be merged.

---

**Thanks for helping make this project better! 💙**