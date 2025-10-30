# Maven Installation Script for Windows
# This script downloads and installs Apache Maven globally

Write-Host "🔧 Installing Apache Maven..." -ForegroundColor Blue

# Create installation directory
$MavenDir = "C:\Tools\Apache\Maven"
$MavenVersion = "3.9.10"
$MavenUrl = "https://archive.apache.org/dist/maven/maven-3/$MavenVersion/binaries/apache-maven-$MavenVersion-bin.zip"
$TempFile = "$env:TEMP\apache-maven-$MavenVersion-bin.zip"

Write-Host "📁 Creating Maven directory: $MavenDir" -ForegroundColor Green

try {
    # Create directory if it doesn't exist
    if (!(Test-Path $MavenDir)) {
        New-Item -ItemType Directory -Path $MavenDir -Force | Out-Null
        Write-Host "✅ Directory created successfully" -ForegroundColor Green
    }

    # Download Maven
    Write-Host "📥 Downloading Maven $MavenVersion..." -ForegroundColor Yellow
    Write-Host "URL: $MavenUrl" -ForegroundColor Gray
    
    Invoke-WebRequest -Uri $MavenUrl -OutFile $TempFile -UseBasicParsing
    Write-Host "✅ Download completed" -ForegroundColor Green

    # Extract Maven
    Write-Host "📦 Extracting Maven..." -ForegroundColor Yellow
    Add-Type -AssemblyName System.IO.Compression.FileSystem
    [System.IO.Compression.ZipFile]::ExtractToDirectory($TempFile, $MavenDir)
    Write-Host "✅ Extraction completed" -ForegroundColor Green

    # Set up Maven directory
    $MavenHome = "$MavenDir\apache-maven-$MavenVersion"
    Write-Host "🏠 Maven Home: $MavenHome" -ForegroundColor Cyan

    # Add to PATH (current session)
    $env:MAVEN_HOME = $MavenHome
    $env:PATH = "$MavenHome\bin;$env:PATH"

    # Set permanent environment variables
    Write-Host "🔧 Setting environment variables..." -ForegroundColor Yellow
    
    # Set MAVEN_HOME
    [Environment]::SetEnvironmentVariable("MAVEN_HOME", $MavenHome, [EnvironmentVariableTarget]::User)
    
    # Get current PATH
    $CurrentPath = [Environment]::GetEnvironmentVariable("PATH", [EnvironmentVariableTarget]::User)
    
    # Add Maven to PATH if not already there
    if ($CurrentPath -notlike "*$MavenHome\bin*") {
        $NewPath = "$MavenHome\bin;$CurrentPath"
        [Environment]::SetEnvironmentVariable("PATH", $NewPath, [EnvironmentVariableTarget]::User)
        Write-Host "✅ Added Maven to PATH" -ForegroundColor Green
    } else {
        Write-Host "✅ Maven already in PATH" -ForegroundColor Green
    }

    # Clean up
    Remove-Item $TempFile -Force
    Write-Host "🧹 Cleaned up temporary files" -ForegroundColor Green

    # Test Maven installation
    Write-Host "🧪 Testing Maven installation..." -ForegroundColor Yellow
    $MavenExe = "$MavenHome\bin\mvn.cmd"
    if (Test-Path $MavenExe) {
        Write-Host "✅ Maven executable found: $MavenExe" -ForegroundColor Green
        
        # Test Maven version
        & $MavenExe --version
        
        Write-Host ""
        Write-Host "🎉 Maven installation completed successfully!" -ForegroundColor Green
        Write-Host "📝 Please restart your PowerShell session or run:" -ForegroundColor Yellow
        Write-Host "   refreshenv" -ForegroundColor Cyan
        Write-Host "   or close and reopen PowerShell" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "🚀 Then you can use: mvn --version" -ForegroundColor Yellow
        
    } else {
        Write-Host "❌ Maven executable not found" -ForegroundColor Red
    }

} catch {
    Write-Host "❌ Installation failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "📋 Installation Summary:" -ForegroundColor Blue
Write-Host "Maven Home: $MavenHome" -ForegroundColor Gray
Write-Host "Maven Bin: $MavenHome\bin" -ForegroundColor Gray
Write-Host "Environment variables set for current user" -ForegroundColor Gray
