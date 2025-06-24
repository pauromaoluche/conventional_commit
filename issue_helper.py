import requests
import os
import subprocess
import re

GITHUB_TOKEN = os.getenv("GH_TOKEN") or "SEU_TOKEN_AQUI"
REPO_OWNER = "pauromaoluche"
REPO_NAME = "conventional_commit"
API_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues"

def slugify(text):
    return re.sub(r'[^\w\-]+', '-', text.lower().strip()).strip('-')

def criar_issue():
    print("📋 Criar nova issue para tarefa")
    titulo = input("Título da tarefa: ").strip()
    tipo = input("Tipo (feat, fix, chore, improvement...): ").strip()
    prioridade = input("Prioridade (Alta, Média, Baixa): ").strip()
    descricao = input("Descrição breve: ").strip()

    body = f"""### Tipo de tarefa
{tipo}

### Prioridade
{prioridade}

### Descrição
{descricao}

### Etapas ou critérios de aceitação
- [ ] Implementar
- [ ] Testar
- [ ] Commitar
"""

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    data = {
        "title": titulo,
        "body": body,
        "labels": ["tarefa"]
    }

    response = requests.post(API_URL, headers=headers, json=data)

    if response.status_code == 201:
        issue = response.json()
        issue_number = issue["number"]
        print(f"✅ Issue criada com sucesso: #{issue_number} - {titulo}")

        nome_branch = f"{tipo}/{slugify(titulo)}-{issue_number}"
        subprocess.run(["git", "checkout", "development"])
        subprocess.run(["git", "pull"])
        subprocess.run(["git", "checkout", "-b", nome_branch])
        print(f"🌿 Branch criada: {nome_branch}")
    else:
        print("❌ Erro ao criar issue:", response.status_code, response.text)

if __name__ == "__main__":
    criar_issue()
