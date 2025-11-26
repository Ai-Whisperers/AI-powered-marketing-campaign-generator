# Script to download recommended Ollama models for campaign generation
# Run this script to download all necessary models

$OLLAMA_PATH = "C:\Users\Alejandro\AppData\Local\Programs\Ollama\ollama.exe"

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "Downloading Ollama Models" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# 1. Llama 3.1 8B (Primary - Fast & Good Quality)
Write-Host "[1/3] Downloading llama3.1:8b (4.9 GB) - Primary model for research..." -ForegroundColor Yellow
& $OLLAMA_PATH pull llama3.1:8b
Write-Host "✅ llama3.1:8b downloaded!" -ForegroundColor Green
Write-Host ""

# 2. Mistral 7B (Spanish optimization)
Write-Host "[2/3] Downloading mistral:7b (4.1 GB) - Optimized for Spanish..." -ForegroundColor Yellow
& $OLLAMA_PATH pull mistral:7b
Write-Host "✅ mistral:7b downloaded!" -ForegroundColor Green
Write-Host ""

# 3. DeepSeek Coder (Code analysis - optional)
Write-Host "[3/3] Downloading deepseek-coder:6.7b (3.8 GB) - For code tasks..." -ForegroundColor Yellow
& $OLLAMA_PATH pull deepseek-coder:6.7b
Write-Host "✅ deepseek-coder:6.7b downloaded!" -ForegroundColor Green
Write-Host ""

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "All models downloaded successfully!" -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Installed models:" -ForegroundColor Cyan
& $OLLAMA_PATH list
