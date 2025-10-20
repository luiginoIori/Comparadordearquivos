# Instruções para Configurar o Repositório Git

## Execute os seguintes comandos no PowerShell ou Prompt de Comando:

### 1. Abra o PowerShell como Administrador

### 2. Navegue para o diretório do projeto:
```cmd
cd "g:\Meu Drive\Modelos IA\ComparadorDeArquivo"
```

### 3. Execute os comandos Git em sequência:

```cmd
# Inicializar repositório Git
git init

# Configurar usuário (substitua pelos seus dados)
git config user.name "Luigi Iori"
git config user.email "luiginolori@gmail.com"

# Adicionar todos os arquivos
git add .

# Fazer o primeiro commit
git commit -m "first commit"

# Renomear branch para main
git branch -M main

# Adicionar repositório remoto
git remote add origin https://github.com/luiginoIori/Comparadordearquivos.git

# Fazer push para o repositório remoto
git push -u origin main
```

### 4. Verificar se tudo funcionou:
```cmd
git status
git remote -v
```

## 📋 Arquivos no Repositório:

✅ **app.py** - Aplicativo principal Streamlit
✅ **requirements.txt** - Dependências do projeto
✅ **README.md** - Documentação principal
✅ **GUIA_DE_USO.md** - Guia detalhado de uso
✅ **iniciar.bat** - Script para iniciar o aplicativo
✅ **setup_git.bat** - Script de configuração Git (Windows)
✅ **setup_git.ps1** - Script de configuração Git (PowerShell)
✅ **.gitignore** - Arquivos a serem ignorados pelo Git
✅ **.streamlit/config.toml** - Configurações do Streamlit

## 🔧 Troubleshooting:

### Se der erro de autenticação:
1. Configure suas credenciais do GitHub
2. Use um Personal Access Token se necessário
3. Configure SSH se preferir

### Se der erro de repositório já existente:
```cmd
git remote set-url origin https://github.com/luiginoIori/Comparadordearquivos.git
```

### Para verificar o status:
```cmd
git log --oneline
git branch -a
git remote -v
```

## 🌐 Após o Push:

O repositório estará disponível em:
**https://github.com/luiginoIori/Comparadordearquivos**

Você poderá:
- ✅ Clonar em outras máquinas
- ✅ Compartilhar o código
- ✅ Fazer backup na nuvem
- ✅ Colaborar com outros desenvolvedores
- ✅ Usar GitHub Pages para documentação

---

**💡 Dica**: Mantenha o repositório sempre atualizado com `git push` após mudanças!