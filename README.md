# 📚 LibreCourse

**LibreCourse** is an open-source Django application for creating, organizing, and collaborating on courses.  
It’s designed to empower educators, learners, and communities by providing a flexible, modern platform to share knowledge freely.  

---

## ✨ Overview

LibreCourse allows anyone to create and manage courses using a clean, intuitive interface.  
Courses are structured into **lessons**, support **Markdown formatting**, and can include **rich media** to engage learners.  

The platform supports both individual educators and collaborative teams, making it ideal for schools, training groups, or open learning communities.  

---

## 🚀 Features

- 🔑 **User accounts**  
  - Personalized usernames with unique display names in the format `username#id`.  
  - Secure authentication system.  

- 📝 **Course creation**  
  - Compose lessons using **Markdown** for text, code, and formatting.  
  - Add images, videos, and external resources to lessons.  
  - Organize lessons into structured courses.  

- 👩‍🏫 **Collaboration**  
  - Invite contributors or co-authors to courses.  

- 👥 **Teacher groups**  
  - Users can join together to form **teacher groups**.  
  - Groups allow educators to publish and manage courses under a **shared pseudonym**, making collaboration seamless and giving the group a unified identity.  

- 🔍 **Discoverability**  
  - Search for courses by title, tags, or author.  
  - Public and private course visibility settings.  

- 🌍 **Open Source**  
  - 100% free and community-driven.  
  - Contributions welcome!  

---

## 🛠️ Upcoming Features

LibreCourse is continuously evolving. Upcoming features include:

* ✅ **Roles & permissions** for fine-grained collaboration.
* ✅ **Learner progress tracking** across lessons and courses.
* ✅ **Student progress dashboards** for teachers

  * View individual progress in real-time or general courses.
  * Track forum participation for better feedback.
* ✅ **Quiz builder** with multiple question types.
* ✅ **Assignments & evaluations** to enhance learning.
* ✅ **Embedded video uploads** beyond external platforms.
* ✅ **Discussion forums** for teachers and learners.
* ✅ **Curriculum support**

  * Bundle related courses under a shared curriculum.
  * Shared forum for discussions between teachers and learners.
  * Course creators can request inclusion in a curriculum.
* ✅ **Moderation & reporting tools** for admins.
* ✅ **Certificates of completion** for finished courses.
* ✅ **Gamification**: badges, points, streaks.
* ✅ **Offline mode** with automatic progress syncing.
* ✅ **Multilingual support** for global communities.
* ✅ **API integrations** with external tools.
* ✅ **Discover & recommendations**

  * Browse courses via a feed or personalized recommendations.

More details in [Dev Roadmap](devroadmap.md)

---

## 🤝 How to Contribute

We welcome contributions of all kinds—bug fixes, new features, documentation improvements, or feedback!
LibreCourse uses the **pull request workflow**. Here’s how you can get involved:

### 🔄 Contribution Workflow

1. **Fork the repository**
   Click the "Fork" button at the top-right of this repo to create your own copy.

2. **Clone your fork**

   ```bash
   git clone https://github.com/your-username/LibreCourse.git
   cd LibreCourse
   ```

3. **Set up the development environment**
   Run the setup script:

   ```bash
   python3 dev_jumpstart.py
   ```

4. **Configure environment variables**
   Create a `.env` file in the project root with at least:

   ```
   SECRET_KEY=your-secret-key
   ```

   Optional (a local SQLite3 fallback is implemented if not set):

   ```
   DATABASE_URL=postgres://username:password@localhost:5432/librecourse
   ```

5. **Create a new branch**
   Always work in a feature branch, not in `main`:

   ```bash
   git checkout -b feature/your-feature-name
   ```

6. **Make your changes**

   * Follow the existing code style and conventions.
   * Keep commits focused and meaningful.

7. **Test your changes**
   Make sure the project runs properly:

   ```bash
   python3 manage.py runserver
   ```

8. **Commit & push**

   ```bash
   git add .
   git commit -m "Add: short description of changes"
   git push origin feature/your-feature-name
   ```

9. **Open a Pull Request (PR)**
   Go to the original repository and open a PR from your branch.

   * Clearly describe what you changed and why.
   * Reference related issues if applicable (e.g., `Fixes #123`).

---

### ✅ Contribution Guidelines

* Keep PRs small and focused—one feature/fix per PR is best.
* Update documentation if your changes affect usage.
* Be respectful and constructive in discussions.
* All contributions are reviewed before merging.

---


## 🤝 Contributions - Project Setup

To make it easier for contributors to set up the project on **Linux (Ubuntu/Debian, Arch-based)** and other supported systems, we provide a single script: `dev_jumpstart.py`.

This script automates the entire environment setup process so you don’t have to manually install or configure dependencies.

### 🔧 What `dev_jumpstart.py` does

Running the script will:

1. **Detect your operating system** (Ubuntu/Debian, Arch Linux, or others).
2. **Ensure system dependencies are installed**  
   - Checks and installs `curl`, `node`, and `npm` if missing or outdated.  
   - On Ubuntu/Debian, uses `apt`; on Arch, uses `pacman`.  
3. **Set up Python environment**  
   - Creates a `.venv` virtual environment (if it doesn’t exist).  
   - Installs/updates all Python dependencies from `requirements.txt`.  
4. **Set up Node.js environment**  
   - Installs or upgrades `node` and `npm` if necessary.  
   - Installs local `npm` dependencies including:  
     - `tailwindcss` (via `@tailwindcss/cli`)  
     - `postcss`  
     - `autoprefixer`  
   - Ensures the TailwindCSS binary is properly linked and accessible.  
5. **Run Django + Tailwind**  
   - Launches the Django development server.  
   - Starts Tailwind in watch mode so CSS updates automatically.  

At the end, you will have a fully working development environment with **Python, Django, TailwindCSS, and all project dependencies configured automatically**.

---

### ▶️ How to use it

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/LibreCourse.git
   cd LibreCourse
2. Run the script:

   ```bash
   python3 dev_jumpstart.py
   ```

   > ⚠️ On some niche Ubuntu systems, you may need to run:
   >
   > ```bash
   > sudo apt install python3-venv
   > ```

3. The script will handle everything:

   * Install missing system packages
   * Set up Python virtualenv
   * Install Node/NPM dependencies
   * Ensure TailwindCSS is installed and ready

---

### 💡 Notes

* If you see warnings from `npm`, they can usually be ignored unless they prevent installation.
* On first run, you may need to enter your system password for `sudo` commands.  

* After setup, you can re-run:

  ```bash
  python3 dev_jumpstart.py

This will **not reinstall everything from scratch**. Instead, it will:

* Check if system dependencies (`curl`, `node`, `npm`, etc.) are present and up to date.
* Check if Python dependencies in `requirements.txt` have changed and install any missing ones.
* Check if Node dependencies (`tailwindcss`, `postcss`, etc.) need updating.
* Start/Restart the **development environment** (Django server + Tailwind watcher).

--- 
 This project is licensed under the GNU Affero General Public License version 3 (AGPLv3). View [LICENSE](LICENSE).
