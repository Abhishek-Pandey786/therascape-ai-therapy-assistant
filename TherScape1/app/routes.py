from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from app.models.therapy_bot import get_chat_response, analyze_mood, combine_emotional_context
from app.models.mood_scene_mapping import mood_scene_mapper, MoodCategory
from app.services.auth_service import auth_service
from app.services.enhanced_video_service import enhanced_video_service
from app.services.mood_tracking_service import mood_tracking_service
from datetime import datetime
import os

main = Blueprint('main', __name__)

@main.route('/')
def landing():
    """Landing page where users enter their name and gender"""
    return render_template('landing.html')

@main.route('/auth')
@main.route('/auth/<mode>')
def auth_page(mode='login'):
    return render_template('auth.html', mode=mode)

@main.route('/demo')
def demo():
    return render_template('demo.html')

@main.route('/chat')
def index():
    """Main chat interface"""
    # Check if user is authenticated or in demo mode
    user_data = session.get('user_data')
    demo_mode = session.get('demoMode') == 'true'
    
    if not user_data and not demo_mode:
        # If not authenticated and not in demo mode, redirect to auth
        return redirect(url_for('main.auth_page'))
    
    # Initialize mood data if it doesn't exist
    if 'mood_data' not in session:
        session['mood_data'] = []
    
    # Prepare user context for template
    user_context = {}
    if user_data:
        # Authenticated user
        user_context = {
            'name': user_data.get('name', user_data.get('username', 'User')),
            'mode': user_data.get('mode', 'authenticated'),
            'save_session': True
        }
    elif demo_mode:
        # Demo mode user
        user_context = {
            'name': user_data.get('name', 'Guest') if user_data else 'Guest',
            'mode': 'demo',
            'save_session': False
        }
    
    return render_template('index.html', user=user_context)

@main.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    user_name = data.get('userName', None)
    
    # Get user information from session
    user_data = session.get('user_data')
    demo_mode = session.get('demoMode') == 'true'
    
    # Validate session integrity for authenticated users
    if user_data and not demo_mode:
        current_session_id = session.get('session_id')
        current_username = user_data.get('username')
        
        if current_session_id and current_username:
            if not current_session_id.startswith(current_username):
                # Session mismatch - create new session for this user
                import uuid
                import time
                session['session_id'] = f"{current_username}_{str(uuid.uuid4())[:8]}_{int(time.time())}"
                session['conversation'] = []
                session['mood_data'] = []
                print(f"Session mismatch fixed for user: {current_username}")
    
    # Determine user name based on session data
    if user_data and 'name' in user_data:
        # Use name from session (demo or authenticated)
        current_user_name = user_data['name']
    elif user_name:
        # Fallback to provided userName (legacy support)
        current_user_name = user_name
        session['user_name'] = user_name
    else:
        # Default fallback
        current_user_name = 'Guest' if demo_mode else 'User'
    
    # Update session with current user name
    session['user_name'] = current_user_name
    
    # Get conversation history from session or initialize
    if 'conversation' not in session:
        session['conversation'] = []
    
    # Create a unique session ID for each new conversation if not exists
    if 'session_id' not in session:
        import uuid
        import time
        if user_data and user_data.get('username'):
            username = user_data.get('username')
            session['session_id'] = f"{username}_{str(uuid.uuid4())[:8]}_{int(time.time())}"
        else:
            session['session_id'] = f"guest_{str(uuid.uuid4())[:8]}_{int(time.time())}"
    
    # Add user message to conversation
    session['conversation'].append({
        'role': 'user',
        'content': user_message
    })
    
    # Analyze emotional context
    emotional_context = analyze_mood(user_message)
    
    # Get comprehensive mood analysis with scene recommendations
    analysis_result = mood_scene_mapper.analyze_mood_for_backend(
        mood_text=user_message,
        intensity=5,  # Default intensity, could be enhanced with user input
        user_preferences=session.get('user_preferences', {})
    )
    
    # Get response from therapy bot
    try:
        messages = session['conversation']
        # Add emotional context to the last message
        messages[-1]['emotionalContext'] = emotional_context
        
        # Pass user_name and session_id to the bot
        bot_response = get_chat_response(messages, user_name=current_user_name, session_id=session['session_id'])
        
        # Add bot response to conversation
        session['conversation'].append({
            'role': 'assistant',
            'content': bot_response,
            'emotionalContext': emotional_context
        })
        
        # Store mood data in local session
        store_mood_data(emotional_context)
        
        # Enhanced: Store mood analysis in Java backend
        if session.get('user_data'):
            mood_storage_result = mood_tracking_service.store_mood_analysis(
                text=user_message,
                mood_data={
                    'intensity': analysis_result.mood_category.value if hasattr(analysis_result, 'mood_category') else 5,
                    'preferences': session.get('user_preferences', {})
                }
            )
        
        # Import video recommendation intelligence
        from app.models.therapy_bot import should_recommend_video, get_video_recommendation_context
        
        # Get current conversation from session
        conversation = session.get('conversation', [])
        
        # Check if video has already been recommended in this conversation
        videos_recommended_count = session.get('videos_recommended_count', 0)
        
        # Check if video should be recommended based on therapeutic guidelines
        should_recommend, recommendation_reason = should_recommend_video(
            user_message, 
            conversation, 
            emotional_context
        )
        
        # Enforce max 1 video per conversation rule unless user explicitly asks for more
        user_asks_for_more = any(phrase in user_message.lower() for phrase in [
            'another video', 'more videos', 'different video', 'show me more', 'other videos'
        ])
        
        if should_recommend and videos_recommended_count >= 1 and not user_asks_for_more:
            should_recommend = False
            recommendation_reason = "Already recommended video in this conversation"
        
        formatted_videos = []
        
        if should_recommend:
            print(f"Video recommendation triggered: {recommendation_reason}")
            
            # Get video recommendations based on detected emotion
            # Enhanced: Get personalized video recommendations
            try:
                video_context = get_video_recommendation_context(emotional_context, user_message)
                
                if session.get('authenticated', False) and session.get('user_data'):
                    username = session['user_data']['username']
                    video_recommendations = enhanced_video_service.get_personalized_video_recommendations(
                        username, analysis_result, max_duration=20
                    )
                else:
                    # For demo users, get quick help videos
                    video_recommendations = enhanced_video_service.get_quick_help_videos(emotional_context)
                
                formatted_videos = video_recommendations[:3]  # Top 3 videos
                
                # Increment video recommendation count
                session['videos_recommended_count'] = videos_recommended_count + 1
                
            except Exception as e:
                print(f"Video service error: {e}")
                # Fallback to mock data for testing when Java backend is not available
                formatted_videos = get_mock_video_recommendations(emotional_context)
                if formatted_videos:
                    session['videos_recommended_count'] = videos_recommended_count + 1
            
            # If no videos from service, use mock data
            if not formatted_videos:
                formatted_videos = get_mock_video_recommendations(emotional_context)
                if formatted_videos:
                    session['videos_recommended_count'] = videos_recommended_count + 1
        else:
            print(f"Video recommendation not triggered: {recommendation_reason}")
            # No videos recommended - empty list
        
        # Export comprehensive analysis for potential backend use
        backend_data = mood_scene_mapper.export_for_backend(analysis_result)
        
        return jsonify({
            'response': bot_response,
            'emotion': emotional_context,
            'videos': formatted_videos,  # Frontend expects 'videos' key
            'mood_analysis': backend_data,
            'crisis_risk': analysis_result.crisis_risk,
            'scene_recommendations': [
                {
                    'sceneType': rec.scene_type.value,
                    'priority': rec.priority,
                    'description': rec.description
                }
                for rec in analysis_result.scene_recommendations[:2]  # Top 2 recommendations
            ],
            'success': True
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 500

@main.route('/get_mood_data', methods=['GET'])
def get_mood_data():
    """Route to retrieve user mood data"""
    mood_data = session.get('mood_data', [])
    return jsonify({
        'mood_data': mood_data,
        'success': True
    })

@main.route('/get_conversation_history', methods=['GET'])
def get_conversation_history():
    """Route to retrieve conversation history for chat persistence"""
    # Check if user is in demo mode
    demo_mode = session.get('demoMode') == 'true'
    user_data = session.get('user_data')
    
    # Ensure user is properly authenticated
    if not user_data and not demo_mode:
        return jsonify({
            'success': False,
            'message': 'User not authenticated'
        }), 401
    
    # For demo mode, only return conversation if it exists in current session
    # For authenticated users, return conversation history
    conversation = session.get('conversation', [])
    user_name = session.get('user_name', 'Guest')
    current_session_id = session.get('session_id')
    
    # Validate that the conversation belongs to the current user
    if user_data:
        current_username = user_data.get('username')
        if current_session_id and current_username:
            # Check if session ID matches current user
            if not current_session_id.startswith(current_username):
                # Session mismatch - clear conversation
                session['conversation'] = []
                conversation = []
                print(f"Session mismatch detected. Cleared conversation for user: {current_username}")
    
    # Format conversation for frontend display
    formatted_conversation = []
    for message in conversation:
        if message['role'] == 'user':
            formatted_conversation.append({
                'sender': 'user',
                'content': message['content'],
                'timestamp': datetime.now().isoformat()
            })
        elif message['role'] == 'assistant':
            formatted_conversation.append({
                'sender': 'bot',
                'content': message['content'],
                'timestamp': datetime.now().isoformat(),
                'emotion': message.get('emotionalContext', None)
            })
    
    return jsonify({
        'conversation': formatted_conversation,
        'user_name': user_name,
        'session_id': current_session_id,
        'demo_mode': demo_mode,
        'success': True
    })

@main.route('/check_previous_conversation', methods=['GET'])
def check_previous_conversation():
    """Route to check if user has previous conversation history"""
    # Only check for authenticated users (not demo mode)
    user_data = session.get('user_data')
    demo_mode = session.get('demoMode') == 'true'
    
    if demo_mode or not user_data:
        return jsonify({
            'has_previous_conversation': False,
            'success': True
        })
    
    conversation = session.get('conversation', [])
    current_session_id = session.get('session_id')
    current_username = user_data.get('username')
    
    # Validate session belongs to current user
    if current_session_id and current_username:
        if not current_session_id.startswith(current_username):
            # Session mismatch - no previous conversation for this user
            session['conversation'] = []
            return jsonify({
                'has_previous_conversation': False,
                'success': True
            })
    
    has_conversation = len(conversation) > 0
    
    return jsonify({
        'has_previous_conversation': has_conversation,
        'message_count': len(conversation),
        'username': current_username,
        'session_id': current_session_id,
        'success': True
    })

@main.route('/clear_conversation', methods=['POST'])
def clear_conversation():
    """Route to clear conversation history"""
    user_data = session.get('user_data')
    
    # Clear conversation and mood data
    session['conversation'] = []
    session['mood_data'] = []
    
    # Reset video recommendation count for fresh conversation
    session['videos_recommended_count'] = 0
    
    # Create new session ID for fresh start
    import uuid
    import time
    if user_data and user_data.get('username'):
        username = user_data.get('username')
        session['session_id'] = f"{username}_{str(uuid.uuid4())[:8]}_{int(time.time())}"
    else:
        session['session_id'] = f"guest_{str(uuid.uuid4())[:8]}_{int(time.time())}"
    
    return jsonify({
        'success': True,
        'message': 'Conversation cleared successfully',
        'new_session_id': session['session_id']
    })

@main.route('/validate_session', methods=['GET'])
def validate_session():
    """Route to validate current session integrity"""
    user_data = session.get('user_data')
    demo_mode = session.get('demoMode') == 'true'
    current_session_id = session.get('session_id')
    
    if not user_data:
        return jsonify({
            'valid': False,
            'reason': 'No user data in session'
        })
    
    if demo_mode:
        return jsonify({
            'valid': True,
            'mode': 'demo',
            'user': user_data.get('name', 'Guest')
        })
    
    # For authenticated users, validate session integrity
    current_username = user_data.get('username')
    if current_session_id and current_username:
        if current_session_id.startswith(current_username):
            return jsonify({
                'valid': True,
                'mode': 'authenticated',
                'user': user_data.get('name'),
                'username': current_username,
                'session_id': current_session_id
            })
        else:
            return jsonify({
                'valid': False,
                'reason': 'Session mismatch',
                'action': 'session_reset_required'
            })
    
    return jsonify({
        'valid': False,
        'reason': 'Invalid session data'
    })

def store_mood_data(emotion):
    """Store user mood data in session"""
    if 'mood_data' not in session:
        session['mood_data'] = []

def get_mock_video_recommendations(emotion):
    """Mock video recommendations for testing when backend is not available"""
    mock_videos = {
        'anxious': [
            {
                'id': 'mock_1',
                'title': '5-Minute Anxiety Relief Breathing',
                'description': 'Quick breathing exercise to calm your mind and reduce anxiety symptoms instantly.',
                'videoUrl': 'https://www.youtube.com/watch?v=YRPh_GaiL8s',
                'thumbnailUrl': 'https://img.youtube.com/vi/YRPh_GaiL8s/maxresdefault.jpg',
                'duration': 5,
                'primaryMoodCategory': 'anxious',
                'therapyTechnique': 'breathing_exercises',
                'contentType': 'meditation',
                'difficultyLevel': 'beginner',
                'crisisSafe': True,
                'averageRating': 4.8,
                'interactiveFeatures': ['breathing guide', 'progress tracker'],
                'tags': ['quick', 'beginner', 'crisis safe']
            },
            {
                'id': 'mock_2',
                'title': 'Forest Meditation for Anxiety',
                'description': 'Guided meditation in a peaceful forest setting to help reduce anxiety and stress.',
                'videoUrl': 'https://www.youtube.com/watch?v=inpok4MKVLM',
                'thumbnailUrl': 'https://img.youtube.com/vi/inpok4MKVLM/maxresdefault.jpg',
                'duration': 15,
                'primaryMoodCategory': 'anxious',
                'therapyTechnique': 'mindfulness_meditation',
                'contentType': 'meditation',
                'difficultyLevel': 'beginner',
                'crisisSafe': True,
                'averageRating': 4.6,
                'interactiveFeatures': ['nature sounds', 'guided meditation'],
                'tags': ['nature', 'mindfulness', 'medium']
            },
            {
                'id': 'mock_3',
                'title': 'Progressive Muscle Relaxation',
                'description': 'Step-by-step muscle relaxation technique to release physical tension and anxiety.',
                'videoUrl': 'https://www.youtube.com/watch?v=86HUcX8ZtAk',
                'thumbnailUrl': 'https://img.youtube.com/vi/86HUcX8ZtAk/maxresdefault.jpg',
                'duration': 20,
                'primaryMoodCategory': 'anxious',
                'therapyTechnique': 'progressive_muscle_relaxation',
                'contentType': 'therapy',
                'difficultyLevel': 'intermediate',
                'crisisSafe': True,
                'averageRating': 4.7,
                'interactiveFeatures': ['muscle tension guide', 'relaxation tracker'],
                'tags': ['progressive', 'muscle relaxation', 'medium']
            }
        ],
        'stressed': [
            {
                'id': 'mock_4',
                'title': 'Beach Stress Relief Meditation',
                'description': 'Calming beach visualization to wash away stress and tension.',
                'videoUrl': 'https://www.youtube.com/watch?v=lFcSrYw-ARY',
                'thumbnailUrl': 'https://img.youtube.com/vi/lFcSrYw-ARY/maxresdefault.jpg',
                'duration': 10,
                'primaryMoodCategory': 'stressed',
                'therapyTechnique': 'guided_imagery',
                'contentType': 'meditation',
                'difficultyLevel': 'beginner',
                'crisisSafe': True,
                'averageRating': 4.5,
                'interactiveFeatures': ['ocean sounds', 'visualization guide'],
                'tags': ['beach', 'stress relief', 'short']
            },
            {
                'id': 'mock_5',
                'title': 'Quick Stress-Busting Exercises',
                'description': 'Simple physical exercises to quickly release stress and boost energy.',
                'videoUrl': 'https://www.youtube.com/watch?v=1ZYbU82GVz4',
                'thumbnailUrl': 'https://img.youtube.com/vi/1ZYbU82GVz4/maxresdefault.jpg',
                'duration': 8,
                'primaryMoodCategory': 'stressed',
                'therapyTechnique': 'physical_activity',
                'contentType': 'exercise',
                'difficultyLevel': 'beginner',
                'crisisSafe': True,
                'averageRating': 4.4,
                'interactiveFeatures': ['exercise tracker', 'energy boost'],
                'tags': ['exercise', 'quick', 'energy']
            }
        ],
        'sad': [
            {
                'id': 'mock_6',
                'title': 'Uplifting Mindfulness Practice',
                'description': 'Gentle mindfulness practice designed to lift your spirits and bring inner peace.',
                'videoUrl': 'https://www.youtube.com/watch?v=ZToicYcHIOU',
                'thumbnailUrl': 'https://img.youtube.com/vi/ZToicYcHIOU/maxresdefault.jpg',
                'duration': 12,
                'primaryMoodCategory': 'sad',
                'therapyTechnique': 'mindfulness_meditation',
                'contentType': 'meditation',
                'difficultyLevel': 'beginner',
                'crisisSafe': True,
                'averageRating': 4.6,
                'interactiveFeatures': ['mood tracking', 'gentle guidance'],
                'tags': ['uplifting', 'mindfulness', 'gentle']
            }
        ]
    }
    
    # Return videos for the specific emotion, or default to anxious videos
    return mock_videos.get(emotion.lower(), mock_videos['anxious'])[:3]
    
    # Map emotions to numerical values (1-10)
    emotion_scores = {
        'Happy': 9,
        'Sad': 3,
        'Anxious': 4,
        'Angry': 2,
        'Neutral': 6,
        'Stressed': 4,
        'Depressed': 2
    }
    
    # Get the score for the emotion (default to 6/Neutral)
    score = emotion_scores.get(emotion, 6)
    
    # Store date and emotion score
    current_date = datetime.now().strftime('%a')  # Short day name (Mon, Tue, etc.)
    
    # Add to mood data
    session['mood_data'].append({
        'date': current_date,
        'score': score,
        'emotion': emotion
    })
    
    # Keep only the last 7 mood entries
    if len(session['mood_data']) > 7:
        session['mood_data'] = session['mood_data'][-7:]

# Therapeutic Tools Routes
@main.route('/coping-strategies')
def coping_strategies():
    return render_template('coping_strategies.html')

@main.route('/breathing-exercises')
def breathing_exercises():
    return render_template('breathing_exercises.html')

@main.route('/mindfulness')
def mindfulness():
    return render_template('mindfulness.html')

@main.route('/crisis')
def crisis():
    return render_template('crisis.html')

@main.route('/logout')
def logout_page():
    """Clear session and redirect to landing page"""
    auth_service.logout_user()
    return redirect(url_for('main.landing'))

# New authentication routes for Java backend integration
@main.route('/api/register', methods=['POST'])
def register_api():
    """Register user via Java backend"""
    data = request.json
    
    # Validate input
    required_fields = ['name', 'email', 'password']
    if not all(field in data for field in required_fields):
        return jsonify({
            'success': False,
            'message': 'Name, email, and password are required'
        }), 400
    
    # Use email as username for consistency
    username = data['email'].split('@')[0]  # Extract part before @ as username
    
    # Register via Java backend
    result = auth_service.register_user({
        'username': username,
        'password': data['password'],
        'email': data['email'],
        'fullName': data['name']
    })
    
    if result['success']:
        return jsonify(result), 201
    else:
        return jsonify(result), 400

@main.route('/api/login', methods=['POST'])
def login_api():
    """Login user via Java backend"""
    data = request.json
    
    # Validate input
    if not data.get('email') or not data.get('password'):
        return jsonify({
            'success': False,
            'message': 'Email and password are required'
        }), 400
    
    # Convert email to username for backend compatibility
    username = data['email'].split('@')[0]  # Extract part before @ as username
    
    # IMPORTANT: Clear all existing session data before login
    session.clear()
    
    # Login via Java backend
    result = auth_service.login_user({
        'username': username,
        'password': data['password']
    })
    
    if result['success']:
        # Store user session data with user-specific session ID
        import uuid
        import time
        user_session_id = f"{username}_{str(uuid.uuid4())[:8]}_{int(time.time())}"
        
        session['user_data'] = {
            'name': result.get('user', {}).get('fullName', 'User'),
            'email': data['email'],
            'username': username,
            'mode': 'authenticated'
        }
        session['demoMode'] = 'false'
        session['session_id'] = user_session_id
        session['user_name'] = result.get('user', {}).get('fullName', 'User')
        
        # Initialize empty conversation and mood data for this specific user
        session['conversation'] = []
        session['mood_data'] = []
        
        return jsonify(result), 200
    else:
        return jsonify(result), 401

@main.route('/api/videos/mood/<mood>')
def get_videos_by_mood(mood):
    """Get video recommendations for a specific mood"""
    try:
        videos = enhanced_video_service.get_popular_videos(mood)
        formatted_videos = videos
        
        return jsonify({
            'success': True,
            'mood': mood,
            'videos': formatted_videos,
            'count': len(formatted_videos)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching videos: {str(e)}'
        }), 500

# API Routes
@main.route('/api/mood-analysis', methods=['POST'])
def analyze_mood_api():
    """API endpoint for comprehensive mood analysis with scene recommendations"""
    try:
        data = request.json
        text = data.get('text', '')
        intensity = data.get('intensity', 5)  # 1-10 scale
        user_preferences = data.get('preferences', {})
        
        if not text:
            return jsonify({
                'error': 'Text is required for mood analysis',
                'success': False
            }), 400
        
        # Perform comprehensive mood analysis
        analysis_result = mood_scene_mapper.analyze_mood_for_backend(
            mood_text=text,
            intensity=intensity,
            user_preferences=user_preferences
        )
        
        # Export in backend-friendly format
        backend_data = mood_scene_mapper.export_for_backend(analysis_result)
        
        return jsonify({
            'analysis': backend_data,
            'success': True
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 500

@main.route('/api/scene-recommendations/<mood>', methods=['GET'])
def get_scene_recommendations_api(mood):
    """API endpoint to get scene recommendations for a specific mood"""
    try:
        # Convert mood string to MoodCategory
        try:
            mood_category = MoodCategory(mood.lower())
        except ValueError:
            return jsonify({
                'error': f'Invalid mood category: {mood}',
                'valid_moods': [m.value for m in MoodCategory],
                'success': False
            }), 400
        
        # Get user preferences from query parameters
        user_preferences = {}
        if request.args.get('max_duration'):
            user_preferences['max_duration'] = int(request.args.get('max_duration'))
        if request.args.get('preferred_scenes'):
            user_preferences['preferred_scenes'] = request.args.get('preferred_scenes').split(',')
        if request.args.get('preferred_techniques'):
            user_preferences['preferred_techniques'] = request.args.get('preferred_techniques').split(',')
        
        # Get recommendations
        recommendations = mood_scene_mapper.get_scene_recommendations(mood_category, user_preferences)
        
        # Convert to JSON format
        recommendations_data = [
            {
                'sceneType': rec.scene_type.value,
                'therapyTechnique': rec.therapy_technique.value,
                'priority': rec.priority,
                'description': rec.description,
                'durationMinutes': rec.duration_minutes,
                'interactiveElements': rec.interactive_elements,
                'goals': rec.goals
            }
            for rec in recommendations
        ]
        
        return jsonify({
            'mood': mood,
            'recommendations': recommendations_data,
            'count': len(recommendations_data),
            'success': True
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 500

@main.route('/api/mood-categories', methods=['GET'])
def get_mood_categories_api():
    """API endpoint to get all available mood categories"""
    return jsonify({
        'mood_categories': [
            {
                'value': mood.value,
                'name': mood.name,
                'description': get_mood_description(mood)
            }
            for mood in MoodCategory
        ],
        'success': True
    })

@main.route('/api/therapy-techniques', methods=['GET'])
def get_therapy_techniques_api():
    """API endpoint to get all available therapy techniques"""
    from app.models.mood_scene_mapping import TherapyTechnique
    
    return jsonify({
        'therapy_techniques': [
            {
                'value': technique.value,
                'name': technique.name,
                'description': get_technique_description(technique)
            }
            for technique in TherapyTechnique
        ],
        'success': True
    })

@main.route('/api/scene-types', methods=['GET'])
def get_scene_types_api():
    """API endpoint to get all available scene types"""
    from app.models.mood_scene_mapping import SceneType
    
    return jsonify({
        'scene_types': [
            {
                'value': scene.value,
                'name': scene.name,
                'description': get_scene_description(scene)
            }
            for scene in SceneType
        ],
        'success': True
    })

@main.route('/api/crisis-assessment', methods=['POST'])
def assess_crisis_risk_api():
    """API endpoint for crisis risk assessment"""
    try:
        data = request.json
        text = data.get('text', '')
        mood = data.get('mood', 'neutral')
        intensity = data.get('intensity', 5)
        
        if not text:
            return jsonify({
                'error': 'Text is required for crisis assessment',
                'success': False
            }), 400
        
        # Convert mood to category
        mood_category = MoodCategory(mood.lower()) if mood else MoodCategory.NEUTRAL
        
        # Assess crisis risk
        crisis_risk = mood_scene_mapper._assess_crisis_risk(text, mood_category, intensity)
        
        # Get appropriate intervention recommendations
        interventions = []
        if crisis_risk:
            interventions = [
                "Immediate professional support recommended",
                "Crisis hotline: 988 (US) or local emergency services",
                "Do not leave person alone if possible",
                "Remove potential means of self-harm",
                "Encourage immediate mental health evaluation"
            ]
        
        return jsonify({
            'crisis_risk': crisis_risk,
            'risk_level': 'HIGH' if crisis_risk else 'LOW',
            'interventions': interventions,
            'immediate_action_required': crisis_risk,
            'success': True
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 500

@main.route('/api/mood-trends', methods=['GET'])
def get_mood_trends_api():
    """Get user's mood trends and analytics"""
    try:
        if not session.get('user_data'):
            return jsonify({
                'success': False,
                'message': 'User not authenticated'
            }), 401
        
        # Get mood history and trends from Java backend
        mood_history = mood_tracking_service.get_user_mood_history()
        mood_trends = mood_tracking_service.get_user_mood_trends()
        
        # Format data for frontend
        chart_data = mood_tracking_service.format_mood_history_for_chart(mood_history)
        dashboard_trends = mood_tracking_service.format_mood_trends_for_dashboard(mood_trends)
        
        # Detect concerning patterns
        concerns = mood_tracking_service.detect_concerning_patterns(mood_history, mood_trends)
        
        return jsonify({
            'success': True,
            'chartData': chart_data,
            'trends': dashboard_trends,
            'history': mood_history,
            'concerns': concerns,
            'hasData': len(mood_history) > 0
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching mood trends: {str(e)}'
        }), 500

@main.route('/api/dashboard', methods=['GET'])
def get_dashboard_data():
    """Get comprehensive dashboard data including mood trends and recommendations"""
    try:
        if not session.get('user_data'):
            return jsonify({
                'success': False,
                'message': 'User not authenticated'
            }), 401
        
        user_data = session.get('user_data', {})
        
        # Get mood trends
        mood_history = mood_tracking_service.get_user_mood_history()
        mood_trends = mood_tracking_service.get_user_mood_trends()
        
        # Get recent videos based on latest mood
        recent_videos = []
        if mood_history:
            latest_mood = mood_history[0].get('mood', 'neutral')
            recent_videos = enhanced_video_service.get_popular_videos(latest_mood, limit=3)
        
        # Format data
        chart_data = mood_tracking_service.format_mood_history_for_chart(mood_history)
        dashboard_trends = mood_tracking_service.format_mood_trends_for_dashboard(mood_trends)
        concerns = mood_tracking_service.detect_concerning_patterns(mood_history, mood_trends)
        
        # Get scene recommendations based on most common mood
        scene_recommendations = []
        if mood_trends.get('mostCommonMood'):
            try:
                from app.models.mood_scene_mapping import MoodCategory, mood_scene_mapper
                mood_category = MoodCategory(mood_trends['mostCommonMood'].lower())
                recommendations = mood_scene_mapper.get_scene_recommendations(mood_category)
                scene_recommendations = [
                    {
                        'sceneType': rec.scene_type.value,
                        'therapyTechnique': rec.therapy_technique.value,
                        'priority': rec.priority,
                        'description': rec.description,
                        'durationMinutes': rec.duration_minutes
                    }
                    for rec in recommendations[:3]
                ]
            except:
                pass
        
        return jsonify({
            'success': True,
            'user': {
                'name': user_data.get('fullName', user_data.get('username', 'User')),
                'username': user_data.get('username'),
                'memberSince': user_data.get('createdAt', 'Recently')
            },
            'moodData': {
                'chartData': chart_data,
                'trends': dashboard_trends,
                'recentEntries': mood_history[:5],
                'concerns': concerns
            },
            'recommendations': {
                'videos': recent_videos,
                'scenes': scene_recommendations
            },
            'stats': {
                'totalSessions': len(mood_history),
                'averageMood': dashboard_trends.get('averageIntensity', 'N/A'),
                'improvementTrend': dashboard_trends.get('improvementTrend', 'stable')
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching dashboard data: {str(e)}'
        }), 500

@main.route('/dashboard')
def dashboard():
    """User dashboard page"""
    if not session.get('user_data'):
        return redirect(url_for('main.auth_page'))
    return render_template('dashboard.html')

@main.route('/api/start-demo', methods=['POST'])
def start_demo():
    """Start demo mode with provided user data"""
    try:
        data = request.json
        name = data.get('name', 'Guest')
        gender = data.get('gender', 'not-specified')
        
        # Set session for demo mode
        session['demoMode'] = 'true'
        session['user_data'] = {
            'name': name,
            'gender': gender,
            'mode': 'demo',
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify({
            'success': True,
            'message': 'Demo mode started successfully',
            'user': {
                'name': name,
                'mode': 'demo'
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Failed to start demo: {str(e)}'
        }), 500

@main.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'services': {
            'flask': True,
            'ai': True,
            'mongodb': True
        }
    })

@main.route('/api/user-profile', methods=['GET'])
def get_user_profile():
    """Get current user profile information"""
    try:
        if not session.get('user_data'):
            return jsonify({
                'success': False,
                'message': 'User not authenticated'
            }), 401
        
        user_data = session.get('user_data', {})
        return jsonify({
            'success': True,
            'user': {
                'username': user_data.get('username'),
                'fullName': user_data.get('fullName'),
                'email': user_data.get('email'),
                'createdAt': user_data.get('createdAt')
            },
            'lastSession': user_data.get('lastLoginTime')
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching user profile: {str(e)}'
        }), 500

@main.route('/api/mood-history', methods=['GET'])
def get_mood_history():
    """Get user's mood history"""
    try:
        if not session.get('user_data'):
            return jsonify({
                'success': False,
                'message': 'User not authenticated'
            }), 401
        
        # Get mood history from Java backend
        mood_history = mood_tracking_service.get_user_mood_history()
        
        return jsonify({
            'success': True,
            'history': mood_history,
            'count': len(mood_history)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching mood history: {str(e)}'
        }), 500

@main.route('/api/therapeutic-goals', methods=['GET'])
def get_therapeutic_goals():
    """Get therapeutic goals for the user"""
    try:
        if not session.get('user_data'):
            return jsonify({
                'success': False,
                'message': 'User not authenticated'
            }), 401
        
        # Get user's recent mood data to generate personalized goals
        mood_history = mood_tracking_service.get_user_mood_history()
        
        # Generate therapeutic goals based on mood patterns
        goals = []
        if mood_history:
            latest_moods = [entry.get('primaryMood', 'neutral') for entry in mood_history[:5]]
            
            # Generate goals based on recent patterns
            if 'anxious' in latest_moods:
                goals.append('Practice 10 minutes of deep breathing exercises daily')
                goals.append('Try progressive muscle relaxation before bed')
            
            if 'sad' in latest_moods or 'depressed' in latest_moods:
                goals.append('Engage in one enjoyable activity today')
                goals.append('Connect with a friend or family member')
                
            if 'stressed' in latest_moods:
                goals.append('Take three 5-minute mindfulness breaks')
                goals.append('Practice setting healthy boundaries')
                
            if 'angry' in latest_moods:
                goals.append('Use anger management techniques when triggered')
                goals.append('Practice identifying anger triggers')
        
        # Default goals if no specific patterns
        if not goals:
            goals = [
                'Check in with your emotions 3 times today',
                'Practice 5 minutes of mindfulness',
                'Take care of your physical health'
            ]
        
        return jsonify({
            'success': True,
            'goals': goals[:3]  # Return top 3 goals
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error generating therapeutic goals: {str(e)}'
        }), 500

@main.route('/api/analyze-mood', methods=['POST'])
def analyze_mood_frontend():
    """Analyze mood and store in Java backend"""
    try:
        data = request.json
        text = data.get('text', '')
        intensity = data.get('intensity', 5)
        preferences = data.get('preferences', {})
        
        if not text.strip():
            return jsonify({
                'success': False,
                'message': 'Text is required for mood analysis'
            }), 400
        
        if not session.get('user_data'):
            return jsonify({
                'success': False,
                'message': 'User not authenticated'
            }), 401
        
        # Analyze mood using our local system
        emotional_context = analyze_mood(text)
        
        # Get comprehensive analysis
        analysis_result = mood_scene_mapper.analyze_mood_for_backend(
            mood_text=text,
            intensity=intensity,
            user_preferences=preferences
        )
        
        # Store in Java backend
        mood_storage_result = mood_tracking_service.store_mood_analysis(
            text=text,
            mood_data={
                'primaryMood': emotional_context,
                'intensity': intensity,
                'confidenceScore': 0.85,  # Default confidence
                'preferences': preferences,
                'crisisRisk': analysis_result.crisis_risk
            }
        )
        
        if mood_storage_result.get('success'):
            return jsonify({
                'success': True,
                'mood': {
                    'primaryMood': emotional_context,
                    'intensity': intensity,
                    'confidenceScore': 0.85,
                    'crisisRisk': analysis_result.crisis_risk
                },
                'message': 'Mood analysis completed and stored successfully'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to store mood analysis'
            }), 500
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error analyzing mood: {str(e)}'
        }), 500

@main.route('/api/logout', methods=['POST'])
def logout_api():
    """Logout user and clear session"""
    try:
        auth_service.logout_user()
        return jsonify({
            'success': True,
            'message': 'Logged out successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error during logout: {str(e)}'
        }), 500

@main.route('/api/video-interaction', methods=['POST'])
def record_video_interaction():
    """Record user interaction with videos for analytics"""
    try:
        data = request.json
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        video_id = data.get('videoId')
        username = data.get('username')
        interaction_type = data.get('interactionType')
        
        if not all([video_id, username, interaction_type]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Record interaction with enhanced video service
        success = enhanced_video_service.record_video_interaction(video_id, username, interaction_type)
        
        if success:
            return jsonify({'success': True, 'message': 'Interaction recorded'})
        else:
            return jsonify({'success': False, 'message': 'Failed to record interaction'}), 500
            
    except Exception as e:
        print(f"Error recording video interaction: {e}")
        return jsonify({'error': 'Internal server error'}), 500

def get_mood_description(mood: MoodCategory) -> str:
    """Get human-readable description for mood categories"""
    descriptions = {
        MoodCategory.HAPPY: "Positive, joyful, or content emotional state",
        MoodCategory.SAD: "Feeling down, melancholy, or sorrowful",
        MoodCategory.ANXIOUS: "Worried, nervous, or experiencing anxiety",
        MoodCategory.ANGRY: "Feeling irritated, frustrated, or enraged",
        MoodCategory.STRESSED: "Overwhelmed, pressured, or under strain",
        MoodCategory.DEPRESSED: "Persistent sadness, hopelessness, or low mood",
        MoodCategory.NEUTRAL: "Balanced, calm, or emotionally stable",
        MoodCategory.FRUSTRATED: "Blocked, hindered, or feeling stuck",
        MoodCategory.LONELY: "Isolated, disconnected, or craving companionship",
        MoodCategory.OVERWHELMED: "Feeling unable to cope with demands"
    }
    return descriptions.get(mood, "Emotional state")

def get_technique_description(technique) -> str:
    """Get human-readable description for therapy techniques"""
    from app.models.mood_scene_mapping import TherapyTechnique
    
    descriptions = {
        TherapyTechnique.BREATHING_EXERCISES: "Controlled breathing patterns for relaxation and anxiety relief",
        TherapyTechnique.MINDFULNESS_MEDITATION: "Present-moment awareness and meditation practices",
        TherapyTechnique.PROGRESSIVE_MUSCLE_RELAXATION: "Systematic tension and relaxation of muscle groups",
        TherapyTechnique.GUIDED_IMAGERY: "Visualization and mental imagery for therapeutic purposes",
        TherapyTechnique.GROUNDING_TECHNIQUES: "Techniques to stay present and connected to reality",
        TherapyTechnique.COGNITIVE_RESTRUCTURING: "Identifying and changing negative thought patterns",
        TherapyTechnique.EXPOSURE_THERAPY: "Gradual exposure to fears or anxiety triggers",
        TherapyTechnique.NATURE_THERAPY: "Using natural environments for healing and wellbeing",
        TherapyTechnique.SOCIAL_INTERACTION: "Therapeutic social engagement and connection",
        TherapyTechnique.PHYSICAL_ACTIVITY: "Movement and exercise for mental health benefits"
    }
    return descriptions.get(technique, "Therapeutic intervention")

def get_scene_description(scene) -> str:
    """Get human-readable description for scene types"""
    from app.models.mood_scene_mapping import SceneType
    
    descriptions = {
        SceneType.CALMING_NATURE: "Peaceful natural environment with trees, grass, and gentle sounds",
        SceneType.PEACEFUL_BEACH: "Serene beach setting with waves, sand, and ocean views",
        SceneType.FOREST_MEDITATION: "Quiet forest grove perfect for meditation and reflection",
        SceneType.MOUNTAIN_RETREAT: "Mountain setting with fresh air and expansive views",
        SceneType.COZY_INDOOR: "Warm, safe indoor space with comfortable furnishings",
        SceneType.BREATHING_GARDEN: "Designed garden space optimized for breathing exercises",
        SceneType.SOCIAL_CAFÉ: "Virtual café environment for social interaction practice",
        SceneType.VIRTUAL_GYM: "Exercise space for physical activity and energy release",
        SceneType.ART_THERAPY_STUDIO: "Creative workspace for artistic expression and therapy",
        SceneType.CONFIDENCE_STAGE: "Supportive environment for building confidence and self-esteem"
    }
    return descriptions.get(scene, "Therapeutic environment")