# 🧠 TheraScape - Complete Integration Guide

## 📋 **Integration Analysis Summary**

Your TheraScape application already has a solid foundation for integration between the Python Flask frontend and Java Spring Boot backend. Here's what I've analyzed and enhanced:

## 🏗️ **Current Architecture**

### **Python Flask Frontend (Port 5000)**

- ✅ AI-powered therapy chatbot using Google Gemini
- ✅ Comprehensive mood analysis and scene recommendations
- ✅ Video recommendation system
- ✅ Authentication service integration
- ✅ Therapeutic tools (breathing exercises, mindfulness, etc.)
- ✅ Session management and mood tracking

### **Java Spring Boot Backend (Port 8080)**

- ✅ User authentication with JWT tokens
- ✅ PostgreSQL database integration
- ✅ Video repository management
- ✅ RESTful API endpoints
- ✅ Security configuration with Spring Security

## 🔧 **New Enhancements Added**

### **1. Enhanced Java Backend**

```
New Files:
- MoodAnalysisController.java - Comprehensive mood analysis API
- MoodAnalysisService.java - Mood analysis business logic
- MoodEntry.java - Mood tracking entity
- MoodEntryRepository.java - Data access layer
- MoodAnalysisRequest.java & MoodAnalysisResponse.java - DTOs
```

### **2. Enhanced Python Frontend**

```
New Files:
- mood_tracking_service.py - Integration with Java mood analysis
- dashboard.html - Comprehensive user dashboard
- dashboard.css - Modern dashboard styling
New Routes:
- /dashboard - User analytics dashboard
- /api/mood-trends - Mood analytics API
- /api/dashboard - Dashboard data API
```

## 🚀 **Quick Start Guide**

### **Step 1: Prerequisites**

```bash
# Java 17+
java -version

# Python 3.8+
python --version

# PostgreSQL (running on port 5432)
psql --version

# Maven (or use included wrapper)
mvn --version
```

### **Step 2: Environment Setup**

**Create `.env` file in TherScape1 folder:**

```env
GOOGLE_API_KEY=your_google_api_key_here
JAVA_BACKEND_URL=http://localhost:8080
JAVA_BACKEND_TIMEOUT=10
ENABLE_JAVA_BACKEND=true
SECRET_KEY=your-secret-key-change-this-in-production
FLASK_ENV=development
FLASK_DEBUG=true
ENABLE_VIDEO_RECOMMENDATIONS=true
ENABLE_USER_AUTHENTICATION=true
```

### **Step 3: Database Setup**

**PostgreSQL Configuration:**

```sql
-- Create database
CREATE DATABASE therascapeLogin;

-- The application will auto-create tables via JPA
```

**Update application.properties if needed:**

```properties
spring.datasource.url=jdbc:postgresql://localhost:5432/therascapeLogin
spring.datasource.username=postgres
spring.datasource.password=root
```

### **Step 4: Start the Application**

**Option A: Use PowerShell Script (Windows)**

```powershell
.\start_therascape.ps1
```

**Option B: Manual Startup**

**Terminal 1 - Java Backend:**

```bash
cd therascape-backend
./mvnw spring-boot:run
```

**Terminal 2 - Python Frontend:**

```bash
cd TherScape1
pip install -r requirements.txt
python run.py
```

## 🌟 **Key Features**

### **1. Integrated User Authentication**

- Registration and login through Java backend
- JWT token management
- Session persistence in Flask
- Secure password handling

### **2. Comprehensive Mood Analysis**

- AI-powered mood detection using Google Gemini
- Mood tracking and analytics stored in PostgreSQL
- Crisis risk assessment
- Personalized therapeutic recommendations

### **3. Smart Video Recommendations**

- Mood-based video suggestions
- Integration with Java video repository
- Formatted responses for frontend display

### **4. User Dashboard**

- Real-time mood trends and analytics
- Interactive charts showing mood progression
- Personalized scene and video recommendations
- Wellness alerts and support resources

### **5. Therapeutic Tools Integration**

- Breathing exercises
- Mindfulness meditation
- Coping strategies
- Crisis support resources

## 📊 **API Endpoints Overview**

### **Python Flask APIs (Port 5000)**

```
GET  /                     - Landing page
GET  /auth                 - Authentication page
GET  /chat                 - Main chat interface
POST /chat                 - AI chatbot interaction
GET  /dashboard            - User dashboard
POST /api/register         - User registration (proxies to Java)
POST /api/login            - User login (proxies to Java)
GET  /api/mood-trends      - User mood analytics
GET  /api/dashboard        - Dashboard data
GET  /api/videos/mood/{mood} - Video recommendations
POST /api/mood-analysis    - Comprehensive mood analysis
```

### **Java Spring Boot APIs (Port 8080)**

```
POST /api/auth/register     - User registration
POST /api/auth/login        - User login
GET  /api/auth/check-username/{username} - Username availability
POST /api/mood/analyze      - Store mood analysis
GET  /api/mood/history/{userId} - User mood history
GET  /api/mood/trends/{userId}  - User mood trends
GET  /api/videos/mood/{category} - Videos by mood category
```

## 🔄 **Data Flow Examples**

### **User Registration Flow**

1. User submits form on `/auth` page
2. Flask receives request at `/api/register`
3. Flask forwards to Java backend `/api/auth/register`
4. Java validates, stores in PostgreSQL, returns JWT
5. Flask stores JWT in session, redirects to `/chat`

### **Chat with Mood Analysis Flow**

1. User sends message via `/chat` POST
2. Flask processes with Google Gemini AI
3. Flask analyzes mood and stores in Java backend
4. Java returns mood analysis and recommendations
5. Flask combines AI response with video/scene recommendations
6. Frontend displays integrated response

### **Dashboard Analytics Flow**

1. User visits `/dashboard`
2. Frontend calls `/api/dashboard`
3. Flask retrieves mood history from Java backend
4. Flask formats data for charts and analytics
5. Dashboard displays interactive mood trends and recommendations

## 🧪 **Testing the Integration**

### **Run Integration Tests**

```bash
cd TherScape1
python test_integration.py
```

### **Manual Testing Checklist**

- [ ] Java backend starts on port 8080
- [ ] Python frontend starts on port 5000
- [ ] User registration works
- [ ] User login receives JWT token
- [ ] Chat interface loads and responds
- [ ] Mood analysis is stored in database
- [ ] Dashboard shows user analytics
- [ ] Video recommendations work
- [ ] Scene recommendations display

## 📱 **User Experience Flow**

1. **Landing Page** (`/`) - User enters name and basic info
2. **Authentication** (`/auth`) - Registration or login
3. **Chat Interface** (`/chat`) - AI therapy sessions with mood tracking
4. **Dashboard** (`/dashboard`) - Analytics and progress tracking
5. **Therapeutic Tools** - Breathing exercises, mindfulness, etc.

## 🔒 **Security Features**

- JWT token authentication
- Session management
- CORS configuration for microservices
- Input validation and sanitization
- Crisis detection and intervention protocols
- Secure password handling with Spring Security

## 📈 **Monitoring & Analytics**

- User mood trends over time
- Session frequency and duration
- Crisis risk detection and alerts
- Therapeutic goal tracking
- Video engagement metrics

## 🚨 **Crisis Support Integration**

- Automatic crisis risk assessment
- Immediate intervention recommendations
- Crisis hotline integration (988)
- Professional support referrals
- Safety planning tools

## 🎯 **Next Steps for Enhancement**

### **Immediate Improvements**

1. Add more sophisticated AI mood analysis models
2. Implement real-time notifications
3. Add user profile customization
4. Enhance video recommendation algorithms

### **Advanced Features**

1. Voice message processing
2. Multi-language support
3. Mobile app API endpoints
4. Integration with wearable devices
5. Group therapy session support

### **Analytics & Monitoring**

1. Advanced user behavior analytics
2. Therapeutic outcome tracking
3. System performance monitoring
4. A/B testing for therapy approaches

## 📞 **Support & Troubleshooting**

### **Common Issues**

**"Connection Refused" Error:**

- Ensure Java backend is running on port 8080
- Check JAVA_BACKEND_URL in .env file
- Verify PostgreSQL is running

**"JWT Token Invalid" Error:**

- Check token expiration settings
- Verify JWT secret key consistency between services
- Clear browser cookies and re-login

**"Port Already in Use" Error:**

```bash
# Kill processes on specific ports
netstat -ano | findstr :8080
taskkill /F /PID <PID>
```

### **Development Tips**

1. **Enable Debug Mode:**

   ```env
   FLASK_DEBUG=true
   ```

2. **Monitor Logs:**

   - Java: Check console output for Spring Boot logs
   - Python: Flask logs appear in terminal
   - Database: Monitor PostgreSQL logs

3. **API Testing:**
   ```bash
   # Test registration
   curl -X POST http://localhost:5000/api/register \
     -H "Content-Type: application/json" \
     -d '{"username":"test","password":"pass123","email":"test@example.com","fullName":"Test User"}'
   ```

## 🎉 **Conclusion**

Your TheraScape application now has a complete, integrated architecture that combines:

- **AI-powered therapy chatbot** for personalized mental health support
- **Robust user management** with secure authentication
- **Comprehensive mood tracking** with analytics and insights
- **Intelligent recommendations** for videos and therapeutic scenes
- **Modern dashboard** for user progress tracking
- **Crisis support integration** for safety and intervention

The integration provides a seamless user experience while maintaining separate concerns between the AI/therapy logic (Python) and user/data management (Java).
