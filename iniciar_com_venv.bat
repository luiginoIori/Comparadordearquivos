@echo off
echo.
echo ========================================
echo  Detector de Arquivos Duplicados v2.0
echo ========================================
echo.

REM Verificar se o ambiente virtual existe
if not exist ".venv\" (
    echo [INFO] Criando ambiente virtual...
    python -m venv .venv
    echo [OK] Ambiente virtual criado
)

REM Ativar ambiente virtual
echo [INFO] Ativando ambiente virtual...
call .venv\Scripts\activate.bat

REM Verificar se tkinter está disponível
echo [INFO] Verificando tkinter...
python -c "import tkinter; print('[OK] Tkinter disponível')" 2>nul
if errorlevel 1 (
    echo [AVISO] Tkinter não encontrado. Funcionalidade de seleção de pasta pode estar limitada.
    echo         Use a opção "Digitar Caminho" ou "Pastas Rápidas" como alternativa.
)

REM Instalar/atualizar dependências
echo [INFO] Instalando dependências...
pip install -r requirements.txt

REM Verificar instalação
echo [INFO] Verificando instalação...
python -c "import streamlit; print('[OK] Streamlit instalado')"
python -c "import pandas; print('[OK] Pandas instalado')"

echo.
echo [INFO] Iniciando aplicação...
echo ========================================
echo  Aplicação será aberta no navegador
echo  URL: http://localhost:8501
echo ========================================
echo.

REM Executar aplicação
streamlit run app.py

echo.
echo [INFO] Aplicação finalizada
pause