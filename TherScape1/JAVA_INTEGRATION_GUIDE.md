# TheraScape Integration Guide: Python Flask + Java Spring Boot

## 🏗️ **Architecture Overview**

This integration combines the best of both worlds:

- **Python Flask** (Port 5000): AI/Therapy features with Google Gemini
- **Java Spring Boot** (Port 8080): User management, authentication, and data persistence

## 🚀 **Quick Setup Guide**

### **1. Install Dependencies**

```bash
# In your Python Flask project
pip install -r requirements.txt
```

### **2. Environment Configuration**

Create a `.env` file in your Flask project root:

```env
# Google API Configuration
GOOGLE_API_KEY=your_google_api_key_here

# Java Backend Configuration
JAVA_BACKEND_URL=http://localhost:8080
JAVA_BACKEND_TIMEOUT=10
ENABLE_JAVA_BACKEND=true

# Flask Configuration
SECRET_KEY=your-secret-key-change-this
FLASK_ENV=development

# Feature Flags
ENABLE_VIDEO_RECOMMENDATIONS=true
ENABLE_USER_AUTHENTICATION=true
```

### **3. Start Both Backends**

**Terminal 1 - Java Spring Boot:**

```bash
cd /path/to/therascape-backend
./mvnw spring-boot:run
# Or: java -jar target/therascape-backend-0.0.1-SNAPSHOT.jar
```

**Terminal 2 - Python Flask:**

```bash
cd /path/to/TherScape1
python run.py
```

## 🔧 **Integration Features Implemented**

### **1. User Authentication Service**

- Registration via Java backend
- JWT-based login system
- Session management in Flask
- Automatic token validation

### **2. Video Recommendation Service**

- Mood-based video suggestions
- Integration with Java video repository
- Formatted responses for frontend

### **3. Enhanced Chat API**

- Video recommendations in chat responses
- User session tracking
- Mood-based content delivery

### **4. Unified Frontend**

- Authentication page (`/auth`)
- Seamless user experience
- Error handling and loading states

## 📡 **API Endpoints**

### **Python Flask Endpoints (Port 5000):**

```
GET  /                     - Landing page
GET  /auth                 - Authentication page
GET  /chat                 - Main chat interface
POST /chat                 - Send message to AI therapist
POST /api/register         - Register user (proxies to Java)
POST /api/login            - Login user (proxies to Java)
GET  /api/videos/mood/{mood} - Get video recommendations
GET  /logout               - Logout and clear session
```

### **Java Spring Boot Endpoints (Port 8080):**

```
POST /api/auth/register           - User registration
POST /api/auth/login              - User login
GET  /api/auth/check-username/{username} - Check username availability
GET  /api/auth/check-email/{email}       - Check email availability
GET  /api/users/{id}              - Get user by ID
GET  /api/users/username/{username} - Get user by username
GET  /api/videos/mood/{category}  - Get videos by mood category
```

## 🔄 **Data Flow**

### **User Registration/Login:**

1. User submits form on `/auth` page
2. Flask receives request at `/api/register` or `/api/login`
3. Flask forwards request to Java backend
4. Java backend validates and returns JWT token
5. Flask stores token in session
6. User redirected to `/chat`

### **Chat Interaction:**

1. User sends message via `/chat` POST
2. Flask processes message with Google Gemini
3. Flask analyzes mood and gets video recommendations from Java
4. Combined response sent to frontend
5. Frontend displays AI response + video suggestions

## 🛠️ **Customization Options**

### **Adding New Features**

1. **Add New API Endpoints:**

```python
# In app/routes.py
@main.route('/api/new-feature', methods=['POST'])
def new_feature():
    # Your implementation
    return jsonify({'success': True})
```

2. **Extend Video Service:**

```python
# In app/services/video_service.py
def get_videos_by_custom_criteria(self, criteria):
    # Custom video filtering logic
    pass
```

3. **Add New Authentication Methods:**

```python
# In app/services/auth_service.py
def oauth_login(self, provider, token):
    # OAuth integration
    pass
```

## 🔒 **Security Considerations**

### **JWT Token Management**

- Tokens stored in Flask session (server-side)
- Automatic token validation before protected requests
- Configurable token expiration

### **CORS Configuration**

- Restricted to specific origins
- Configured for microservices communication
- Environment-specific settings

### **Input Validation**

- All user inputs validated
- SQL injection protection via JPA
- XSS prevention in templates

## 📊 **Database Schema (Java Backend)**

### **Users Table:**

```sql
CREATE TABLE users (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255),
    active BOOLEAN DEFAULT TRUE
);
```

### **Videos Table:**

```sql
CREATE TABLE videos (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    mood_category VARCHAR(255),
    video_url VARCHAR(500),
    title VARCHAR(255),
    description TEXT
);
```

## 🧪 **Testing Integration**

### **Test User Registration:**

```bash
curl -X POST http://localhost:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"password123","email":"test@example.com","fullName":"Test User"}'
```

### **Test Login:**

```bash
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"password123"}'
```

### **Test Video Recommendations:**

```bash
curl http://localhost:5000/api/videos/mood/happy
```

## 🚀 **Deployment Strategy**

### **Docker Deployment**

**Python Flask Dockerfile:**

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "run.py"]
```

**Docker Compose:**

```yaml
version: "3.8"
services:
  java-backend:
    build: ./therascape-backend
    ports:
      - "8080:8080"
    environment:
      - SPRING_PROFILES_ACTIVE=production

  python-frontend:
    build: ./TherScape1
    ports:
      - "5000:5000"
    environment:
      - JAVA_BACKEND_URL=http://java-backend:8080
    depends_on:
      - java-backend
```

## 🎯 **Next Steps & Enhancements**

### **Immediate Improvements:**

1. **Add user profile management**
2. **Implement chat history persistence**
3. **Add real-time notifications**
4. **Enhance video recommendation algorithm**

### **Advanced Features:**

1. **Voice message processing**
2. **Multi-language support**
3. **Advanced analytics dashboard**
4. **Mobile app API endpoints**

### **Monitoring & Analytics:**

1. **User engagement tracking**
2. **Mood analysis trends**
3. **System performance monitoring**
4. **Error logging and alerting**

## 📞 **Support & Troubleshooting**

### **Common Issues:**

1. **Connection Refused Error:**

   - Ensure Java backend is running on port 8080
   - Check JAVA_BACKEND_URL in environment

2. **JWT Token Invalid:**

   - Check token expiration settings
   - Verify JWT secret key consistency

3. **CORS Errors:**
   - Update CORS origins in configuration
   - Check browser developer tools

### **Debugging:**

- Enable Flask debug mode: `FLASK_ENV=development`
- Check Java backend logs for authentication issues
- Monitor network requests in browser dev tools

This integration provides a robust, scalable foundation for your therapy chatbot with proper user management, video recommendations, and seamless user experience!
