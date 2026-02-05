# Push to GitHub Repository
# Repository: https://github.com/omkar191130/crop-yeild

Write-Host "Pushing code to GitHub..." -ForegroundColor Cyan

# Initialize Git
if (-not (Test-Path ".git")) {
    git init
}

# Add remote
$remote = git remote get-url origin 2>$null
if ($remote) {
    git remote remove origin
}
git remote add origin https://github.com/omkar191130/crop-yeild.git

# Push code
git add .
git commit -m "Vercel-ready deployment: Crop Yield Prediction System"
git branch -M main
git push -f origin main

Write-Host ""
Write-Host "SUCCESS! Code pushed to GitHub" -ForegroundColor Green
Write-Host "View at: https://github.com/omkar191130/crop-yeild" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next: Deploy on Vercel" -ForegroundColor Yellow
Write-Host "1. Visit https://vercel.com" -ForegroundColor White
Write-Host "2. Import crop-yeild repository" -ForegroundColor White
Write-Host "3. Click Deploy" -ForegroundColor White
