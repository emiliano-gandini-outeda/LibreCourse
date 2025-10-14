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
NODE_MIN_VERSION = (20, 17, 0)

ICONS = {
    "Arch": "",
    "Debian": "",
    "Ubuntu": "",
    "Windows": "",
    "Linux": "",
    "Python": "🐍",
    "Node": "🟢",
    "Tailwind": "🎨",
    "Server": "🚀",
    "Warning": "⚠",
    "Success": "✅",
    "Action": "⚡",
    "DB": "🗄️",
    "Stop": "🛑",
    "Info": "💡"
}

# -------------------- UTILS --------------------
RESET = "\033[0m"
COLORS = {
    "cyan": "\033[96m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "magenta": "\033[95m",
    "blue": "\033[94m",
    "red": "\033[91m",
    "white": "\033[97m",
    "grey": "\033[90m"
}

def print_header(msg):
    print(f"\n{COLORS['blue']}==================== {msg} ===================={RESET}")

def print_status(msg, icon="", color="white", indent=0):
    indent_str = "  " * indent
    c = COLORS.get(color, COLORS["white"])
    print(f"{c}{indent_str}[{icon}] {msg}{RESET}")

def run_cmd(cmd, check=True, env=None, hide_warnings=False):
    if hide_warnings and isinstance(cmd, list) and cmd[0] == "npm":
        # Redirect stderr to null
        if platform.system().lower() != "windows":
            cmd_str = " ".join(cmd) + " 2>/dev/null"
            subprocess.run(cmd_str, check=check, shell=True)
            return
        else:
            # On Windows, npm quiet mode
            cmd.append("--quiet")
    print_status(f"> {' '.join(cmd) if isinstance(cmd, list) else cmd}", icon=ICONS["Info"], indent=1)
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
    return sys_platform

# -------------------- VENV --------------------
def ensure_venv():
    print_header("Python Virtual Environment")
    try:
        import venv
        test_path = ".venv_test"
        subprocess.run([sys.executable, "-m", "venv", test_path], check=True)
        shutil.rmtree(test_path)
    except (ImportError, subprocess.CalledProcessError):
        install_venv_package(detect_os())

    if not os.path.exists(VENV_PATH):
        print_status("Creating virtual environment...", ICONS["Action"], color="cyan")
        subprocess.run([sys.executable, "-m", "venv", VENV_PATH], check=True)

    python_bin = get_python_bin()
    try:
        run_cmd([python_bin, "-m", "pip", "--version"])
    except subprocess.CalledProcessError:
        print_status("pip not found in venv. Installing pip...", ICONS["Action"], color="cyan")
        run_cmd([python_bin, "-m", "ensurepip", "--upgrade"])

def install_venv_package(os_type):
    print_status("venv module not found. Installing system package...", ICONS["Action"], color="cyan")
    try:
        if os_type in ["Ubuntu", "Debian"]:
            run_cmd(["sudo", "apt", "update"])
            run_cmd(["sudo", "apt", "install", "-y", "python3-venv"])
        elif os_type == "Arch":
            run_cmd(["sudo", "pacman", "-Syu", "--noconfirm", "python-virtualenv"])
        elif os_type == "Windows":
            print_status("Please ensure Python includes venv module.", ICONS["Warning"], color="yellow")
    except subprocess.CalledProcessError:
        print_status("Failed to install venv package. Install manually.", ICONS["Warning"], color="yellow")
        sys.exit(1)

def get_python_bin():
    return os.path.join(VENV_PATH, "Scripts" if platform.system() == "Windows" else "bin", "python")

def install_python_deps():
    print_header("Python Dependencies")
    python_bin = get_python_bin()
    run_cmd([python_bin, "-m", "pip", "install", "--upgrade", "pip"])
    if os.path.exists("requirements.txt"):
        run_cmd([python_bin, "-m", "pip", "install", "-r", "requirements.txt"])
    else:
        run_cmd([python_bin, "-m", "pip", "install"] + PY_DEPS)

# -------------------- CURL --------------------
def ensure_curl(os_type):
    print_header("Checking curl")
    if shutil.which("curl"):
        print_status("curl is already installed.", ICONS["Success"], color="green")
        return
    print_status("curl not found. Installing...", ICONS["Action"], color="cyan")
    try:
        if os_type in ["Ubuntu", "Debian"]:
            run_cmd(["sudo", "apt", "update", "--allow-releaseinfo-change"])
            run_cmd(["sudo", "apt", "install", "-y", "curl"])
        elif os_type == "Arch":
            run_cmd(["sudo", "pacman", "-Syu", "--noconfirm", "curl"])
        elif os_type == "Windows":
            print_status("Install curl manually from https://curl.se/windows/", ICONS["Warning"], color="yellow")
            sys.exit(1)
    except subprocess.CalledProcessError:
        print_status("Failed to install curl. Install manually.", ICONS["Warning"], color="yellow")
        sys.exit(1)
    print_status("curl is ready.", ICONS["Success"], color="green")

# -------------------- NODE / NPM / TAILWIND --------------------
def get_node_version():
    try:
        result = subprocess.run(["node", "-v"], capture_output=True, text=True)
        if result.returncode != 0:
            return None
        version_tuple = tuple(int(x) for x in result.stdout.strip().lstrip("v").split("."))
        return version_tuple
    except FileNotFoundError:
        return None

def ensure_node():
    print_header("Node.js & NPM")
    os_type = detect_os()
    node_version = get_node_version()
    if node_version is None or node_version < NODE_MIN_VERSION:
        print_status("Installing or updating Node.js...", ICONS["Action"], color="cyan")
        install_node(os_type)
    else:
        print_status(f"Node.js version OK ({'.'.join(map(str,node_version))})", ICONS["Success"], color="green")

    if not shutil.which("npm") or not shutil.which("npx"):
        print_status("npm/npx missing. Node.js installation failed.", ICONS["Warning"], color="yellow")
        sys.exit(1)

def install_node(os_type):
    try:
        if os_type in ["Ubuntu", "Debian"]:
            run_cmd("curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -", hide_warnings=True)
            run_cmd(["sudo", "apt", "install", "-y", "nodejs"], hide_warnings=True)
        elif os_type == "Arch":
            run_cmd(["sudo", "pacman", "-Syu", "--noconfirm", "nodejs", "npm"], hide_warnings=True)
        elif os_type == "Windows":
            print_status("Install Node.js >=20 manually from https://nodejs.org/", ICONS["Warning"], color="yellow")
            sys.exit(1)
    except subprocess.CalledProcessError:
        print_status("Node.js installation failed. Install manually.", ICONS["Warning"], color="yellow")
        sys.exit(1)

def install_npm_deps():
    print_header("TailwindCSS Setup")
    ensure_node()

    packages = ["tailwindcss", "@tailwindcss/cli", "postcss", "autoprefixer"]
    if not os.path.exists("package.json"):
        run_cmd(["npm", "init", "-y"], hide_warnings=True)

    run_cmd(["npm", "install", "--save-dev"] + packages, hide_warnings=True)

    tailwind_bin = os.path.join("node_modules", ".bin", "tailwindcss")
    if not os.path.exists(tailwind_bin):
        print_status("TailwindCSS binary not found!", ICONS["Warning"], color="yellow")
        sys.exit(1)
    print_status("TailwindCSS is installed and ready.", ICONS["Success"], color="green")

# -------------------- SERVER --------------------
def find_free_port(start_port):
    port = start_port
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('localhost', port)) != 0:
                return port
        port += 1

def run_servers():
    print_header("Starting Servers")
    python_bin = get_python_bin()
    port = int(os.environ.get("DJANGO_PORT", DJANGO_PORT))

    start_port = int(os.environ.get("DJANGO_PORT", DJANGO_PORT))
    port=find_free_port(start_port)

    print_status(f"Using port {port}", ICONS["Success"], color="green")

    django_proc = subprocess.Popen([python_bin, "manage.py", "runserver", f"0.0.0.0:{port}"])
    tailwind_proc = subprocess.Popen("npx tailwindcss -i static/css/input.css -o static/css/output.css --watch", shell=True)

    try:
        django_proc.wait()
        tailwind_proc.wait()
    except KeyboardInterrupt:
        print_status("Stopping servers...", ICONS["Stop"], color="yellow")
        django_proc.terminate()
        tailwind_proc.terminate()

# -------------------- MIGRATIONS --------------------
def run_migrations():
    print_header("Django Migrations")
    python_bin = get_python_bin()

    # Step 1: Always run makemigrations first
    print_status("Checking for model changes...", ICONS["DB"], color="cyan")
    run_cmd([python_bin, "manage.py", "makemigrations"])

    # Step 2: Check for unapplied migrations
    result = subprocess.run([python_bin, "manage.py", "showmigrations", "--plan"],
                            capture_output=True, text=True)
    pending = any(line.strip().startswith("[ ]") for line in result.stdout.splitlines())

    if pending:
        print_status("Applying migrations...", ICONS["DB"], color="cyan")
        run_cmd([python_bin, "manage.py", "migrate"])
    else:
        print_status("No migrations to apply.", ICONS["Success"], color="green")


# -------------------- MAIN --------------------
def main():
    os_type = detect_os()
    print_header(f"Detected OS: {os_type} {ICONS.get(os_type,'')}")
    ensure_curl(os_type)
    ensure_venv()
    install_python_deps()
    install_npm_deps()
    run_migrations()
    run_servers()

if __name__ == "__main__":
    main()
