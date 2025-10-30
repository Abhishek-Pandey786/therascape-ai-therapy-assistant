#!/bin/bash

# TheraScape Full Application Startup Script
# This script helps you start both Java Spring Boot backend and Python Flask frontend

echo "🚀 TheraScape Full Application Startup"
echo "======================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to check if a port is in use
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null; then
        return 0
    else
        return 1
    fi
}

# Function to start Java backend
start_java_backend() {
    echo -e "${BLUE}📱 Starting Java Spring Boot Backend...${NC}"
    
    cd "therascape-backend"
    
    # Check if Maven wrapper exists
    if [ -f "./mvnw" ]; then
        echo "Using Maven wrapper..."
        ./mvnw spring-boot:run &
    elif command -v mvn &> /dev/null; then
        echo "Using system Maven..."
        mvn spring-boot:run &
    else
        echo -e "${RED}❌ Maven not found. Please install Maven or use the Maven wrapper.${NC}"
        return 1
    fi
    
    JAVA_PID=$!
    echo -e "${GREEN}✅ Java backend starting with PID: $JAVA_PID${NC}"
    
    # Wait for Java backend to start
    echo "Waiting for Java backend to start on port 8080..."
    for i in {1..30}; do
        if check_port 8080; then
            echo -e "${GREEN}✅ Java backend is ready on http://localhost:8080${NC}"
            break
        fi
        sleep 2
        echo -n "."
    done
    
    if ! check_port 8080; then
        echo -e "${RED}❌ Java backend failed to start on port 8080${NC}"
        return 1
    fi
    
    cd ..
    return 0
}

# Function to start Python frontend
start_python_frontend() {
    echo -e "${BLUE}🐍 Starting Python Flask Frontend...${NC}"
    
    cd "TherScape1"
    
    # Check if virtual environment exists
    if [ -d "venv" ]; then
        echo "Activating virtual environment..."
        source venv/bin/activate
    elif [ -d ".venv" ]; then
        echo "Activating virtual environment..."
        source .venv/bin/activate
    else
        echo -e "${YELLOW}⚠️  No virtual environment found. Using system Python.${NC}"
    fi
    
    # Check if requirements are installed
    if [ -f "requirements.txt" ]; then
        echo "Installing/updating requirements..."
        pip install -r requirements.txt
    fi
    
    # Check for .env file
    if [ ! -f ".env" ]; then
        echo -e "${YELLOW}⚠️  .env file not found. Creating from template...${NC}"
        cp .env.example .env 2>/dev/null || echo "Please create a .env file with your configuration."
    fi
    
    # Start Flask application
    echo "Starting Flask application..."
    python run.py &
    PYTHON_PID=$!
    
    echo -e "${GREEN}✅ Python frontend starting with PID: $PYTHON_PID${NC}"
    
    # Wait for Python frontend to start
    echo "Waiting for Python frontend to start on port 5000..."
    for i in {1..20}; do
        if check_port 5000; then
            echo -e "${GREEN}✅ Python frontend is ready on http://localhost:5000${NC}"
            break
        fi
        sleep 1
        echo -n "."
    done
    
    if ! check_port 5000; then
        echo -e "${RED}❌ Python frontend failed to start on port 5000${NC}"
        return 1
    fi
    
    cd ..
    return 0
}

# Function to check prerequisites
check_prerequisites() {
    echo -e "${BLUE}🔍 Checking prerequisites...${NC}"
    
    # Check Java
    if command -v java &> /dev/null; then
        JAVA_VERSION=$(java -version 2>&1 | head -n 1 | cut -d'"' -f2)
        echo -e "${GREEN}✅ Java found: $JAVA_VERSION${NC}"
    else
        echo -e "${RED}❌ Java not found. Please install Java 17 or higher.${NC}"
        return 1
    fi
    
    # Check Python
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version)
        echo -e "${GREEN}✅ Python found: $PYTHON_VERSION${NC}"
    elif command -v python &> /dev/null; then
        PYTHON_VERSION=$(python --version)
        echo -e "${GREEN}✅ Python found: $PYTHON_VERSION${NC}"
    else
        echo -e "${RED}❌ Python not found. Please install Python 3.8 or higher.${NC}"
        return 1
    fi
    
    # Check PostgreSQL (optional but recommended)
    if command -v psql &> /dev/null; then
        echo -e "${GREEN}✅ PostgreSQL found${NC}"
    else
        echo -e "${YELLOW}⚠️  PostgreSQL not found. Make sure it's running for the Java backend.${NC}"
    fi
    
    return 0
}

# Function to show application URLs
show_urls() {
    echo ""
    echo -e "${GREEN}🎉 TheraScape is now running!${NC}"
    echo "=============================="
    echo -e "${BLUE}Frontend (Python Flask):${NC} http://localhost:5000"
    echo -e "${BLUE}Backend API (Java Spring):${NC} http://localhost:8080"
    echo ""
    echo -e "${YELLOW}Available Pages:${NC}"
    echo "• Landing Page: http://localhost:5000/"
    echo "• Authentication: http://localhost:5000/auth"
    echo "• Chat Interface: http://localhost:5000/chat"
    echo "• Dashboard: http://localhost:5000/dashboard"
    echo "• Therapeutic Tools: http://localhost:5000/coping-strategies"
    echo ""
    echo -e "${YELLOW}API Endpoints:${NC}"
    echo "• Mood Analysis: http://localhost:5000/api/mood-analysis"
    echo "• User Registration: http://localhost:5000/api/register"
    echo "• User Login: http://localhost:5000/api/login"
    echo "• Video Recommendations: http://localhost:5000/api/videos/mood/{mood}"
    echo ""
}

# Function to handle cleanup
cleanup() {
    echo ""
    echo -e "${YELLOW}🛑 Shutting down TheraScape...${NC}"
    
    if [ ! -z "$JAVA_PID" ]; then
        echo "Stopping Java backend (PID: $JAVA_PID)..."
        kill $JAVA_PID 2>/dev/null
    fi
    
    if [ ! -z "$PYTHON_PID" ]; then
        echo "Stopping Python frontend (PID: $PYTHON_PID)..."
        kill $PYTHON_PID 2>/dev/null
    fi
    
    # Kill any remaining processes on our ports
    echo "Cleaning up ports..."
    lsof -ti:8080 | xargs kill -9 2>/dev/null || true
    lsof -ti:5000 | xargs kill -9 2>/dev/null || true
    
    echo -e "${GREEN}✅ Cleanup complete. Goodbye!${NC}"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Main execution
main() {
    echo -e "${BLUE}Starting TheraScape Full Application...${NC}"
    
    # Check prerequisites
    if ! check_prerequisites; then
        echo -e "${RED}❌ Prerequisites check failed. Please install required software.${NC}"
        exit 1
    fi
    
    # Check if ports are already in use
    if check_port 8080; then
        echo -e "${YELLOW}⚠️  Port 8080 is already in use. Stopping existing process...${NC}"
        lsof -ti:8080 | xargs kill -9 2>/dev/null || true
        sleep 2
    fi
    
    if check_port 5000; then
        echo -e "${YELLOW}⚠️  Port 5000 is already in use. Stopping existing process...${NC}"
        lsof -ti:5000 | xargs kill -9 2>/dev/null || true
        sleep 2
    fi
    
    # Start Java backend first
    if ! start_java_backend; then
        echo -e "${RED}❌ Failed to start Java backend. Exiting.${NC}"
        exit 1
    fi
    
    # Start Python frontend
    if ! start_python_frontend; then
        echo -e "${RED}❌ Failed to start Python frontend. Stopping Java backend.${NC}"
        kill $JAVA_PID 2>/dev/null
        exit 1
    fi
    
    # Show URLs and wait
    show_urls
    
    echo -e "${GREEN}Press Ctrl+C to stop both servers.${NC}"
    echo ""
    
    # Wait for user to stop
    wait
}

# Run main function
main "$@"
