# Contributing Guide

We’re excited that you’re interested in contributing to LibreCourse!  
This guide explains how to set up your environment, follow coding standards, and submit contributions properly.

<br>

## 🌱 1. Set up your development environment

1. **Clone the repository:**

```bash
git clone https://github.com/your-username/LibreCourse.git
cd LibreCourse
```

2. **Run the setup script** (Linux/Ubuntu/Arch compatible):

```bash
python3 dev_jumpstart.py
```

This will:

* Create a `.venv` virtual environment (if missing)
* Install all Python dependencies from `requirements-dev.txt`
* Install Node.js and npm dependencies
* Set up TailwindCSS and PostCSS
* Start the Django development server and Tailwind watcher


**⚠️ On some systems, you may need:**

 ```bash
 sudo apt install python3-venv
 ```

### 💡 Notes

* If you see warnings from `npm`, they can usually be ignored unless they prevent installation.
* On first run, you may need to enter your system password for `sudo` commands.  

* After setup, you can re-run:

```bash
python3 dev_jumpstart.py
```
This will **not reinstall everything from scratch**. Instead, it will:

* Check if system dependencies (`curl`, `node`, `npm`, etc.) are present and up to date.
* Check if Python dependencies in `requirements-dev.txt` have changed and install any missing ones.
* Check if Node dependencies (`tailwindcss`, `postcss`, etc.) need updating.
* Start/Restart the **development environment** (Django server + Tailwind watcher).

3. **Configure environment variables**:
   Create a `.env` file in the project root with at least:

```
SECRET_KEY=your-secret-key
DATABASE_URL=postgres://username:password@localhost:5432/librecourse  # optional
```
<br>

## 🧩 2. Open an Issue

Before starting work, **open an issue** describing the feature or fix.

**Issue Title:**
Use a short, clear title.

**Issue Description:**

* Feature name
* Short explanation of what it does
* Outline of your implementation plan

Example:

```markdown
# Title: Add user profile picture upload

## Description:
- Implement profile picture upload using Django FileField
- Store images in media/pfp/ and display them in user profiles
```
<br>

## 🌿 3. Fork & Branch

1. **Fork** this repository.
2. **Create a new branch** using:

```text
issue-<issue-number>-<short-feature-summary>
```

Example:

```text
issue-42-add-profile-pictures
```
<br>

## 🧹 4. Code Style (PEP 8)

All Python code **must follow [PEP 8](https://peps.python.org/pep-0008/)**.

Inside the project virtual environment (`.venv`), run:

```bash
.venv/bin/black .
.venv/bin/flake8 --exclude .venv/
```
**Fix all formatting issues before committing.**

<br>

## 📦 5. Adding Dependencies

If your new feature requires additional Python packages, **add them to `requirements.txt`**, **not** `requirements-dev.txt`.

* `requirements.txt` → dependencies needed for the application to run
* `requirements-dev.txt` → only for development tools (e.g., linters, testing frameworks)

After adding a new dependency, update your virtual environment:

```bash
.venv/bin/pip install -r requirements.txt
```

This ensures that everyone running the project will automatically have the required packages for new features.

<br>

## 🧪 6. Testing with Pytest

All tests must use **pytest** and live under `/tests/` organized by app → feature.

Run tests from project root (inside `.venv`):

```bash
.venv/bin/pytest
```

Verbose output:

```bash
.venv/bin/pytest -v
```

**⚠️ If you get import errors:**

* Ensure all `tests/` folders have `__init__.py`
* Remove `.pyc` files and `__pycache__`
* Avoid running pytest from inside subfolders

<br>

## 📬 7. Making Changes

1. Work in your **feature branch**, never `main`:

```bash
git checkout -b issue-<number>-<short-feature-summary>
```

2. Make your changes and **follow PEP 8 style**.
3. **Test** your changes with pytest.
4. Commit and push:

```bash
git add .
git commit -m "Add: short description of changes"
git push origin issue-<number>-<short-feature-summary>
```

<br>

## 🔄 8. Pull Request

1. Open a **PR** to the main repository.
2. **PR Title:** Match the issue title.
3. **PR Description:** Reference the issue (e.g., `Closes #42`) and summarize changes.

<br>

## ✅ 9. Review Process

All PRs are reviewed for:

* PEP 8 compliance
* Correctness and maintainability
* Documentation updates
* Tests coverage

Once approved and requested changes are made, your PR will be merged.

<br>

## 💡 Notes

* Keep PRs small and focused (one feature/fix per PR)
* Update documentation if needed
* Be respectful and constructive in discussions
* Use the virtual environment `.venv` for all Python commands to avoid conflicts

---

<br>

**Thanks for contributing to LibreCourse! 💙**

