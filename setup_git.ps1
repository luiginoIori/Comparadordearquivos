# Script PowerShell para configurar Git
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Inicializando Repositorio Git" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Mudar para o diretório do projeto
Set-Location "g:\Meu Drive\Modelos IA\ComparadorDeArquivo"
Write-Host "Diretório atual: $(Get-Location)" -ForegroundColor Green

# Adicionar título ao README
Write-Host "Adicionando título ao README..." -ForegroundColor Yellow
Add-Content -Path "README.md" -Value "# Comparadordearquivos"

# Inicializar Git
Write-Host "Inicializando Git..." -ForegroundColor Yellow
git init

# Configurar usuário (se necessário)
Write-Host "Configurando usuário..." -ForegroundColor Yellow
git config user.name "Luigi Iori"
git config user.email "luiginolori@gmail.com"

# Adicionar todos os arquivos
Write-Host "Adicionando arquivos ao staging..." -ForegroundColor Yellow
git add .

# Fazer commit
Write-Host "Fazendo primeiro commit..." -ForegroundColor Yellow
git commit -m "first commit"

# Renomear branch para main
Write-Host "Renomeando branch para main..." -ForegroundColor Yellow
git branch -M main

# Adicionar repositório remoto
Write-Host "Adicionando repositório remoto..." -ForegroundColor Yellow
git remote add origin https://github.com/luiginoIori/Comparadordearquivos.git

# Fazer push
Write-Host "Fazendo push para repositório remoto..." -ForegroundColor Yellow
git push -u origin main

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "   Processo concluído com sucesso!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Repositório disponível em:" -ForegroundColor Cyan
Write-Host "https://github.com/luiginoIori/Comparadordearquivos" -ForegroundColor Blue

Read-Host "Pressione Enter para continuar"