# 🧰 Commit Helper

Este projeto tem como objetivo **padronizar mensagens de commit**, **gerar automaticamente um changelog** e **atualizar a versão do projeto automaticamente** com base nos commits realizados.

> ⚠️ **Atenção:** Atualmente o projeto está preparado para uso individual. Em breve, poderá ser adaptado para uso em equipes.

## 🚀 Funcionalidades

- Prompt interativo para criação de mensagens de commit.
- Estrutura padronizada baseada em tipos (`feat`, `fix`, `docs`, etc.).
- Geração automática de changelog.
- Integração com Git para aplicar a mensagem diretamente no commit.

## 📦 Como usar

1. Certifique-se de ter **Python 3** instalado.
2. Coloque o script `install_commit_helper.sh` no diretorio do seu projeto
3. De permissão para execução, `chmod +x install_commit_helper.sh`
4. Certifique-se que ja rodou `git init` e que o repositorio do git ja esta configurado no diretorio atual
5. Execute o sh `./install_commit_helper.sh`
6. Quando for commitar algo, adicione os itens desejados que vão ser commitados, pelo proprio `git add` ou pelo proprio editor.
7. Rode `./commit.sh`
8. Após preencher as informações pedidas, só rodar o `git push`

O script `commit_helper.py` irá guiar você no processo de criação da mensagem de commit, salvá-la e aplicá-la diretamente com o Git.

## 📘 Estrutura das Mensagens

O script segue a convenção de commits semânticos, como por exemplo:

- `feat: Adiciona funcionalidade X`
- `fix: Corrige erro no módulo Y`
- `docs: Atualiza documentação`
- `style: Ajusta formatação`
- `refactor: Refatora componente Z`

## 🛠 Requisitos

- Python 3.x
- Git

## 📅 Roadmap

- [x] Geração de mensagens de commit padronizadas
- [ ] Suporte multiusuário/equipe
- [x] Geração parcial de `CHANGELOG.md`
- [ ] Geração completa de `CHANGELOG.md`
- [ ] Integração com `pre-commit` hook

## 📄 Licença

Este projeto está em desenvolvimento pessoal e ainda não possui uma licença oficial. Futuramente poderá ser aberto para colaboração.

---