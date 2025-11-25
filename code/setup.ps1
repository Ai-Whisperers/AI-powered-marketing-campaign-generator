# Campaign Generator - Setup Script for Windows
# Run this script to configure the environment

Write-Host "Campaign Generator Setup" -ForegroundColor Cyan
Write-Host "========================" -ForegroundColor Cyan
Write-Host ""

# Check if .env exists
$envFile = ".env"
$envExample = ".env.example"

if (-not (Test-Path $envFile)) {
    Write-Host "Creating .env file from .env.example..." -ForegroundColor Yellow
    Copy-Item $envExample $envFile
    Write-Host "Created .env file" -ForegroundColor Green
} else {
    Write-Host ".env file already exists" -ForegroundColor Green
}

# Check for Google credentials JSON file
$googleCredFiles = Get-ChildItem -Path ".." -Filter "client_secret*.json" -ErrorAction SilentlyContinue
if ($googleCredFiles) {
    $credFile = $googleCredFiles[0]
    Write-Host "Found Google credentials file: $($credFile.Name)" -ForegroundColor Green

    # Parse the JSON file
    $credJson = Get-Content $credFile.FullName | ConvertFrom-Json

    if ($credJson.installed) {
        $clientId = $credJson.installed.client_id
        $clientSecret = $credJson.installed.client_secret

        Write-Host "Extracted Client ID: $($clientId.Substring(0, 20))..." -ForegroundColor Gray

        # Update .env file
        $envContent = Get-Content $envFile -Raw

        if ($envContent -match "GOOGLE_CLIENT_ID=") {
            $envContent = $envContent -replace "GOOGLE_CLIENT_ID=.*", "GOOGLE_CLIENT_ID=$clientId"
        } else {
            $envContent += "`nGOOGLE_CLIENT_ID=$clientId"
        }

        if ($envContent -match "GOOGLE_CLIENT_SECRET=") {
            $envContent = $envContent -replace "GOOGLE_CLIENT_SECRET=.*", "GOOGLE_CLIENT_SECRET=$clientSecret"
        } else {
            $envContent += "`nGOOGLE_CLIENT_SECRET=$clientSecret"
        }

        Set-Content $envFile $envContent
        Write-Host "Updated .env with Google credentials" -ForegroundColor Green
    }
} else {
    Write-Host "No Google credentials file found (client_secret*.json)" -ForegroundColor Yellow
    Write-Host "You'll need to configure Google Drive manually in n8n" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Starting Docker containers..." -ForegroundColor Cyan
docker-compose down 2>$null
docker-compose up -d

Write-Host ""
Write-Host "Waiting for services to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Check container status
$containers = docker-compose ps --format json | ConvertFrom-Json
Write-Host ""
Write-Host "Container Status:" -ForegroundColor Cyan
docker-compose ps

Write-Host ""
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Access your services:" -ForegroundColor Cyan

Write-Host "  API Docs:      http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "  1. Open http://localhost:5678" -ForegroundColor White
Write-Host "  2. Go to Settings > Credentials" -ForegroundColor White
Write-Host "  3. Add 'Google Drive OAuth2 API' credential" -ForegroundColor White
Write-Host "  4. Use Client ID and Secret from your .env file" -ForegroundColor White
Write-Host "  5. Click 'Sign in with Google' to authorize" -ForegroundColor White
Write-Host "  6. Import workflow from n8n/workflows/campaign-generator-gdrive.json" -ForegroundColor White
Write-Host ""
