# Guia de Uso - Navegador de Pastas

## 🎯 Novas Funcionalidades de Seleção de Pastas

### 📁 **Navegador Gráfico**
- Clique no botão **📁 Navegar** para abrir o seletor nativo do Windows
- Navegue pelas pastas usando a interface familiar do Windows
- Selecione a pasta desejada e clique em "OK"

### ⌨️ **Entrada Manual**
- Clique no botão **⌨️** para ativar o modo de entrada manual
- Digite o caminho completo da pasta (ex: `C:\Meus Documentos`)
- O sistema valida automaticamente se a pasta existe

### 🔗 **Pastas Comuns**
Acesso rápido aos locais mais utilizados:
- 🏠 **Pasta do Usuário**: Sua pasta pessoal
- 🖥️ **Área de Trabalho**: Desktop do Windows
- 📁 **Documentos**: Pasta de documentos
- ⬇️ **Downloads**: Pasta de downloads
- 🖼️ **Imagens**: Pasta de imagens
- 💾 **Drives**: Todos os drives disponíveis (C:, D:, etc.)

### 🗑️ **Gerenciamento**
- **🗑️ Limpar**: Remove a seleção atual
- **Validação Automática**: Verifica se as pastas existem
- **Feedback Visual**: Indicadores de status (✅ válida, ❌ inválida)

## 🚀 **Como Usar**

### Passo 1: Selecionar Pasta de Origem
1. Na barra lateral, localize "🗂️ Pasta de Origem"
2. Escolha um dos métodos:
   - **📁 Navegar**: Para usar o seletor gráfico
   - **⌨️ Manual**: Para digitar o caminho
   - **🔗 Pasta Comum**: Para acesso rápido
3. Confirme que aparece ✅ "Pasta válida!"

### Passo 2: Selecionar Pasta de Comparação
1. Localize "🔍 Pasta para Comparação"
2. Repita o processo da pasta de origem
3. Pode ser a mesma pasta ou uma diferente

### Passo 3: Iniciar Análise
1. Com ambas as pastas selecionadas, clique em "🔍 Iniciar Análise"
2. Aguarde o processamento
3. Visualize os resultados

## 💡 **Dicas Importantes**

### ✅ **Melhores Práticas**
- Use pastas diferentes para comparação mais eficaz
- Pastas com muitos arquivos podem demorar mais para processar
- Mantenha backup dos arquivos antes de excluir duplicados

### ⚠️ **Solução de Problemas**
- Se o navegador gráfico não abrir, use a entrada manual
- Verifique se você tem permissão de acesso às pastas
- Caminhos com caracteres especiais devem usar aspas

### 🎯 **Exemplos Práticos**

**Limpeza de Downloads:**
- Origem: `C:\Users\[Seu Nome]\Downloads`
- Comparação: `D:\Backup\Downloads`

**Organização de Fotos:**
- Origem: `C:\Users\[Seu Nome]\Pictures`
- Comparação: `E:\Fotos Backup`

**Documentos Duplicados:**
- Origem: `C:\Users\[Seu Nome]\Documents`
- Comparação: `\\Servidor\Documentos`

---

**💡 Lembre-se**: O sistema compara nome, tamanho, data e conteúdo (hash MD5) para garantir 100% de precisão na detecção de duplicados!