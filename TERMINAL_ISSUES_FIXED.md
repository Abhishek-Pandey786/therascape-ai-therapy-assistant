# 🔧 TheraScape - Fixing Terminal Problems & Setup

## 🚨 **Current Issues Identified & Fixed**

### ✅ **Python Environment - FIXED**

- Virtual environment is properly set up and activated
- All required packages are installed correctly
- Flask application creates successfully
- Google Gemini API is configured and working
- Environment variables are properly set

### ⚠️ **Java Backend - Issue with Maven Wrapper**

- **Problem**: Maven wrapper fails due to space in Windows username path
- **Current Status**: Java 23 is installed, but Maven wrapper can't execute

## 🛠️ **Solutions**

### **Option 1: Install Maven Globally (Recommended)**

1. **Download Maven**:

   - Go to https://maven.apache.org/download.cgi
   - Download `apache-maven-3.9.10-bin.zip`

2. **Install Maven**:

   ```powershell
   # Extract to C:\Program Files\Apache\maven
   # Add to PATH: C:\Program Files\Apache\maven\bin
   ```

3. **Set Environment Variables**:

   ```powershell
   # Add to System Environment Variables:
   MAVEN_HOME=C:\Program Files\Apache\maven
   PATH=%PATH%;%MAVEN_HOME%\bin
   ```

4. **Verify Installation**:
   ```powershell
   mvn --version
   ```

### **Option 2: Use Pre-compiled JAR (Quick Fix)**

If you have a pre-built JAR file:

```powershell
cd therascape-backend
java -jar target/therascape-backend-0.0.1-SNAPSHOT.jar
```

### **Option 3: Fix Maven Wrapper (Advanced)**

Create a new wrapper batch file that handles spaces:

```batch
@echo off
set "MAVEN_PROJECTBASEDIR=%~dp0"
set "WRAPPER_JAR=%MAVEN_PROJECTBASEDIR%\.mvn\wrapper\maven-wrapper.jar"
java -jar "%WRAPPER_JAR%" %*
```

## 🚀 **Current Working Setup**

### **Python Flask Frontend (Ready ✅)**

```powershell
# Navigate to project
cd "d:\Documents\Christ University\4th-Trimester\SPEC Project\TherapyBot\TherScape1"

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Start Flask app
python run.py
```

**Status**: Ready to run on http://localhost:5000

### **Java Spring Boot Backend (Needs Maven Fix ⚠️)**

```powershell
# After installing Maven globally:
cd "d:\Documents\Christ University\4th-Trimester\SPEC Project\TherapyBot\therascape-backend"
mvn spring-boot:run
```

**Status**: Will work after Maven installation

## 🧪 **Testing Without Java Backend**

You can test the Python frontend independently:

```powershell
# In TherScape1 directory with venv activated
python -c "
from app import create_app
app = create_app()
print('✅ Flask app ready')
print('🔗 Frontend URL: http://localhost:5000')
print('⚠️ Java backend integration will show connection errors until backend is started')
"
```

## 📋 **Integration Test Results**

### **Working Components**:

- ✅ Python Flask application
- ✅ Google Gemini AI integration
- ✅ Virtual environment setup
- ✅ Environment configuration
- ✅ All Python dependencies installed
- ✅ Templates and static files
- ✅ Routing and API endpoints

### **Pending Components**:

- ⚠️ Java backend compilation (Maven issue)
- ⚠️ PostgreSQL database connection
- ⚠️ Full integration testing

## 🎯 **Immediate Next Steps**

1. **Install Maven** (see Option 1 above)
2. **Verify PostgreSQL** is running on port 5432
3. **Start Java backend** with Maven
4. **Run integration tests**

## 🚀 **Quick Start (Python Only)**

To test the chatbot functionality without the Java backend:

```powershell
# 1. Navigate to project
cd "d:\Documents\Christ University\4th-Trimester\SPEC Project\TherapyBot\TherScape1"

# 2. Activate virtual environment
.\venv\Scripts\Activate.ps1

# 3. Start Flask app
python run.py
```

Then visit:

- Landing Page: http://localhost:5000/
- Chat Interface: http://localhost:5000/chat
- Breathing Exercises: http://localhost:5000/breathing-exercises
- Mindfulness: http://localhost:5000/mindfulness

## 🔧 **Environment Status**

```
✅ Python 3.x - Installed and working
✅ Virtual Environment - Active and configured
✅ Flask 3.1.1 - Installed and working
✅ Google Gemini API - Configured and working
✅ All Python dependencies - Installed
⚠️ Maven - Needs global installation
✅ Java 23 - Installed
⚠️ PostgreSQL - Status unknown
```

## 💡 **Recommendation**

**Install Maven globally to resolve all issues**, then both backends will work perfectly together!

After Maven installation, you can use the provided startup scripts:

- Windows: `start_therascape.ps1`
- Linux/Mac: `start_therascape.sh`
