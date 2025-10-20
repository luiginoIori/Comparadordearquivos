@echo off
echo ========================================
echo   Comparador de Arquivos Duplicados
echo ========================================
echo.
echo Iniciando o aplicativo...
echo.
echo O aplicativo sera aberto automaticamente no seu navegador.
echo Para encerrar, pressione Ctrl+C neste terminal.
echo.
echo ========================================
echo.

cd /d "%~dp0"
streamlit run app.py

pause