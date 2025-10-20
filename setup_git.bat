@echo off
cd /d "g:\Meu Drive\Modelos IA\ComparadorDeArquivo"

echo ========================================
echo   Inicializando Repositorio Git
echo ========================================
echo.

echo Verificando se Git esta instalado...
git --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Git nao esta instalado ou nao esta no PATH
    echo Baixe o Git em: https://git-scm.com/downloads
    pause
    exit /b 1
)

echo Git encontrado! Continuando...
echo.

echo Inicializando Git...
git init

echo Configurando usuario...
git config user.name "Luigi Iori"
git config user.email "luiginolori@gmail.com"

echo Adicionando arquivos...
git add .

echo Verificando arquivos adicionados...
git status

echo Fazendo primeiro commit...
git commit -m "first commit - Comparador de Arquivos Duplicados"

echo Renomeando branch para main...
git branch -M main

echo Adicionando repositorio remoto...
git remote add origin https://github.com/luiginoIori/Comparadordearquivos.git

echo Verificando conexao com repositorio remoto...
git remote -v

echo Fazendo push...
git push -u origin main

if errorlevel 1 (
    echo.
    echo AVISO: Pode ser necessario configurar autenticacao
    echo Verifique: https://docs.github.com/en/authentication
) else (
    echo.
    echo ========================================
    echo   Processo concluido com sucesso!
    echo ========================================
    echo.
    echo Repositorio disponivel em:
    echo https://github.com/luiginoIori/Comparadordearquivos
)

echo.
pause