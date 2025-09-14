#!/usr/bin/env python3
import os
import subprocess
import sys
import platform
import shutil

# -------------------- CONFIG --------------------
PY_DEPS = [
    "django>=4.2,<5.0",
    "django-browser-reload>=0.2",
    "django-widget-tweaks>=1.5",
    "psycopg2-binary>=2.9",
    "whitenoise>=6.4",
]

TAILWIND_CMD = [
    "tailwindcss",
    "-i", "static/css/input.css",
    "-o", "static/css/output.css",
    "--watch"
]

ICONS = {
    "Arch": "",
    "Debian": "",
    "Ubuntu": "",
    "Windows": "",
    "Linux": "",
}

VENV_PATH = ".venv"

# -------------------- UTILS --------------------
def run_cmd(cmd, check=True, env=None):
    print(f"> {' '.join(cmd)}")
    subprocess.run(cmd, check=check, env=env)

def detect_os():
    sys_platform = platform.system().lower()
    if sys_platform == "windows":
        return "Windows"
    elif sys_platform == "linux":
        try:
            with open("/etc/os-release") as f:
                data = f.read().lower()
            if "arch" in data:
                return "Arch"
            elif "ubuntu" in data:
                return "Ubuntu"
            elif "debian" in data:
                return "Debian"
            else:
                return "Linux"
        except FileNotFoundError:
            return "Linux"
    else:
        return sys_platform

def print_status(msg, icon=""):
    print(f"[{icon}] {msg}" if icon else msg)

# -------------------- VENV / PYTHON --------------------
def install_venv_package(os_type):
    print_status("Virtualenv module not found. Attempting to install system package...", icon="⚡")
    try:
        if os_type in ["Ubuntu", "Debian"]:
            run_cmd(["sudo", "apt", "update"])
            run_cmd(["sudo", "apt", "install", "-y", "python3.12-venv"])
        elif os_type == "Arch":
            run_cmd(["sudo", "pacman", "-Syu", "--noconfirm", "python-virtualenv"])
        elif os_type == "Windows":
            print_status("venv should already be included with Python on Windows. Please ensure Python is installed correctly.", icon="⚠")
        else:
            print_status(f"No automatic installation method for {os_type}. Install venv manually.", icon="⚠")
    except subprocess.CalledProcessError:
        print_status("Failed to install venv package. Install manually.", icon="⚠")
        sys.exit(1)

def ensure_venv():
    try:
        import venv
    except ImportError:
        os_type = detect_os()
        install_venv_package(os_type)

    if not os.path.exists(VENV_PATH):
        print_status("Creating virtual environment...", icon="⚡")
        subprocess.run([sys.executable, "-m", "venv", VENV_PATH], check=True)

    # Asegurarse de que pip esté disponible en el venv
    python_bin = get_python_bin()
    try:
        run_cmd([python_bin, "-m", "pip", "--version"])
    except subprocess.CalledProcessError:
        print_status("pip not found in venv. Installing pip...", icon="⚡")
        run_cmd([python_bin, "-m", "ensurepip", "--upgrade"])



def get_python_bin():
    return os.path.join(VENV_PATH, "Scripts" if platform.system() == "Windows" else "bin", "python")

def install_python_deps():
    print_status("Installing Python dependencies from requirements.txt...", icon="🐍")
    python_bin = get_python_bin()
    run_cmd([python_bin, "-m", "pip", "install", "--upgrade", "pip"])
    if os.path.exists("requirements.txt"):
        run_cmd([python_bin, "-m", "pip", "install", "-r", "requirements.txt"])
    else:
        print_status("requirements.txt not found!", icon="⚠")


# -------------------- NPM / TAILWIND --------------------
def ensure_npm_tailwind():
    if not shutil.which("npm") or not shutil.which("npx"):
        print_status("npm or npx not found. Install manually.", icon="⚠")
        sys.exit(1)
    # Tailwind is installed via npx so no global install needed

def install_npm_deps():
    if os.path.exists("package.json"):
        print_status("Installing npm dependencies...", icon="📦")
        run_cmd(["npm", "install"])

# -------------------- SERVERS --------------------
def run_servers():
    print_status("Starting Django and Tailwind servers...", icon="🚀")
    python_bin = get_python_bin()
    django_proc = subprocess.Popen([python_bin, "manage.py", "runserver"])
    tailwind_proc = subprocess.Popen(TAILWIND_CMD)

    try:
        django_proc.wait()
        tailwind_proc.wait()
    except KeyboardInterrupt:
        print_status("Stopping servers...", icon="🛑")
        django_proc.terminate()
        tailwind_proc.terminate()

# -------------------- MIGRATIONS --------------------
def run_migrations():
    print_status("Checking for pending migrations...", icon="🗄️")
    python_bin = get_python_bin()

    # Check if there are unapplied migrations
    result = subprocess.run(
        [python_bin, "manage.py", "showmigrations", "--plan"],
        capture_output=True,
        text=True,
    )

    pending = any(
        line.strip().startswith("[ ]") for line in result.stdout.splitlines()
    )

    if pending:
        print_status("Applying Django migrations...", icon="🗄️")
        run_cmd([python_bin, "manage.py", "makemigrations"])
        run_cmd([python_bin, "manage.py", "migrate"])
    else:
        print_status("No migrations to apply.", icon="✅")


# -------------------- MAIN --------------------
def main():
    os_type = detect_os()
    print_status(f"Detected OS: {os_type}", icon=ICONS.get(os_type, ""))
    ensure_venv()
    install_python_deps()
    ensure_npm_tailwind()
    install_npm_deps()
    run_migrations()
    run_servers()

if __name__ == "__main__":
    main()
