# 📋 Guia de Instalação - Detector de Arquivos Duplicados

## 🔧 Pré-requisitos

### Python
- **Versão mínima:** Python 3.8+
- **Recomendado:** Python 3.9 ou superior

### Tkinter (Interface Gráfica)
O **tkinter** é necessário para o diálogo de seleção de pastas e já vem incluído na maioria das instalações do Python.

#### ✅ Verificar se tkinter está instalado:
```bash
python -c "import tkinter; print('Tkinter OK')"
```

#### ❌ Se tkinter não estiver disponível:

**Windows:**
```bash
# Reinstalar Python com tkinter incluído
# Baixar do site oficial: https://www.python.org/downloads/
# Marcar a opção "tcl/tk and IDLE" durante a instalação
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install python3-tk
```

**Linux (CentOS/RHEL):**
```bash
sudo yum install tkinter
# ou
sudo dnf install python3-tkinter
```

**macOS:**
```bash
# Tkinter já vem incluído na instalação padrão do Python
# Se houver problemas, reinstalar Python via Homebrew:
brew install python-tk
```

## 📦 Instalação das Dependências

### 1. Instalar dependências principais:
```bash
pip install -r requirements.txt
```

### 2. Verificar instalação:
```bash
streamlit --version
python -c "import pandas; print('Pandas OK')"
python -c "import tkinter; print('Tkinter OK')"
```

## 🚀 Executar a Aplicação

```bash
streamlit run app.py
```

## 🔍 Solução de Problemas

### Problema: "ModuleNotFoundError: No module named 'tkinter'"

**Soluções:**
1. **Windows:** Reinstalar Python com tkinter incluído
2. **Linux:** Instalar pacote tkinter via gerenciador de pacotes
3. **Alternativa:** Usar a opção "⌨️ Digitar Caminho" na aplicação

### Problema: Diálogo de pasta não abre

A aplicação possui três métodos de seleção de pasta:
1. **PowerShell (Windows)** - Método principal
2. **Tkinter** - Fallback automático
3. **Input manual** - Sempre disponível

### Problema: Erro de permissão

```bash
# Executar como administrador (Windows)
# ou
sudo python app.py  # Linux/macOS
```

## 📝 Notas Importantes

- O **tkinter** é parte da biblioteca padrão do Python
- Não é necessário instalar separadamente na maioria dos casos
- Se houver problemas, use as "Pastas Rápidas" ou "Digitar Caminho"
- A aplicação funciona mesmo sem tkinter (com funcionalidade reduzida)

## 🆘 Suporte

Se continuar com problemas:
1. Verifique a versão do Python: `python --version`
2. Teste a importação: `python -c "import tkinter"`
3. Use o método alternativo de entrada manual de caminho