# 🌿 TheraScape - AI-Powered Therapy Assistant

> **A comprehensive mental health platform combining AI therapy, mood analysis, and immersive experiences**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Java](https://img.shields.io/badge/Java-17-orange.svg)](https://openjdk.org)
[![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.5.3-green.svg)](https://spring.io/projects/spring-boot)
[![Flask](https://img.shields.io/badge/Flask-3.1.1-lightgrey.svg)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🌟 Overview

TheraScape is a next-generation mental health platform that combines artificial intelligence, evidence-based therapeutic techniques, and modern web technologies to provide accessible, personalized mental health support.

### 🎯 Key Features

- **🤖 AI-Powered Conversations**: Advanced Gemini 2.5 Flash integration with therapeutic conversation patterns
- **🧠 Mood Analysis & Tracking**: Real-time emotional state detection and visualization
- **🎵 Therapeutic Resources**: Guided breathing exercises, mindfulness meditation, and coping strategies
- **🔐 Enterprise Security**: JWT authentication, secure session management, and data protection
- **🎨 Modern UI/UX**: Responsive design with accessibility features and voice interaction
- **🔗 Microservices Architecture**: Scalable Python frontend with Java Spring Boot backend
- **⚡ Crisis Intervention**: Built-in safety protocols and emergency resource recommendations

## 🏗️ Architecture

```
TheraScape/
├── 🐍 TherScape1/ (Python Flask Frontend)
│   ├── AI Chat Interface
│   ├── Mood Analysis Engine
│   ├── Therapeutic Tools
│   └── User Session Management
├── ☕ therascape-backend/ (Java Spring Boot)
│   ├── User Authentication
│   ├── Data Persistence (MongoDB)
│   ├── RESTful APIs
│   └── Security & Validation
└── 📚 Documentation & Deployment Scripts
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** with pip
- **Java 17** with Maven
- **MongoDB** (local or cloud)
- **Google Gemini API Key**

### 1. Clone the Repository

```bash
git clone https://github.com/sumith300/therascape.git
cd therascape
```

### 2. Setup Python Frontend

```bash
cd TherScape1
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Configure Environment

```bash
# Create .env file in TherScape1/
cp .env.example .env

# Add your API keys
GOOGLE_API_KEY=your_gemini_api_key_here
SECRET_KEY=your_secret_key_here
JAVA_BACKEND_URL=http://localhost:8080
```

### 4. Setup Java Backend

```bash
cd therascape-backend

# Configure MongoDB connection in src/main/resources/application.properties
spring.data.mongodb.uri=mongodb://localhost:27017/therascape

# Run the application
./mvnw spring-boot:run
```

### 5. Start the Frontend

```bash
cd TherScape1
python run.py
```

### 6. Access the Application

- **Frontend**: http://localhost:5000
- **Backend API**: http://localhost:8080
- **API Documentation**: http://localhost:8080/swagger-ui.html

## 🔧 Development Setup

### Python Development Environment

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Code formatting
black app/
flake8 app/

# Type checking
mypy app/
```

### Java Development Environment

```bash
# Run tests
./mvnw test

# Code formatting
./mvnw spring-javaformat:apply

# Build package
./mvnw clean package
```

## 📊 Technology Stack

### Frontend (Python)

- **Framework**: Flask 3.1.1
- **AI Integration**: Google Gemini 2.5 Flash via LangChain
- **UI**: HTML5, CSS3, JavaScript (Vanilla)
- **Speech**: Web Speech API
- **Charts**: Chart.js for mood visualization

### Backend (Java)

- **Framework**: Spring Boot 3.5.3
- **Security**: Spring Security with JWT
- **Database**: MongoDB with Spring Data
- **Validation**: Hibernate Validator
- **Build Tool**: Maven

### Infrastructure

- **Authentication**: JWT tokens
- **Session Management**: Flask sessions + MongoDB persistence
- **API Communication**: RESTful APIs with JSON
- **Deployment**: Docker-ready configuration

## 🎨 UI/UX Features

### 🌸 Therapeutic Design

- **Forest Theme**: Calming green color palette inspired by nature therapy
- **Accessibility**: WCAG 2.1 AA compliant design
- **Responsive**: Mobile-first approach with progressive enhancement
- **Voice Integration**: Hands-free interaction for accessibility

### 🧭 User Journey

1. **Landing Page**: Welcome with demo option
2. **Authentication**: Secure registration/login
3. **Chat Interface**: AI therapy conversations
4. **Mood Tracking**: Visual progress monitoring
5. **Therapeutic Tools**: Guided exercises and resources

## 🔐 Security & Privacy

### Data Protection

- **Encryption**: All sensitive data encrypted at rest and in transit
- **Session Security**: Secure session management with automatic expiration
- **Input Validation**: Comprehensive server-side validation
- **Crisis Detection**: Built-in safety protocols for mental health emergencies

### Compliance

- **HIPAA Ready**: Architecture designed for healthcare data compliance
- **GDPR Compliant**: User data control and deletion capabilities
- **Security Headers**: Comprehensive HTTP security headers
- **Rate Limiting**: API protection against abuse

## 📈 Performance

### Optimizations

- **Caching**: Intelligent caching for mood analysis and responses
- **Lazy Loading**: Progressive content loading for better UX
- **Connection Pooling**: Efficient database connections
- **Model Selection**: Smart AI model selection based on availability

### Monitoring

- **Health Checks**: Built-in health monitoring endpoints
- **Logging**: Structured logging for debugging and analytics
- **Metrics**: Performance metrics collection
- **Error Tracking**: Comprehensive error reporting

## 🧪 Testing

### Test Coverage

```bash
# Python tests
pytest tests/ --cov=app --cov-report=html

# Java tests
./mvnw test jacoco:report
```

### Test Types

- **Unit Tests**: Individual component testing
- **Integration Tests**: API and database integration
- **E2E Tests**: Full user journey testing
- **Security Tests**: Authentication and authorization testing

## 📚 API Documentation

### Core Endpoints

#### Authentication

- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User authentication
- `GET /api/auth/me` - Get current user

#### Mood Analysis

- `POST /api/mood-analysis` - Comprehensive mood analysis
- `GET /api/mood-categories` - Available mood categories
- `POST /api/crisis-assessment` - Crisis risk evaluation

#### Chat & Therapy

- `POST /api/chat` - AI therapy conversation
- `GET /api/videos/recommendations` - Therapeutic video suggestions
- `POST /api/session/save` - Save therapy session

For complete API documentation, visit the [API Documentation](Backend_Integration_API_Documentation.md).

## 🚀 Deployment

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build

# Production deployment
docker-compose -f docker-compose.prod.yml up -d
```

### Cloud Deployment

- **Frontend**: Heroku, Vercel, or AWS Elastic Beanstalk
- **Backend**: AWS EC2, Google Cloud Run, or Azure Container Instances
- **Database**: MongoDB Atlas, AWS DocumentDB, or Azure Cosmos DB

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Workflow

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Gemini API** for advanced AI capabilities
- **Spring Boot Team** for the excellent framework
- **Flask Community** for the lightweight web framework
- **Mental Health Professionals** who provided therapeutic guidance
- **Open Source Community** for the amazing tools and libraries

## 📞 Support

- **Documentation**: [Full Documentation](docs/)
- **Issues**: [GitHub Issues](https://github.com/sumith300/therascape/issues)
- **Discussions**: [GitHub Discussions](https://github.com/sumith300/therascape/discussions)
- **Email**: support@therascape.com

## 🎯 Future Roadmap

### Phase 1 (Current)

- ✅ AI Therapy Chat Interface
- ✅ Mood Analysis & Tracking
- ✅ User Authentication
- ✅ Therapeutic Resources

### Phase 2 (Next 3 months)

- 🔄 Unity AR/VR Integration
- 🔄 Mobile Application
- 🔄 Advanced Analytics Dashboard
- 🔄 Multi-language Support

### Phase 3 (6+ months)

- 📋 Healthcare Provider Integration
- 📋 Clinical Trial Support
- 📋 Wearable Device Integration
- 📋 Advanced AI Personalization

---

<div align="center">
  
**Built with ❤️ for Mental Health**

_TheraScape is designed to supplement, not replace, professional mental health care. Always consult with qualified healthcare providers for serious mental health concerns._

</div>
