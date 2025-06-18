#!/bin/bash
echo "🔧 Executando commit helper..."
python commit_helper.py --generate-message
if [ $? -ne 0 ]; then
    echo "❌ Erro ao gerar mensagem."
    exit 1
fi
git commit -F .git/COMMIT_EDITMSG
