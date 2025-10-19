#!/usr/bin/env python3
import os
import subprocess
import sys
import platform
import shutil
import socket
import time
import hashlib

# -------------------- CONFIG --------------------
PY_DEPS = [
    "django>=4.2,<5.0",
    "django-browser-reload>=0.2",
    "django-widget-tweaks>=1.5",
    "psycopg2-binary>=2.9",
    "whitenoise>=6.4",
    "pytest",
    "pytest-django",
    "black",
    "flake8",
]

VENV_PATH = ".venv"
DJANGO_PORT = 8000
NODE_MIN_VERSION = (20, 17, 0)

DEBUG = False

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
    "Info": "💡",
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
    "grey": "\033[90m",
}


def print_header(msg):
    print(f"\n{COLORS['blue']}==================== {msg} ===================={RESET}")


def print_status(msg, icon="", color="white", indent=0):
    indent_str = "  " * indent
    c = COLORS.get(color, COLORS["white"])
    print(f"{c}{indent_str}[{icon}] {msg}{RESET}")


def run_cmd(cmd, check=True, env=None, hide_warnings=False, debug=False):
    if isinstance(cmd, list):
        cmd_str = " ".join(cmd)
    else:
        cmd_str = cmd

    if debug:
        print_status(f"[DEBUG] Running command: {cmd_str}", ICONS["Info"], color="magenta")

    try:
        subprocess.run(cmd, check=check, env=env, shell=isinstance(cmd, str))
    except subprocess.CalledProcessError as e:
        print_status(f"[ERROR] Command failed: {cmd_str}", ICONS["Warning"], color="red")
        print_status(f"[ERROR] Return code: {e.returncode}", ICONS["Warning"], color="red")
        if hasattr(e, "stdout") and e.stdout:
            print(e.stdout)
        if hasattr(e, "stderr") and e.stderr:
            print(e.stderr)
        raise


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
        print_status(
            "pip not found in venv. Installing pip...", ICONS["Action"], color="cyan"
        )
        run_cmd([python_bin, "-m", "ensurepip", "--upgrade"])


def install_venv_package(os_type):
    print_status(
        "venv module not found. Installing system package...",
        ICONS["Action"],
        color="cyan",
    )
    try:
        if os_type in ["Ubuntu", "Debian"]:
            run_cmd(["sudo", "apt", "update"])
            run_cmd(["sudo", "apt", "install", "-y", "python3-venv"])
        elif os_type == "Arch":
            run_cmd(["sudo", "pacman", "-Syu", "--noconfirm", "python-virtualenv"])
        elif os_type == "Windows":
            print_status(
                "Please ensure Python includes venv module.",
                ICONS["Warning"],
                color="yellow",
            )
    except subprocess.CalledProcessError:
        print_status(
            "Failed to install venv package. Install manually.",
            ICONS["Warning"],
            color="yellow",
        )
        sys.exit(1)


def get_python_bin():
    return os.path.join(
        VENV_PATH, "Scripts" if platform.system() == "Windows" else "bin", "python"
    )


def install_python_deps():
    print_header("Python Dependencies")
    python_bin = get_python_bin()
    run_cmd([python_bin, "-m", "pip", "install", "--upgrade", "pip"])
    if os.path.exists("requirements-dev.txt"):
        run_cmd([python_bin, "-m", "pip", "install", "-r", "requirements-dev.txt"])
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
            print_status(
                "Install curl manually from https://curl.se/windows/",
                ICONS["Warning"],
                color="yellow",
            )
            sys.exit(1)
    except subprocess.CalledProcessError:
        print_status(
            "Failed to install curl. Install manually.",
            ICONS["Warning"],
            color="yellow",
        )
        sys.exit(1)
    print_status("curl is ready.", ICONS["Success"], color="green")


# -------------------- NODE / NPM / TAILWIND --------------------
def get_node_version():
    try:
        result = subprocess.run(["node", "-v"], capture_output=True, text=True)
        if result.returncode != 0:
            return None
        version_tuple = tuple(
            int(x) for x in result.stdout.strip().lstrip("v").split(".")
        )
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
        print_status(
            f"Node.js version OK ({'.'.join(map(str,node_version))})",
            ICONS["Success"],
            color="green",
        )

    if not shutil.which("npm") or not shutil.which("npx"):
        print_status(
            "npm/npx missing. Node.js installation failed.",
            ICONS["Warning"],
            color="yellow",
        )
        sys.exit(1)


def install_node(os_type):
    try:
        if os_type in ["Ubuntu", "Debian"]:
            run_cmd(
                "curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -",
                hide_warnings=True,
            )
            run_cmd(["sudo", "apt", "install", "-y", "nodejs"], hide_warnings=True)
        elif os_type == "Arch":
            run_cmd(
                ["sudo", "pacman", "-Syu", "--noconfirm", "nodejs", "npm"],
                hide_warnings=True,
            )
        elif os_type == "Windows":
            print_status(
                "Install Node.js >=20 manually from https://nodejs.org/",
                ICONS["Warning"],
                color="yellow",
            )
            sys.exit(1)
    except subprocess.CalledProcessError:
        print_status(
            "Node.js installation failed. Install manually.",
            ICONS["Warning"],
            color="yellow",
        )
        sys.exit(1)


# -------------------- NODE / NPM / TAILWIND --------------------
def install_npm_deps():
    print_header("TailwindCSS + LightningCSS Setup")
    ensure_node()

    # Correct package for LightningCSS CLI
    packages = ["tailwindcss", "@tailwindcss/cli", "lightningcss-cli"]

    if not os.path.exists("package.json"):
        run_cmd(["npm", "init", "-y"], hide_warnings=True)

    run_cmd(["npm", "install", "--save-dev"] + packages, hide_warnings=True)

    tailwind_bin = os.path.join("node_modules", ".bin", "tailwindcss")
    lightning_bin = os.path.join("node_modules", ".bin", "lightningcss")

    if not os.path.exists(tailwind_bin):
        print_status("TailwindCSS binary not found!", ICONS["Warning"], color="yellow")
        sys.exit(1)
    if not os.path.exists(lightning_bin):
        print_status("LightningCSS binary not found!", ICONS["Warning"], color="yellow")
        sys.exit(1)

    print_status("TailwindCSS + LightningCSS installed successfully.", ICONS["Success"], color="green")

# -------------------- SERVER --------------------
def find_free_port(start_port):
    port = start_port
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("localhost", port)) != 0:
                return port
        port += 1


def file_hash(path):
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

def run_servers():
    print_header("Starting Servers")
    python_bin = get_python_bin()
    port = int(os.environ.get("DJANGO_PORT", DJANGO_PORT))
    port = find_free_port(port)
    print_status(f"Using port {port}", ICONS["Success"], color="green")

    # Start Django dev server
    django_proc = subprocess.Popen(
        [python_bin, "manage.py", "runserver", f"0.0.0.0:{port}"]
    )
    print_status("Django server started.", ICONS["Server"], color="green")

    # Tailwind watch
    tailwind_cmd = "./node_modules/.bin/tailwindcss -i static/css/input.css -o static/css/output.css --watch"
    tailwind_proc = subprocess.Popen(tailwind_cmd, shell=True)
    print_status("TailwindCSS watching for changes...", ICONS["Tailwind"], color="cyan")

    lightning_bin = "./node_modules/.bin/lightningcss"
    output_file = "static/css/output.css"
    min_file = "static/css/output.min.css"

    last_hash = None
    try:
        while True:
            if os.path.exists(output_file):
                current_hash = file_hash(output_file)
                if last_hash != current_hash:
                    last_hash = current_hash
                    # Run LightningCSS
                    subprocess.run(
                        [lightning_bin, output_file, "-o", min_file, "--minify", "--targets", ">= 0.25%"]
                    )
                    print_status("[🎨] LightningCSS rebuilt output.min.css", ICONS["Tailwind"], color="green")
            time.sleep(0.2)  # short debounce to avoid double triggers
    except KeyboardInterrupt:
        print_status("\nStopping servers...", ICONS["Stop"], color="yellow")
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
    result = subprocess.run(
        [python_bin, "manage.py", "showmigrations", "--plan"],
        capture_output=True,
        text=True,
    )
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
