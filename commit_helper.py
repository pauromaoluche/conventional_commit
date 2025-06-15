import os
import subprocess
from datetime import datetime
import re
import sys

VERSION_LOG_FILE = "versionLog"
CHANGELOG_FILE = "CHANGELOG.md"
DEFAULT_VERSION = "1.0.0"

TYPES = {
    "feat": "Nova funcionalidade",
    "fix": "Correção de bug",
    "docs": "Apenas documentação",
    "style": "Formatação, ponto e vírgula, etc.",
    "refactor": "Refatoração sem alteração de funcionalidade"
}

MAJORMINORPATCH = {
    "major": "(1).0.0 - Mudança incompatível, que quebra retrocompatibilidade.",
    "minor": "1.(1).0 - Nova funcionalidade, mantendo compatibilidade.",
    "patch": "1.1.(1) - Correção de bug, pequena melhoria."
}

def get_user_input():
    print("\nSelecione o tipo do commit:")
    for key, desc in TYPES.items():
        print(f"{key} - {desc}")
    commit_type = input("\nType: ").strip()

    if commit_type not in TYPES:
        print("Tipo inválido!")
        sys.exit(1)

    message = input("\nMensagem do commit: ").strip()
    additional = input("Informações adicionais (opcional): ").strip()

    print("\nInforme a mudança de versão:")
    for key, desc in MAJORMINORPATCH.items():
        print(f"{key} - {desc}")
    major = input("\nMAJOR (0 se não mudou): ").strip() or "0"
    minor = input("MINOR (0 se não mudou): ").strip() or "0"
    patch = input("PATCH (0 se não mudou): ").strip() or "0"

    return commit_type, message, additional, int(major), int(minor), int(patch)

def read_current_version():
    if not os.path.exists(VERSION_LOG_FILE):
        return DEFAULT_VERSION
    with open(VERSION_LOG_FILE, "r") as f:
        lines = f.readlines()
        for line in reversed(lines):
            match = re.search(r'v(\d+\.\d+\.\d+)', line)
            if match:
                return match.group(1)
    return DEFAULT_VERSION

def bump_version(version, major, minor, patch):
    current = list(map(int, version.split(".")))
    new_version = [
        current[0] + major,
        current[1] + minor if major == 0 else 0,
        current[2] + patch if major == 0 and minor == 0 else 0
    ]
    return ".".join(map(str, new_version))

def update_version_log(date, commit_type, message, additional, version, modified_files):
    with open(VERSION_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{date}] {commit_type}: {message} | {additional} (v{version})\n")
        if modified_files:
            f.write("Arquivos modificados:\n")
            for file in modified_files:
                f.write(f"  - {file}\n")
            f.write("\n")

def update_changelog(date, version, commit_type, message, additional, modified_files):
    entry = f"## v{version} [{date}]\n **{commit_type}**: {message}"
    if additional:
        entry += f"\n- {additional}"

    if modified_files:
        entry += f"\n\nArquivos modificados:\n"
        for file in modified_files:
            entry += f"- `{file}`\n"

    entry += "\n\n"

    if os.path.exists(CHANGELOG_FILE):
        with open(CHANGELOG_FILE, "r", encoding="utf-8") as f:
            existing = f.read()
        with open(CHANGELOG_FILE, "w", encoding="utf-8") as f:
            f.write(entry + existing)
    else:
        with open(CHANGELOG_FILE, "w", encoding="utf-8") as f:
            f.write("# Changelog\n\n" + entry)

def create_git_tag(version):
    try:
        subprocess.run(["git", "rev-parse", "--verify", "HEAD"], check=True, stdout=subprocess.DEVNULL)
        subprocess.run(["git", "tag", "-a", f"v{version}", "-m", f"Versão {version}"], check=True)
    except subprocess.CalledProcessError:
        print("⚠️ Repositório sem commits anteriores. Tag não criada.")

def get_modified_files():
    result = subprocess.run(["git", "diff", "--cached", "--name-only"], capture_output=True, text=True)
    return result.stdout.strip().splitlines()

def generate_commit_message():
    commit_type, message, additional, major, minor, patch = get_user_input()
    current_version = read_current_version()
    new_version = bump_version(current_version, major, minor, patch)
    modified_files = get_modified_files()

    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #update_version_log(date, commit_type, message, additional, new_version, modified_files)
    update_changelog(date, new_version, commit_type, message, additional, modified_files)
    #create_git_tag(new_version)

    subprocess.run(["git", "add", VERSION_LOG_FILE, CHANGELOG_FILE], check=True)

    commit_msg = f"{commit_type}: {message}\n\n{additional}\n\nv{new_version}\n\n{modified_files}"
    return commit_msg

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--generate-message":
        try:
            msg = generate_commit_message()
            with open(".git/COMMIT_EDITMSG", "w", encoding="utf-8") as f:
                f.write(msg)
            print(msg)
        except EOFError:
            print("❌ Falha ao gerar a mensagem do commit.")
            sys.exit(1)
    else:
        print("Este script deve ser executado com --generate-message para criar commit.")

if __name__ == "__main__":
    main()
