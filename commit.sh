#!/bin/bash

echo "🔧 Executando commit helper..."

# Gerar mensagem do commit pelo script Python e salvar no arquivo temporário do Git
python3 commit_helper.py --generate-message
if [ $? -ne 0 ]; then
    echo "❌ Falha ao gerar mensagem do commit."
    exit 1
fi

# Fazer commit usando a mensagem gerada
git commit -F .git/COMMIT_EDITMSG
