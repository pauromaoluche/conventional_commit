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
    "improvement": "Melhoria de funcionalidade existente",
    "chore": "Tarefas de manutenção, sem impacto direto no código",
    "fix": "Correção de bug",
    "docs": "Apenas documentação",
    "style": "Formatação, ponto e vírgula, etc.",
    "refactor": "Refatoração sem alteração de funcionalidade"
}

def get_version_bump(commit_type):
    if commit_type == "feat":
        return (0, 1, 0)
    return (0, 0, 1)

def get_user_input():
    print("\nSelecione o tipo do commit:")
    for key, desc in TYPES.items():
        print(f"{key} - {desc}")
    commit_type = input("\nTipo: ").strip()

    if commit_type not in TYPES:
        print("❌ Tipo inválido!")
        sys.exit(1)

    message = input("\nMensagem do commit: ").strip()
    additional = input("Informações adicionais (opcional): ").strip()
    return commit_type, message, additional

def read_current_version():
    if not os.path.exists(CHANGELOG_FILE):
        return DEFAULT_VERSION
    with open(CHANGELOG_FILE, "r") as f:
        for line in f:
            match = re.search(r'v(\d+\.\d+\.\d+)', line)
            if match:
                return match.group(1)
    return DEFAULT_VERSION

def bump_version(version, major, minor, patch):
    current = list(map(int, version.split(".")))
    return ".".join(map(str, [
        current[0] + major,
        current[1] + (0 if major else minor),
        current[2] + (0 if major or minor else patch)
    ]))

def get_modified_files():
    result = subprocess.run(["git", "diff", "--cached", "--name-only"], capture_output=True, text=True)
    return result.stdout.strip().splitlines()

def update_changelog(date, version, commit_type, message, additional, modified_files):
    entry = f"## v{version} [{date}]\n\n- **{commit_type}**: {message}"
    if additional:
        entry += f"\n- {additional}"
    if modified_files:
        entry += "\n\nArquivos modificados:\n" + "\n".join(f"- `{f}`" for f in modified_files)
    entry += "\n\n"

    if os.path.exists(CHANGELOG_FILE):
        with open(CHANGELOG_FILE, "r", encoding="utf-8") as f:
            old = f.read()
        with open(CHANGELOG_FILE, "w", encoding="utf-8") as f:
            f.write(entry + old)
    else:
        with open(CHANGELOG_FILE, "w", encoding="utf-8") as f:
            f.write("# Changelog\n\n" + entry)

def create_git_tag(version):
    try:
        subprocess.run(["git", "rev-parse", "--verify", "HEAD"], check=True, stdout=subprocess.DEVNULL)
        subprocess.run(["git", "tag", "-a", f"v{version}", "-m", f"Versão {version}"], check=True)
    except subprocess.CalledProcessError:
        print("⚠️ Sem commits anteriores. Tag ignorada.")

def get_issue_number_from_branch():
    branch = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True).stdout.strip()
    match = re.search(r'-(\d+)$', branch)
    return match.group(1) if match else None

def generate_commit_message():
    commit_type, message, additional = get_user_input()
    current_version = read_current_version()
    major, minor, patch = get_version_bump(commit_type)
    new_version = bump_version(current_version, major, minor, patch)
    modified_files = get_modified_files()

    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    update_changelog(date, new_version, commit_type, message, additional, modified_files)
    create_git_tag(new_version)
    subprocess.run(["git", "add", CHANGELOG_FILE], check=True)

    footer = ""
    issue_number = get_issue_number_from_branch()
    if issue_number:
        footer = f"\n\nCloses #{issue_number}"

    return f"{commit_type}: {message}\n\n{additional}\n\nv{new_version}\n\nArquivos:\n" + \
        "\n".join(modified_files) + footer

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--generate-message":
        try:
            msg = generate_commit_message()
            with open(".git/COMMIT_EDITMSG", "w", encoding="utf-8") as f:
                f.write(msg)
            print("✅ Mensagem gerada com sucesso.")
        except EOFError:
            print("❌ Entrada de usuário cancelada.")
            sys.exit(1)
    else:
        print("Use: python3 commit_helper.py --generate-message")

if __name__ == "__main__":
    main()
