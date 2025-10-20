# 🔍 Detector de Arquivos Duplicados v2.0

Uma aplicação Streamlit intuitiva para detectar e gerenciar arquivos duplicados em pastas.

## ✨ Características

- 🔍 **Detecção Inteligente**: Usa hash MD5 para identificar duplicatas com precisão
- 📊 **Interface Amigável**: Interface web limpa e responsiva
- 🎯 **Seleção Individual**: Escolha exatamente quais arquivos mover
- 🚚 **Movimentação Segura**: Move duplicatas para pasta separada
- 📈 **Estatísticas Detalhadas**: Visualize espaço economizado e resumos
- 🔧 **Múltiplos Métodos**: Seleção de pasta via diálogo, entrada manual ou atalhos

## 🚀 Instalação Rápida

### Método 1: Script Automático (Recomendado)
```bash
# Windows
.\iniciar_com_venv.bat
```

### Método 2: Manual
```bash
# 1. Criar ambiente virtual
python -m venv .venv

# 2. Ativar ambiente (Windows)
.venv\Scripts\activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Executar aplicação
streamlit run app.py
```

## 📋 Pré-requisitos

- **Python 3.8+** (recomendado 3.9+)
- **tkinter** (geralmente incluído com Python)
- **Windows PowerShell** (para melhor experiência no Windows)

### ✅ Verificar Dependências
```bash
python --version          # Python 3.8+
python -c "import tkinter; print('Tkinter OK')"
```

## 📦 Dependências

| Pacote | Versão | Descrição |
|--------|---------|-----------|
| `streamlit` | ≥1.28.0 | Framework web principal |
| `pandas` | ≥2.0.0 | Manipulação de dados |
| `pathlib2` | ≥2.3.7 | Utilitários de sistema de arquivos |
| `tkinter` | Padrão | Interface gráfica (incluído no Python) |

## 🎯 Como Usar

1. **📁 Selecionar Pasta**
   - Clique "📁 Selecionar Pasta" para diálogo nativo
   - Use "📂 Pastas Rápidas" para locais comuns
   - Digite caminho manualmente com "⌨️ Digitar Caminho"

2. **🔍 Analisar**
   - Clique "🔍 Iniciar Análise"
   - Aguarde o processamento (com barra de progresso)

3. **📋 Revisar Resultados**
   - Veja estatísticas de duplicatas encontradas
   - Compare arquivos originais vs duplicados
   - Use botões de seleção rápida ou individual

4. **🚚 Mover Arquivos**
   - Selecione arquivos desejados
   - Clique "🚚 Mover Arquivos Selecionados"
   - Arquivos vão para pasta `ArquivosDuplicados`

## 🔧 Soluções de Problemas

### Tkinter não encontrado
```bash
# Windows: Reinstalar Python com tkinter
# Linux: sudo apt-get install python3-tk
# macOS: brew install python-tk
```

### Diálogo de pasta não abre
- Use **PowerShell** (método principal no Windows)
- **Fallback automático** para tkinter
- **Alternativa**: "⌨️ Digitar Caminho" ou "📂 Pastas Rápidas"

### Erro de permissão
```bash
# Executar como administrador (Windows)
# ou usar pasta sem restrições
```

## 📂 Estrutura do Projeto

```
ComparadorDeArquivo/
├── app.py                 # Aplicação principal
├── requirements.txt       # Dependências Python
├── iniciar_com_venv.bat  # Script de inicialização automática
├── INSTALACAO.md         # Guia detalhado de instalação
├── README.md             # Este arquivo
└── .venv/                # Ambiente virtual (criado automaticamente)
```

## 🎯 Recursos Avançados

- **🔄 Análise Recursiva**: Inclui subpastas automaticamente
- **📊 Métricas em Tempo Real**: Espaço economizado, arquivos únicos
- **🎯 Seleção Inteligente**: Recomenda duplicados mais recentes
- **💾 Backup Automático**: Histórico em JSON para auditoria
- **🎨 Interface Responsiva**: Design limpo e intuitivo

## 📝 Notas Importantes

- ⚠️ **Sempre faça backup** antes de mover arquivos importantes
- 🔍 **Verifique manualmente** antes de confirmar exclusões
- 📁 **Arquivos movidos** vão para `ArquivosDuplicados` (não são deletados)
- 🔄 **Arquivos são movidos**, não copiados (economiza espaço)

## 🆘 Suporte

Para problemas ou dúvidas:
1. Consulte `INSTALACAO.md` para guia detalhado
2. Verifique dependências com os comandos de teste
3. Use métodos alternativos de seleção de pasta se houver problemas

---

**Versão:** 2.0 | **Desenvolvido com:** ❤️ + Streamlit + Python