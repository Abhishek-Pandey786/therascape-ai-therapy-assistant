# Simple Maven Installation Script for Windows
Write-Host "Installing Apache Maven..." -ForegroundColor Blue

# Variables
$MavenDir = "C:\Tools\Apache\Maven"
$MavenVersion = "3.9.10"
$MavenUrl = "https://archive.apache.org/dist/maven/maven-3/$MavenVersion/binaries/apache-maven-$MavenVersion-bin.zip"
$TempFile = "$env:TEMP\apache-maven-$MavenVersion-bin.zip"

try {
    # Create directory
    Write-Host "Creating Maven directory: $MavenDir" -ForegroundColor Green
    if (!(Test-Path $MavenDir)) {
        New-Item -ItemType Directory -Path $MavenDir -Force | Out-Null
    }

    # Download Maven
    Write-Host "Downloading Maven..." -ForegroundColor Yellow
    Invoke-WebRequest -Uri $MavenUrl -OutFile $TempFile -UseBasicParsing
    Write-Host "Download completed" -ForegroundColor Green

    # Extract Maven
    Write-Host "Extracting Maven..." -ForegroundColor Yellow
    Add-Type -AssemblyName System.IO.Compression.FileSystem
    [System.IO.Compression.ZipFile]::ExtractToDirectory($TempFile, $MavenDir)
    Write-Host "Extraction completed" -ForegroundColor Green

    # Set up environment
    $MavenHome = "$MavenDir\apache-maven-$MavenVersion"
    Write-Host "Maven Home: $MavenHome" -ForegroundColor Cyan

    # Set environment variables for current session
    $env:MAVEN_HOME = $MavenHome
    $env:PATH = "$MavenHome\bin;$env:PATH"

    # Set permanent environment variables
    Write-Host "Setting environment variables..." -ForegroundColor Yellow
    [Environment]::SetEnvironmentVariable("MAVEN_HOME", $MavenHome, [EnvironmentVariableTarget]::User)
    
    $CurrentPath = [Environment]::GetEnvironmentVariable("PATH", [EnvironmentVariableTarget]::User)
    if ($CurrentPath -notlike "*$MavenHome\bin*") {
        $NewPath = "$MavenHome\bin;$CurrentPath"
        [Environment]::SetEnvironmentVariable("PATH", $NewPath, [EnvironmentVariableTarget]::User)
        Write-Host "Added Maven to PATH" -ForegroundColor Green
    }

    # Clean up
    Remove-Item $TempFile -Force
    Write-Host "Cleaned up temporary files" -ForegroundColor Green

    # Test installation
    Write-Host "Testing Maven installation..." -ForegroundColor Yellow
    $MavenExe = "$MavenHome\bin\mvn.cmd"
    if (Test-Path $MavenExe) {
        Write-Host "Maven executable found: $MavenExe" -ForegroundColor Green
        & $MavenExe --version
        Write-Host ""
        Write-Host "Maven installation completed successfully!" -ForegroundColor Green
        Write-Host "Please restart PowerShell or run 'refreshenv' to use mvn command" -ForegroundColor Yellow
    } else {
        Write-Host "Maven executable not found" -ForegroundColor Red
    }

} catch {
    Write-Host "Installation failed: $($_.Exception.Message)" -ForegroundColor Red
}
