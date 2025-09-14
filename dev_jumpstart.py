#!/usr/bin/env python3
import os
import subprocess
import sys
import platform
import shutil
import socket

# -------------------- CONFIG --------------------
PY_DEPS = [
    "django>=4.2,<5.0",
    "django-browser-reload>=0.2",
    "django-widget-tweaks>=1.5",
    "psycopg2-binary>=2.9",
    "whitenoise>=6.4",
]

VENV_PATH = ".venv"
DJANGO_PORT = 8000

ICONS = {
    "Arch": "",
    "Debian": "",
    "Ubuntu": "",
    "Windows": "",
    "Linux": "",
}

# -------------------- UTILS --------------------
def run_cmd(cmd, check=True, env=None):
    print(f"> {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    subprocess.run(cmd, check=check, env=env, shell=isinstance(cmd, str))

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
    print_status("venv module not found or unusable. Installing system package...", icon="⚡")
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
    os_type = detect_os()
    try:
        import venv
        test_path = ".venv_test"
        subprocess.run([sys.executable, "-m", "venv", test_path], check=True)
        shutil.rmtree(test_path)
    except (ImportError, subprocess.CalledProcessError):
        install_venv_package(os_type)

    if not os.path.exists(VENV_PATH):
        print_status("Creating virtual environment...", icon="⚡")
        subprocess.run([sys.executable, "-m", "venv", VENV_PATH], check=True)

    python_bin = get_python_bin()
    try:
        run_cmd([python_bin, "-m", "pip", "--version"])
    except subprocess.CalledProcessError:
        print_status("pip not found in venv. Installing pip...", icon="⚡")
        run_cmd([python_bin, "-m", "ensurepip", "--upgrade"])

def get_python_bin():
    return os.path.join(VENV_PATH, "Scripts" if platform.system() == "Windows" else "bin", "python")

def install_python_deps():
    print_status("Installing Python dependencies...", icon="🐍")
    python_bin = get_python_bin()
    run_cmd([python_bin, "-m", "pip", "install", "--upgrade", "pip"])
    if os.path.exists("requirements.txt"):
        run_cmd([python_bin, "-m", "pip", "install", "-r", "requirements.txt"])
    else:
        run_cmd([python_bin, "-m", "pip", "install"] + PY_DEPS)

# -------------------- NPM / NODE / TAILWIND --------------------
def run_cmd(cmd, check=True, env=None):
    print(f"> {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    subprocess.run(cmd, check=check, env=env, shell=isinstance(cmd, str))

def get_node_version():
    try:
        result = subprocess.run(["node", "-v"], capture_output=True, text=True)
        if result.returncode == 0:
            v = result.stdout.strip()
            # remove 'v' prefix
            return tuple(map(int, v.lstrip("v").split(".")))
    except FileNotFoundError:
        return None

def install_node(os_type):
    print_status("Installing Node.js and npm...", icon="⚡")
    try:
        if os_type in ["Ubuntu", "Debian"]:
            # Remove old Node.js
            run_cmd("sudo apt remove -y nodejs npm")
            # Install via NodeSource
            run_cmd("curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -")
            run_cmd("sudo apt install -y nodejs")
        elif os_type == "Arch":
            run_cmd("sudo pacman -Rns --noconfirm nodejs npm")
            run_cmd("sudo pacman -Syu --noconfirm nodejs npm")
        elif os_type == "Windows":
            print_status("Please install Node.js from https://nodejs.org/", icon="⚠")
            sys.exit(1)
        else:
            print_status(f"No automatic Node.js installation method for {os_type}. Install manually.", icon="⚠")
            sys.exit(1)
    except subprocess.CalledProcessError:
        print_status("Failed to install Node.js/npm. Install manually.", icon="⚠")
        sys.exit(1)

def ensure_node():
    os_type = detect_os()
    node_version = get_node_version()
    min_versions = [(20,17,0), (22,9,0)]
    
    def version_ok(v):
        return v >= min_versions[0] or v >= min_versions[1]

    if node_version is None:
        print_status("Node.js not found.", icon="⚡")
        install_node(os_type)
    elif not version_ok(node_version):
        print_status(f"Node.js version too old: {'.'.join(map(str,node_version))}", icon="⚡")
        user_input = input("Do you want to uninstall and install the latest Node.js? [y/N]: ").strip().lower()
        if user_input == "y":
            install_node(os_type)
        else:
            print_status("Cannot continue with outdated Node.js.", icon="⚠")
            sys.exit(1)
    
    # Ensure npm is available
    if not shutil.which("npm") or not shutil.which("npx"):
        print_status("npm or npx not found after Node.js installation.", icon="⚠")
        sys.exit(1)

def install_tailwind_local():
    print_status("Installing local TailwindCSS...", icon="⚡")
    run_cmd("npm install --save-dev tailwindcss @tailwindcss/postcss")
    # verify
    result = subprocess.run("npx tailwindcss --version", shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print_status("TailwindCSS not found after local install.", icon="⚠")
        sys.exit(1)

def install_npm_deps():
    ensure_node()
    if os.path.exists("package.json"):
        print_status("Installing npm dependencies...", icon="⚡")
        run_cmd("npm install --include=dev")
    install_tailwind_local()

# -------------------- SERVERS --------------------
def find_free_port(start_port):
    port = start_port
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('localhost', port)) != 0:
                return port
        port += 1

def run_servers():
    print_status("Starting Django and Tailwind servers...", icon="🚀")
    python_bin = get_python_bin()
    port = find_free_port(DJANGO_PORT)

    django_proc = subprocess.Popen([python_bin, "manage.py", "runserver", str(port)])

    tailwind_cmd = "npx tailwindcss -i static/css/input.css -o static/css/output.css --watch"
    tailwind_proc = subprocess.Popen(tailwind_cmd, shell=True)

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
    result = subprocess.run(
        [python_bin, "manage.py", "showmigrations", "--plan"],
        capture_output=True,
        text=True,
    )
    pending = any(line.strip().startswith("[ ]") for line in result.stdout.splitlines())
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
    install_npm_deps()
    run_migrations()
    run_servers()

if __name__ == "__main__":
    main()
