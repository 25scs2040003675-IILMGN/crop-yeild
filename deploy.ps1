# 🚀 QUICK DEPLOYMENT SCRIPT
# Run this to deploy your Crop Yield Prediction System to Vercel

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   CROP YIELD PREDICTION DEPLOYMENT" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check if Git is installed
Write-Host "[1/5] Checking Git installation..." -ForegroundColor Yellow
if (Get-Command git -ErrorAction SilentlyContinue) {
    Write-Host "✓ Git is installed" -ForegroundColor Green
} else {
    Write-Host "✗ Git is not installed. Please install Git first:" -ForegroundColor Red
    Write-Host "  https://git-scm.com/download/win" -ForegroundColor Yellow
    exit
}

# Step 2: Initialize Git Repository
Write-Host ""
Write-Host "[2/5] Initializing Git repository..." -ForegroundColor Yellow

if (Test-Path ".git") {
    Write-Host "✓ Git repository already exists" -ForegroundColor Green
} else {
    git init
    Write-Host "✓ Git repository initialized" -ForegroundColor Green
}

# Step 3: Add files
Write-Host ""
Write-Host "[3/5] Adding files to Git..." -ForegroundColor Yellow
git add .
Write-Host "✓ Files added" -ForegroundColor Green

# Step 4: Commit
Write-Host ""
Write-Host "[4/5] Creating initial commit..." -ForegroundColor Yellow
git commit -m "Initial commit: Crop Yield Prediction System with Vercel deployment"
Write-Host "✓ Commit created" -ForegroundColor Green

# Step 5: Instructions for GitHub
Write-Host ""
Write-Host "[5/5] Next Steps:" -ForegroundColor Yellow
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  PUSH TO GITHUB" -ForegroundColor Cyan  
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Go to: https://github.com/new" -ForegroundColor White
Write-Host "2. Repository name: crop-yield-prediction" -ForegroundColor White
Write-Host "3. Click 'Create repository'" -ForegroundColor White
Write-Host "4. Run these commands:" -ForegroundColor White
Write-Host ""
Write-Host "   git remote add origin https://github.com/YOUR_USERNAME/crop-yield-prediction.git" -ForegroundColor Cyan
Write-Host "   git branch -M main" -ForegroundColor Cyan
Write-Host "   git push -u origin main" -ForegroundColor Cyan
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  DEPLOY TO VERCEL" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Go to: https://vercel.com" -ForegroundColor White
Write-Host "2. Click 'Sign Up' (use GitHub)" -ForegroundColor White
Write-Host "3. Click 'Add New...' -> 'Project'" -ForegroundColor White
Write-Host "4. Select 'crop-yield-prediction'" -ForegroundColor White
Write-Host "5. Click 'Deploy'" -ForegroundColor White
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  DONE!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Your project is ready for deployment! 🎉" -ForegroundColor Green
Write-Host ""
Write-Host "For detailed instructions, see:" -ForegroundColor Yellow
Write-Host "  DEPLOYMENT_GUIDE.md" -ForegroundColor Cyan
Write-Host ""
