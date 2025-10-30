# TheraScape Full Application Startup Script for Windows PowerShell
# This script helps you start both Java Spring Boot backend and Python Flask frontend

Write-Host "🚀 TheraScape Full Application Startup" -ForegroundColor Blue
Write-Host "======================================" -ForegroundColor Blue

# Function to check if a port is in use
function Test-Port {
    param([int]$Port)
    try {
        $connection = Test-NetConnection -ComputerName localhost -Port $Port -WarningAction SilentlyContinue
        return $connection.TcpTestSucceeded
    }
    catch {
        return $false
    }
}

# Function to start Java backend
function Start-JavaBackend {
    Write-Host "📱 Starting Java Spring Boot Backend..." -ForegroundColor Cyan
    
    if (Test-Path "therascape-backend") {
        Set-Location "therascape-backend"
        
        # Check if Maven wrapper exists
        if (Test-Path "mvnw.cmd") {
            Write-Host "Using Maven wrapper..." -ForegroundColor Green
            $javaProcess = Start-Process -FilePath "mvnw.cmd" -ArgumentList "spring-boot:run" -PassThru -WindowStyle Minimized
        }
        elseif (Get-Command mvn -ErrorAction SilentlyContinue) {
            Write-Host "Using system Maven..." -ForegroundColor Green
            $javaProcess = Start-Process -FilePath "mvn" -ArgumentList "spring-boot:run" -PassThru -WindowStyle Minimized
        }
        else {
            Write-Host "❌ Maven not found. Please install Maven or use the Maven wrapper." -ForegroundColor Red
            Set-Location ".."
            return $null
        }
        
        Write-Host "✅ Java backend starting with PID: $($javaProcess.Id)" -ForegroundColor Green
        
        # Wait for Java backend to start
        Write-Host "Waiting for Java backend to start on port 8080..." -ForegroundColor Yellow
        for ($i = 1; $i -le 30; $i++) {
            if (Test-Port -Port 8080) {
                Write-Host "✅ Java backend is ready on http://localhost:8080" -ForegroundColor Green
                break
            }
            Start-Sleep -Seconds 2
            Write-Host "." -NoNewline
        }
        
        if (-not (Test-Port -Port 8080)) {
            Write-Host "❌ Java backend failed to start on port 8080" -ForegroundColor Red
            Set-Location ".."
            return $null
        }
        
        Set-Location ".."
        return $javaProcess
    }
    else {
        Write-Host "❌ therascape-backend directory not found!" -ForegroundColor Red
        return $null
    }
}

# Function to start Python frontend
function Start-PythonFrontend {
    Write-Host "🐍 Starting Python Flask Frontend..." -ForegroundColor Cyan
    
    if (Test-Path "TherScape1") {
        Set-Location "TherScape1"
        
        # Check if virtual environment exists
        if (Test-Path "venv") {
            Write-Host "Activating virtual environment..." -ForegroundColor Green
            & "venv\Scripts\Activate.ps1"
        }
        elseif (Test-Path ".venv") {
            Write-Host "Activating virtual environment..." -ForegroundColor Green
            & ".venv\Scripts\Activate.ps1"
        }
        else {
            Write-Host "⚠️  No virtual environment found. Using system Python." -ForegroundColor Yellow
        }
        
        # Check if requirements are installed
        if (Test-Path "requirements.txt") {
            Write-Host "Installing/updating requirements..." -ForegroundColor Green
            python -m pip install -r requirements.txt
        }
        
        # Check for .env file
        if (-not (Test-Path ".env")) {
            Write-Host "⚠️  .env file not found. Creating from template..." -ForegroundColor Yellow
            if (Test-Path ".env.example") {
                Copy-Item ".env.example" ".env"
            }
            else {
                Write-Host "Please create a .env file with your configuration." -ForegroundColor Yellow
            }
        }
        
        # Start Flask application
        Write-Host "Starting Flask application..." -ForegroundColor Green
        $pythonProcess = Start-Process -FilePath "python" -ArgumentList "run.py" -PassThru -WindowStyle Minimized
        
        Write-Host "✅ Python frontend starting with PID: $($pythonProcess.Id)" -ForegroundColor Green
        
        # Wait for Python frontend to start
        Write-Host "Waiting for Python frontend to start on port 5000..." -ForegroundColor Yellow
        for ($i = 1; $i -le 20; $i++) {
            if (Test-Port -Port 5000) {
                Write-Host "✅ Python frontend is ready on http://localhost:5000" -ForegroundColor Green
                break
            }
            Start-Sleep -Seconds 1
            Write-Host "." -NoNewline
        }
        
        if (-not (Test-Port -Port 5000)) {
            Write-Host "❌ Python frontend failed to start on port 5000" -ForegroundColor Red
            Set-Location ".."
            return $null
        }
        
        Set-Location ".."
        return $pythonProcess
    }
    else {
        Write-Host "❌ TherScape1 directory not found!" -ForegroundColor Red
        return $null
    }
}

# Function to check prerequisites
function Test-Prerequisites {
    Write-Host "🔍 Checking prerequisites..." -ForegroundColor Cyan
    
    # Check Java
    try {
        $javaVersion = java -version 2>&1 | Select-Object -First 1
        Write-Host "✅ Java found: $javaVersion" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ Java not found. Please install Java 17 or higher." -ForegroundColor Red
        return $false
    }
    
    # Check Python
    try {
        $pythonVersion = python --version 2>&1
        Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ Python not found. Please install Python 3.8 or higher." -ForegroundColor Red
        return $false
    }
    
    # Check PostgreSQL (optional but recommended)
    try {
        $postgresVersion = psql --version 2>&1
        Write-Host "✅ PostgreSQL found: $postgresVersion" -ForegroundColor Green
    }
    catch {
        Write-Host "⚠️  PostgreSQL not found. Make sure it's running for the Java backend." -ForegroundColor Yellow
    }
    
    return $true
}

# Function to show application URLs
function Show-URLs {
    Write-Host ""
    Write-Host "🎉 TheraScape is now running!" -ForegroundColor Green
    Write-Host "=============================="
    Write-Host "Frontend (Python Flask): http://localhost:5000" -ForegroundColor Cyan
    Write-Host "Backend API (Java Spring): http://localhost:8080" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Available Pages:" -ForegroundColor Yellow
    Write-Host "• Landing Page: http://localhost:5000/"
    Write-Host "• Authentication: http://localhost:5000/auth"
    Write-Host "• Chat Interface: http://localhost:5000/chat"
    Write-Host "• Dashboard: http://localhost:5000/dashboard"
    Write-Host "• Therapeutic Tools: http://localhost:5000/coping-strategies"
    Write-Host ""
    Write-Host "API Endpoints:" -ForegroundColor Yellow
    Write-Host "• Mood Analysis: http://localhost:5000/api/mood-analysis"
    Write-Host "• User Registration: http://localhost:5000/api/register"
    Write-Host "• User Login: http://localhost:5000/api/login"
    Write-Host "• Video Recommendations: http://localhost:5000/api/videos/mood/{mood}"
    Write-Host ""
}

# Function to handle cleanup
function Stop-TheraScape {
    param($JavaProcess, $PythonProcess)
    
    Write-Host ""
    Write-Host "🛑 Shutting down TheraScape..." -ForegroundColor Yellow
    
    if ($JavaProcess -and -not $JavaProcess.HasExited) {
        Write-Host "Stopping Java backend (PID: $($JavaProcess.Id))..." -ForegroundColor Yellow
        try {
            $JavaProcess.Kill()
            $JavaProcess.WaitForExit(5000)
        }
        catch {
            Write-Host "Force killing Java process..." -ForegroundColor Red
        }
    }
    
    if ($PythonProcess -and -not $PythonProcess.HasExited) {
        Write-Host "Stopping Python frontend (PID: $($PythonProcess.Id))..." -ForegroundColor Yellow
        try {
            $PythonProcess.Kill()
            $PythonProcess.WaitForExit(5000)
        }
        catch {
            Write-Host "Force killing Python process..." -ForegroundColor Red
        }
    }
    
    # Kill any remaining processes on our ports
    Write-Host "Cleaning up ports..." -ForegroundColor Yellow
    try {
        Get-Process | Where-Object {$_.ProcessName -eq "java"} | Where-Object {$_.MainWindowTitle -like "*spring-boot*"} | Stop-Process -Force -ErrorAction SilentlyContinue
        Get-Process | Where-Object {$_.ProcessName -eq "python"} | Where-Object {$_.MainWindowTitle -like "*flask*"} | Stop-Process -Force -ErrorAction SilentlyContinue
    }
    catch {
        # Ignore errors during cleanup
    }
    
    Write-Host "✅ Cleanup complete. Goodbye!" -ForegroundColor Green
}

# Main execution
Write-Host "Starting TheraScape Full Application..." -ForegroundColor Cyan

# Check prerequisites
if (-not (Test-Prerequisites)) {
    Write-Host "❌ Prerequisites check failed. Please install required software." -ForegroundColor Red
    exit 1
}

# Check if ports are already in use
if (Test-Port -Port 8080) {
    Write-Host "⚠️  Port 8080 is already in use. Please stop the existing process." -ForegroundColor Yellow
}

if (Test-Port -Port 5000) {
    Write-Host "⚠️  Port 5000 is already in use. Please stop the existing process." -ForegroundColor Yellow
}

# Start Java backend first
$javaProcess = Start-JavaBackend
if (-not $javaProcess) {
    Write-Host "❌ Failed to start Java backend. Exiting." -ForegroundColor Red
    exit 1
}

# Start Python frontend
$pythonProcess = Start-PythonFrontend
if (-not $pythonProcess) {
    Write-Host "❌ Failed to start Python frontend. Stopping Java backend." -ForegroundColor Red
    if ($javaProcess -and -not $javaProcess.HasExited) {
        $javaProcess.Kill()
    }
    exit 1
}

# Show URLs and wait
Show-URLs

Write-Host "Press Ctrl+C or close this window to stop both servers." -ForegroundColor Green
Write-Host ""

# Set up cleanup on exit
try {
    # Wait for user to stop (Ctrl+C)
    while ($true) {
        Start-Sleep -Seconds 1
        
        # Check if processes are still running
        if ($javaProcess.HasExited -and $pythonProcess.HasExited) {
            Write-Host "Both processes have exited." -ForegroundColor Yellow
            break
        }
    }
}
finally {
    Stop-TheraScape -JavaProcess $javaProcess -PythonProcess $pythonProcess
}
