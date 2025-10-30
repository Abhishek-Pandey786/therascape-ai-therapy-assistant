import os
import time
import random
import re
from dotenv import load_dotenv
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI # pyright: ignore[reportMissingImports]
from langchain.prompts import PromptTemplate # type: ignore

# Load environment variables
load_dotenv()

# Google API Key - Load from environment variables
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
print(f"API Key in therapy_bot.py: {GOOGLE_API_KEY[:10] if GOOGLE_API_KEY else 'Not found'}...")

# Configure Gemini API
api_configured = False
selected_model = "models/gemini-2.5-flash-preview-05-20"  # Default to Gemini 2.5 Flash Preview which has better free tier

if GOOGLE_API_KEY:
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        print("Gemini API configured successfully")
        api_configured = True
        
        # Test the API key
        models = genai.list_models()
        print(f"Available models: {[m.name for m in models]}")
        
        # Find the best available model
        available_models = [m.name for m in models]
        preferred_models = [
            "models/gemini-1.5-flash",
            "models/gemini-1.5-flash-8b",
            "models/gemini-2.0-flash", 
            "models/gemini-2.5-flash-preview-05-20"
        ]
        
        for model_name in preferred_models:
            if model_name in available_models:
                selected_model = model_name
                print(f"Selected model: {selected_model}")
                break
        
        # If none of the preferred models are available, use whatever is available
        if selected_model not in available_models and available_models:
            selected_model = available_models[0]
            print(f"Falling back to available model: {selected_model}")
    except Exception as e:
        print(f"Error configuring Gemini API: {e}")
        api_configured = False
else:
    print("Warning: GOOGLE_API_KEY not found in environment variables")

# Define enhanced therapist persona with structured, empathetic approach
THERAPIST_PROMPT = """You are TheraScape, a compassionate, structured, and empathetic therapy assistant. 
Your role is not to replace a professional therapist but to provide supportive, reflective, and helpful conversations.

Guidelines:
1. **Empathy First** – Always acknowledge the user's emotions and validate their feelings before suggesting solutions. Use warm, understanding language.
   - Example: "It sounds like you're feeling really overwhelmed right now, and that's completely valid."
   
2. **Structured Reasoning** – Organize responses into clear steps:
   - Reflect back what the user said (to show understanding).
   - Explore underlying emotions or thoughts.
   - Offer gentle suggestions, coping strategies, or questions to guide reflection.
   - End with an open, supportive note.

3. **Balance Support & Boundaries** – Provide comfort, encouragement, and practical strategies (breathing exercises, journaling, reframing thoughts, grounding techniques) but avoid making medical diagnoses or strong claims.

4. **Human-Like Conversation** – Write in a calm, natural, and conversational tone. Avoid robotic or overly formal responses.

5. **Encourage Growth** – When appropriate, nudge the user towards positive thinking, resilience, or self-awareness. Use motivational but realistic language.

6. **Safety First** – If the user shows signs of self-harm or crisis, gently encourage reaching out to a professional or trusted contact, and provide crisis hotline info if relevant.

7. **Video Recommendations** - Only suggest videos when it naturally fits the conversation:
   - Never recommend videos immediately at the start of conversations (initial greetings)
   - Only suggest when user explicitly asks for help, tips, or coping strategies
   - Only when user expresses emotional distress that could benefit from video support
   - Frame video suggestions supportively: "Would you like me to share a helpful video that many people find calming?"
   - Limit to maximum 1 video recommendation per conversation unless user asks for more

Example Response Structure:
- Acknowledge their emotion: "I can hear that you're feeling..."
- Validate their experience: "That sounds really difficult/challenging..."
- Explore gently: "What's been the hardest part about this?" or "How long have you been feeling this way?"
- Offer support/strategy: "Something that might help is..." or "Would you like to try..."
- End with encouragement: "You're not alone in this" or "I'm here to support you through this"

Always respond with genuine warmth, professional boundaries, and focus on the user's wellbeing."""

# Initialize the Gemini model
model = None
if GOOGLE_API_KEY and api_configured:
    try:
        # Extract the model name without the "models/" prefix for LangChain
        langchain_model_name = selected_model.replace("models/", "")
        
        model = ChatGoogleGenerativeAI(
            model=langchain_model_name,
            temperature=0.6,  # Lower temperature for more focused responses
            max_output_tokens=400,  # Increased for complete responses
            top_p=0.95,
            google_api_key=GOOGLE_API_KEY
        )
        print("Gemini model initialized successfully")
    except Exception as e:
        print(f"Error initializing Gemini model: {e}")

# Simple session-based conversation tracking (no persistent memory)
current_session_memory = {}

# Track asked questions to avoid repetition in current session only
session_questions = {}

# Track recent responses to avoid repetition
recent_responses = {}

def is_response_too_similar(new_response, recent_responses_list, threshold=0.7):
    """Check if the new response is too similar to recent responses"""
    import re
    
    # Simple similarity check based on key phrases
    new_response_words = set(re.findall(r'\b\w+\b', new_response.lower()))
    
    for recent_response in recent_responses_list:
        recent_words = set(re.findall(r'\b\w+\b', recent_response.lower()))
        
        # Calculate overlap
        if len(new_response_words) > 0 and len(recent_words) > 0:
            overlap = len(new_response_words.intersection(recent_words))
            similarity = overlap / min(len(new_response_words), len(recent_words))
            
            if similarity > threshold:
                return True
    
    return False

def add_to_recent_responses(session_id, response):
    """Add response to recent responses and maintain a sliding window"""
    if session_id not in recent_responses:
        recent_responses[session_id] = []
    
    recent_responses[session_id].append(response)
    
    # Keep only last 3 responses
    if len(recent_responses[session_id]) > 3:
        recent_responses[session_id] = recent_responses[session_id][-3:]

def get_varied_response(emotion, user_input, session_id):
    """Get structured, therapeutic response based on emotion with empathy-first approach"""
    if session_id not in session_questions:
        session_questions[session_id] = set()
    
    # Enhanced therapeutic responses with structured empathy
    emotion_responses = {
        'Stressed': [
            "I can hear that you're feeling really stressed right now, and that's completely understandable. Stress can feel so overwhelming when it builds up. What's been the biggest source of pressure for you lately? Sometimes just talking about it can help lighten the load a bit.",
            "It sounds like you're carrying a heavy burden of stress. That must be exhausting for you. When you're feeling this overwhelmed, what usually helps you feel even a little bit calmer? I'm here to help you work through this step by step.",
            "I hear how much pressure you're under, and I want you to know that feeling stressed doesn't mean you're not handling things well—it means you care deeply. What aspect of your stress feels most urgent to you right now? Let's see if we can break it down together.",
            "That sounds really overwhelming, and it's completely valid to feel stressed when dealing with so much. Sometimes our minds can feel like they're racing with everything we need to handle. What's one thing that's been weighing most heavily on your mind?",
            "I can sense how much stress you're experiencing, and I want you to know that you're not alone in feeling this way. Stress can make everything feel urgent and impossible. What would feel most helpful for you to focus on right now—talking through what's stressing you, or maybe trying a quick way to find some calm?"
        ],
        'Anxious': [
            "I can hear the anxiety in what you're sharing, and I want you to know that anxiety, while uncomfortable, is your mind's way of trying to protect you. What thoughts have been running through your mind that are contributing to these anxious feelings? Sometimes naming them can reduce their power.",
            "It sounds like anxiety is really taking up a lot of space in your mind right now. That must feel so unsettling and exhausting. When you notice the anxiety building, what does it feel like in your body? Understanding your signals can help us work with it.",
            "I hear how much worry you're carrying, and anxiety can make everything feel uncertain and scary. You're being so brave by reaching out and talking about it. What situations or thoughts tend to trigger these anxious feelings most for you?",
            "That sounds really difficult—anxiety can make our minds feel like they're spinning with 'what if' thoughts. It's completely normal to feel this way, and it doesn't mean anything is wrong with you. What's been your biggest worry lately? Sometimes anxiety tries to solve problems that haven't even happened yet.",
            "I can sense how much your mind is racing with anxious thoughts right now. Anxiety can feel so overwhelming, but you're taking a positive step by talking about it. Have you noticed if there are certain times of day or situations when the anxiety feels stronger? Understanding patterns can be really helpful."
        ],
        'Sad': [
            "I can hear the sadness in your words, and I want you to know that it's okay to feel this way. Sadness is a natural response when we're going through difficult times or processing loss. What's been weighing most heavily on your heart lately? I'm here to listen and support you through this.",
            "It sounds like you're going through a really painful time right now, and I'm sorry you're experiencing this sadness. Sometimes sadness can feel like a heavy blanket that's hard to lift. What's been the most difficult part of your day today?",
            "I hear how much pain you're carrying, and I want you to know that your feelings are completely valid. Sadness often comes when something meaningful to us has been affected. Would you feel comfortable sharing what's been bringing up these sad feelings for you?",
            "That sounds really hard, and I can sense the deep sadness you're feeling. It takes courage to reach out when we're in pain. Sometimes sadness can feel isolating, but you're not alone in this. What's been the hardest moment for you recently?",
            "I can feel the sadness in what you're sharing, and I want you to acknowledge how strong you are for continuing to take care of yourself even when things feel this difficult. What's been helping you get through each day, even in small ways?"
        ],
        'Angry': [
            "I can hear the frustration and anger in what you're sharing, and those feelings are completely valid. Anger often shows up when something important to us feels threatened or unfair. What situation has been triggering these strong feelings for you? It's important to honor what your anger is trying to tell you.",
            "It sounds like something has really upset you, and anger can be such a powerful emotion. Sometimes anger is our way of protecting ourselves or standing up for what matters to us. What's been the most frustrating part of what you're dealing with?",
            "I hear how angry and frustrated you're feeling right now. Those are intense emotions, and it makes sense that you'd feel this way if something unfair or hurtful has happened. What's been making you feel most upset? Sometimes talking through it can help us understand what needs to change.",
            "That sounds incredibly frustrating, and anger is often a sign that our boundaries have been crossed or something unjust has happened. Your feelings are completely understandable. What's been the trigger for these angry feelings? I'm here to help you work through this in a healthy way.",
            "I can sense how much anger you're carrying, and that must feel overwhelming. Anger can be exhausting when we hold onto it. What's been the main source of your frustration? Sometimes understanding the 'why' behind our anger can help us figure out what we need to do next."
        ],
        'Happy': [
            "I love hearing that you're feeling happy! It's wonderful when life gives us these lighter, more joyful moments. What's been bringing you this happiness? I'd love to hear about what's going well for you—sometimes sharing our joy makes it even brighter.",
            "That's so wonderful to hear! Happiness can be such a gift, especially when we've been through difficult times. What's been the highlight that's brought you this joy? It's important to celebrate and savor these positive feelings.",
            "It makes me so glad to hear you sounding happy and positive! These moments of joy are precious and worth holding onto. What's been going particularly well for you lately? Sometimes reflecting on what brings us happiness helps us create more of it.",
            "That's fantastic! I can hear the lightness and joy in what you're sharing. Happiness is such a beautiful emotion to experience. What's been contributing to these good feelings? I love celebrating these moments with you.",
            "I'm so happy to hear you're feeling this way! Joy and happiness can be such healing forces in our lives. What's been the best part of what you're experiencing? These positive emotions are worth paying attention to and nurturing."
        ],
        'Depressed': [
            "I can hear how much pain and heaviness you're carrying right now, and I want you to know that reaching out takes incredible strength. Depression can make everything feel dark and hopeless, but you're not alone in this. What's been the hardest part about how you've been feeling? I'm here to sit with you in this difficult space.",
            "It sounds like you're going through an incredibly difficult time, and depression can make each day feel like an uphill battle. Your feelings are valid, and it's important that you're talking about this. What's been making things feel most overwhelming for you? Even small steps toward healing matter.",
            "I hear the deep sadness and pain you're experiencing, and I want you to know that what you're feeling is real and important. Depression can make it hard to see any light, but you've taken a brave step by reaching out. What support do you have around you right now? You don't have to face this alone.",
            "That sounds incredibly heavy to carry, and I'm sorry you're going through this darkness. Depression can make everything feel meaningless and exhausting. Have you been able to talk to anyone else about how you're feeling—a friend, family member, or counselor? Professional support can be really important with depression.",
            "I can sense how much you're struggling, and depression is one of the most challenging things anyone can face. It takes so much courage to keep going when everything feels this hard. What's one small thing that has brought you even a moment of comfort lately? Sometimes we need to start with the tiniest steps toward healing."
        ],
        'Neutral': [
            "I'm here and ready to listen to whatever is on your mind. Sometimes it helps just to have a safe space to share your thoughts, whether they're big or small. What's been occupying your thoughts lately? I'm here to support you through whatever you'd like to explore.",
            "Thank you for reaching out. I'm here to provide a supportive space for you to share whatever feels important. What's been going on in your life that you'd like to talk about? Sometimes just expressing our thoughts can bring clarity.",
            "I'm glad you're here and I'm ready to listen with full attention. Everyone's experience is valid and worth discussing. What would feel most helpful for you to focus on today? I'm here to support you in whatever way feels right.",
            "I'm here for you and ready to offer support in whatever way feels helpful. Sometimes we don't need to have a crisis to benefit from talking things through. What's been on your mind or heart lately that you'd like to explore together?",
            "Thank you for taking the time to connect. I'm here to provide a caring, non-judgmental space for whatever you'd like to share. What aspects of your life or feelings would you like to talk about today? There's no pressure—we can explore whatever feels right for you."
        ]
    }
    
    # Get available responses for this emotion
    available_responses = emotion_responses.get(emotion, emotion_responses['Neutral'])
    
    # Filter out recently used responses
    unused_responses = [r for r in available_responses if r not in session_questions[session_id]]
    
    # If we've used all responses, reset
    if not unused_responses:
        session_questions[session_id] = set()
        unused_responses = available_responses
    
    # Select a response
    selected_response = random.choice(unused_responses)
    session_questions[session_id].add(selected_response)
    
    return selected_response

# Enhanced therapeutic backup responses with structured empathy
BACKUP_RESPONSES = [
    "I can hear that you're going through something difficult right now, and I want you to know that your feelings are completely valid. You're not alone in this, and it takes courage to reach out. What would feel most helpful for you to focus on right now?",
    "It sounds like you're carrying a lot right now, and that takes incredible strength. Thank you for trusting me with what you're experiencing. Sometimes just having someone listen can provide a small sense of relief. What's been weighing most heavily on your mind?",
    "I hear you, and I want you to know that whatever you're feeling right now is okay and understandable. You're taking a positive step by reaching out and talking about what's going on. What aspect of your situation feels most important to explore together?",
    "Thank you for sharing with me—it shows real strength to open up when things feel difficult. Your experience matters, and I'm here to support you through whatever you're facing. What would feel most supportive for you right now?",
    "I can sense that you're going through something challenging, and I want you to know that you don't have to face this alone. Sometimes life can feel overwhelming, but you're here and you're reaching out, which shows real resilience. What's been the most difficult part for you lately?",
    "It sounds like you're navigating some tough emotions or situations, and I want to acknowledge how hard that can be. You're being brave by talking about it, and that's an important step. What would help you feel even a little bit more supported right now?",
    "I hear you, and I want you to know that your feelings—whatever they are—are important and valid. Sometimes we need a safe space to process what we're going through, and that's exactly what this is. What's been on your heart that you'd like to explore together?",
    "Thank you for trusting me with what you're experiencing. It takes courage to be vulnerable and share when things feel difficult. You matter, and your wellbeing matters. What aspect of your situation would feel most helpful to talk through?",
    "I can sense that something is weighing on you, and I want you to know that it's completely okay to not have everything figured out. You're human, and being human means experiencing the full range of emotions. What's been the most challenging part of your day or week?",
    "Whatever brought you here today, I'm glad you reached out. Sometimes we need someone to simply witness our experience without judgment, and that's what I'm here for. You're not alone in whatever you're facing. What would feel most important for us to focus on together?"
]

def convert_to_langchain_messages(messages):
    """Convert our messages to the format expected by LangChain"""
    history = []
    
    for message in messages:
        if message['role'] == 'user':
            # Add emotional context if available
            if 'emotionalContext' in message:
                emotional_context = f"""
                [EMOTIONAL CONTEXT:
                Text sentiment: {message['emotionalContext']}
                ]
                """
                history.append({"role": "user", "content": message['content'], "system": emotional_context})
            else:
                history.append({"role": "user", "content": message['content']})
        else:
            history.append({"role": "assistant", "content": message['content']})
    
    return history

def get_chat_response(messages, user_name=None, session_id=None):
    """Get response from Gemini model with session-based context (no persistent memory)"""
    if not GOOGLE_API_KEY or not api_configured:
        return "API key not configured. Please add your Google API key to the .env file."
    
    # Clean up old sessions periodically
    cleanup_old_sessions()
    
    # Generate a unique session ID if not present
    if session_id is None:
        import time
        session_id = f"auto_{int(time.time())}"
    
    # Only store current session data (not persistent across app restarts)
    if session_id not in current_session_memory:
        current_session_memory[session_id] = []
    
    # Add current messages to session memory
    for message in messages:
        if message not in current_session_memory[session_id]:
            current_session_memory[session_id].append(message)
    
    # Extract user's latest message
    user_input = messages[-1]['content']
    
    # Personalized greeting if this is the first message
    personalized_greeting = ""
    if user_name and len(messages) <= 2:  # 1 user + 1 bot message
        personalized_greeting = f"Greet the user by name ({user_name}) in a warm, welcoming way at the start of the conversation."
    
    # Try with direct Gemini API first
    try:
        # Get detected emotion for context
        emotion_context = messages[-1].get('emotionalContext', 'Neutral')
        
        # Build conversation context ONLY from current session
        conversation_context = ""
        if len(current_session_memory[session_id]) > 1:
            # Get the last few messages for context from THIS session only
            recent_messages = current_session_memory[session_id][-3:]  # Last 3 messages
            conversation_context = "\nRecent conversation:\n"
            for msg in recent_messages:
                role = "User" if msg['role'] == 'user' else "Assistant"
                conversation_context += f"{role}: {msg['content']}\n"
            # Get the last few messages for context
            recent_messages = current_session_memory[session_id][-3:]  # Last 3 messages
            conversation_context = "\nRecent conversation:\n"
            for msg in recent_messages:
                role = "User" if msg['role'] == 'user' else "Assistant"
                conversation_context += f"{role}: {msg['content']}\n"
        
        # Create enhanced therapeutic conversation prompt
        if conversation_context:
            # Build on the conversation with structured approach
            full_prompt = f"""
{THERAPIST_PROMPT}

{personalized_greeting}
{conversation_context}

Current user message: "{user_input}"
Detected emotion: {emotion_context}

Respond using the structured therapeutic approach:
1. Acknowledge their emotion with empathy
2. Validate their experience 
3. Explore gently with a thoughtful question
4. Offer support, insight, or coping strategy if appropriate
5. End with encouragement and openness

Keep responses warm, professional, and focused on their emotional wellbeing. Aim for 3-5 sentences that feel natural and supportive.
"""
        else:
            # First message - welcoming therapeutic introduction
            full_prompt = f"""
{THERAPIST_PROMPT}

{personalized_greeting}
User's first message: "{user_input}"
Detected emotion: {emotion_context}

This is the beginning of a therapeutic conversation. Respond with:
1. A warm, professional greeting (use their name if provided)
2. Acknowledge their emotion with validation
3. Create a safe, welcoming space
4. Ask an open, gentle question to understand their needs
5. Convey genuine care and availability

Keep it warm, professional, and inviting. 3-4 sentences that establish trust and support.
"""
        
        # Try with direct Gemini API with more natural response limits
        gemini_model = genai.GenerativeModel(
            model_name="models/gemini-1.5-flash",  # Use a more stable model
            generation_config={
                "temperature": 0.7,  # Higher temperature for more natural responses
                "top_p": 0.9,
                "top_k": 40,
                "max_output_tokens": 500,  # Increased for complete responses
            },
            safety_settings={
                genai.types.HarmCategory.HARM_CATEGORY_HATE_SPEECH: genai.types.HarmBlockThreshold.BLOCK_ONLY_HIGH,
                genai.types.HarmCategory.HARM_CATEGORY_HARASSMENT: genai.types.HarmBlockThreshold.BLOCK_ONLY_HIGH,
                genai.types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: genai.types.HarmBlockThreshold.BLOCK_ONLY_HIGH,
                genai.types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: genai.types.HarmBlockThreshold.BLOCK_ONLY_HIGH,
            }
        )
        response = gemini_model.generate_content(full_prompt)
        
        # Check if response has valid content
        if response.candidates and len(response.candidates) > 0:
            candidate = response.candidates[0]
            if candidate.content and candidate.content.parts:
                bot_response = candidate.content.parts[0].text
                print(f"Generated response: {bot_response}")
                return bot_response
            else:
                print(f"No content in response. Finish reason: {candidate.finish_reason}")
                print(f"Falling back to smart response for emotion: {emotion_context}")
                # Use sentiment-appropriate response as fallback
                emotion_context = messages[-1].get('emotionalContext', 'Neutral')
                return get_smart_fallback_response(user_input, emotion_context, session_id)
        else:
            print("No candidates in response")
            print(f"Falling back to smart response for emotion: {emotion_context}")
            # Use sentiment-appropriate response as fallback
            emotion_context = messages[-1].get('emotionalContext', 'Neutral')
            return get_smart_fallback_response(user_input, emotion_context, session_id)
    except Exception as e:
        print(f"Error with Gemini API: {e}")
        # Check if it's a quota error
        if "quota" in str(e).lower() or "429" in str(e):
            print("Quota exceeded, using simplified approach")
            # Try a simpler approach with context awareness
            try:
                # Build context summary from conversation
                context_summary = ""
                if len(current_session_memory[session_id]) > 1:
                    user_messages = [msg['content'] for msg in current_session_memory[session_id] if msg['role'] == 'user']
                    context_summary = f"User has previously shared: {' | '.join(user_messages[-3:])}"
                
                simple_prompt = f"""
You are a compassionate friend having a natural conversation with someone who wants to talk.

{context_summary}

Current user message: "{user_input}"

Respond naturally and authentically. Don't use templates or rigid structures. Just be genuinely supportive and interested in what they're sharing. Let the conversation flow naturally like you would with a good friend.
"""
                gemini_model = genai.GenerativeModel(
                    model_name="models/gemini-1.5-flash",  # Use a more stable model
                    generation_config={
                        "temperature": 0.7,
                        "top_p": 0.9,
                        "top_k": 40,
                        "max_output_tokens": 500,  # Increased for complete responses
                    },
                    safety_settings={
                        genai.types.HarmCategory.HARM_CATEGORY_HATE_SPEECH: genai.types.HarmBlockThreshold.BLOCK_ONLY_HIGH,
                        genai.types.HarmCategory.HARM_CATEGORY_HARASSMENT: genai.types.HarmBlockThreshold.BLOCK_ONLY_HIGH,
                        genai.types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: genai.types.HarmBlockThreshold.BLOCK_ONLY_HIGH,
                        genai.types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: genai.types.HarmBlockThreshold.BLOCK_ONLY_HIGH,
                    }
                )
                
                response = gemini_model.generate_content(simple_prompt)
                
                # Check if response has valid content
                if response.candidates and len(response.candidates) > 0:
                    candidate = response.candidates[0]
                    if candidate.content and candidate.content.parts:
                        return candidate.content.parts[0].text
                    else:
                        print(f"No content in simplified response. Finish reason: {candidate.finish_reason}")
                        # Use sentiment-appropriate response as fallback
                        emotion_context = messages[-1].get('emotionalContext', 'Neutral')
                        return get_smart_fallback_response(user_input, emotion_context, session_id)
                else:
                    print("No candidates in simplified response")
                    # Use sentiment-appropriate response as fallback
                    emotion_context = messages[-1].get('emotionalContext', 'Neutral')
                    return get_smart_fallback_response(user_input, emotion_context, session_id)
            except Exception as simple_e:
                print(f"Error with simplified approach: {simple_e}")
        
        # Try LangChain approach as a fallback
        try:
            # Create a prompt template with the therapist persona
            prompt = PromptTemplate(
                input_variables=["input"],
                template=f"{THERAPIST_PROMPT}\n\nUser: {{input}}\n\nRespond naturally and authentically with validation and support. Ask thoughtful questions to encourage dialogue. Provide complete, helpful responses."
            )
            
            # Use the modern RunnableSequence approach instead of deprecated LLMChain
            chain = prompt | model
            
            # Get response from the model
            response = chain.invoke({
                "input": user_input
            })
            
            return response.content if hasattr(response, 'content') else str(response)
        except Exception as inner_e:
            print(f"Error with LangChain approach: {inner_e}")
            
            # Use sentiment-appropriate response as last resort
            emotion_context = messages[-1].get('emotionalContext', 'Neutral')
            return get_smart_fallback_response(user_input, emotion_context, session_id)

def analyze_mood(text):
    """Analyze the mood/sentiment from text with retry mechanism"""
    if not GOOGLE_API_KEY or not api_configured:
        return keyword_mood_detection(text)
    
    # First try keyword-based detection for simple cases
    keyword_result = keyword_mood_detection(text)
    
    # If keyword detection finds something specific, use it
    if keyword_result != "Neutral":
        print(f"Keyword-based emotion detected: {keyword_result}")
        return keyword_result
    
    # For neutral cases, try AI analysis with simplified prompt
    try:
        # Simplified, safer prompt that's less likely to trigger safety filters
        prompt = f"""Classify this text emotion: "{text}"
        
        Options: Happy, Sad, Anxious, Angry, Neutral, Stressed, Depressed
        
        Reply with just one word from the options above."""
        
        generation_config = {
            "temperature": 0.1,  # Lower temperature for more consistent results
            "top_p": 0.8,
            "top_k": 10,
            "max_output_tokens": 50,  # Just need one word
        }
        
        # Use a more stable model for mood analysis
        model = genai.GenerativeModel(
            model_name="models/gemini-1.5-flash",  # More stable model
            generation_config=generation_config,
            safety_settings={
                genai.types.HarmCategory.HARM_CATEGORY_HATE_SPEECH: genai.types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                genai.types.HarmCategory.HARM_CATEGORY_HARASSMENT: genai.types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                genai.types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: genai.types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                genai.types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: genai.types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            }
        )
        
        response = model.generate_content(prompt)
        
        # Check if response has valid content
        if response.candidates and len(response.candidates) > 0:
            candidate = response.candidates[0]
            if candidate.content and candidate.content.parts:
                detected_emotion = candidate.content.parts[0].text.strip()
                
                # Validate the response is one of our expected emotions
                valid_emotions = ['Happy', 'Sad', 'Anxious', 'Angry', 'Neutral', 'Stressed', 'Depressed']
                if detected_emotion in valid_emotions:
                    print(f"AI-detected emotion for '{text}': {detected_emotion}")
                    return detected_emotion
                else:
                    print(f"Invalid AI emotion response: {detected_emotion}, using keyword fallback")
                    return keyword_mood_detection(text)
            else:
                print(f"No content in mood analysis response. Finish reason: {candidate.finish_reason}")
                return keyword_mood_detection(text)
        else:
            print("No candidates in mood analysis response")
            return keyword_mood_detection(text)
    
    except Exception as e:
        print(f"Error analyzing mood with AI: {e}")
        # Always fall back to keyword-based detection
        return keyword_mood_detection(text)

def combine_emotional_context(text):
    """Combine emotional analyses into a single context"""
    try:
        text_sentiment = analyze_mood(text)
        
        return text_sentiment
    except Exception as e:
        print(f"Error creating emotional context: {e}")
        return "Neutral"

def get_sentiment_response(user_input, emotion, session_id="default"):
    """Generate contextually aware response based on conversation history and emotion"""
    
    # Get conversation context from current session only
    conversation_context = current_session_memory.get(session_id, [])
    
    # If there's conversation history, build on it
    if len(conversation_context) > 1:
        return get_contextual_response(user_input, emotion, conversation_context, session_id)
    else:
        # First message - use the varied response system
        return get_varied_response(emotion, user_input, session_id)

def get_contextual_response(user_input, emotion, conversation_context, session_id):
    """Generate natural responses that properly build on conversation history"""
    
    # Extract what the user has actually shared in this conversation
    user_messages = []
    for msg in conversation_context:
        if msg['role'] == 'user':
            user_messages.append(msg['content'].lower())
    
    current_input = user_input.lower()
    
    # Detect user frustration patterns
    frustration_patterns = [
        'already said', 'i told you', 'mentioned that', 'said that',
        'not helping', 'not understanding', 'going anywhere', 'not working',
        'same thing', 'keep asking', 'what i said', 'told you already'
    ]
    
    conversation_stagnation_patterns = [
        'this conversation', 'not going anywhere', 'getting nowhere',
        'same questions', 'not helping', 'not understanding'
    ]
    
    # Handle user frustration
    if any(pattern in current_input for pattern in frustration_patterns):
        return handle_user_frustration(user_input, user_messages, session_id)
    
    # Handle conversation stagnation
    if any(pattern in current_input for pattern in conversation_stagnation_patterns):
        return handle_conversation_stagnation(user_input, user_messages, session_id)
    
    # Build on previous context
    context_response = build_on_context(user_input, user_messages, emotion, session_id)
    if context_response:
        return context_response
    
    # Default to natural emotion-based responses
    return get_natural_emotion_response(emotion, user_input, session_id)

def handle_user_frustration(user_input, user_messages, session_id):
    """Handle when user expresses frustration with the conversation"""
    
    # Acknowledge the frustration and reference what they've shared
    context_keywords = extract_context_keywords(user_messages)
    
    if context_keywords:
        context_str = ", ".join(context_keywords[:3])  # Use first 3 keywords
        return f"I hear your frustration, and you're right - I want to understand better. You've mentioned {context_str}. Can you help me understand what's been the most difficult part about this for you?"
    else:
        return "I hear your frustration, and I'm sorry I haven't been more helpful. Let me try a different approach - what would be most helpful for you to talk about right now?"

def handle_conversation_stagnation(user_input, user_messages, session_id):
    """Handle when user feels conversation isn't progressing"""
    
    context_keywords = extract_context_keywords(user_messages)
    
    if context_keywords:
        # Try to pivot to action or deeper exploration
        if 'stress' in context_keywords or 'work' in context_keywords:
            return "You're right, let's get more specific. You mentioned work stress - what's one thing that happened today that really got to you?"
        elif 'sad' in context_keywords:
            return "I hear you - let's go deeper. When you feel sad, what thoughts typically go through your mind?"
        elif 'anxious' in context_keywords:
            return "You're right, let's focus on something concrete. What's one situation that makes your anxiety spike?"
        else:
            return "Let's try something different. Instead of talking about feelings, what's one specific thing that happened recently that stuck with you?"
    else:
        return "You're absolutely right. Let's start fresh - what's one thing that's been really on your mind lately that you'd like to explore?"

def extract_context_keywords(user_messages):
    """Extract key topics and emotions from user messages"""
    keywords = []
    
    for msg in user_messages:
        msg_lower = msg.lower()
        
        # Emotion keywords
        if any(word in msg_lower for word in ['stress', 'overwhelmed', 'pressure']):
            keywords.append('work stress')
        elif any(word in msg_lower for word in ['sad', 'depressed', 'down']):
            keywords.append('sadness')
        elif any(word in msg_lower for word in ['anxious', 'worry', 'nervous']):
            keywords.append('anxiety')
        elif any(word in msg_lower for word in ['angry', 'frustrated', 'mad']):
            keywords.append('anger')
        
        # Context keywords
        if any(word in msg_lower for word in ['work', 'job', 'boss', 'career']):
            keywords.append('work')
        elif any(word in msg_lower for word in ['relationship', 'partner', 'boyfriend', 'girlfriend']):
            keywords.append('relationship')
        elif any(word in msg_lower for word in ['family', 'parents', 'kids', 'children']):
            keywords.append('family')
        elif any(word in msg_lower for word in ['school', 'college', 'university', 'class']):
            keywords.append('school')
        elif any(word in msg_lower for word in ['sleep', 'sleeping', 'insomnia']):
            keywords.append('sleep issues')
        elif any(word in msg_lower for word in ['thoughts', 'thinking', 'mind']):
            keywords.append('negative thoughts')
    
    return list(set(keywords))  # Remove duplicates

def build_on_context(user_input, user_messages, emotion, session_id):
    """Build naturally on previous conversation context"""
    
    if len(user_messages) < 2:
        return None  # Not enough context to build on
    
    current_input = user_input.lower()
    context_keywords = extract_context_keywords(user_messages)
    
    # Look for progression in the conversation
    if 'work' in context_keywords:
        if any(word in current_input for word in ['presentation', 'meeting', 'deadline', 'project']):
            return "Ah, so it's specifically about work pressure. That sounds really stressful. What's been the most challenging part of handling this?"
        elif any(word in current_input for word in ['boss', 'manager', 'supervisor']):
            return "That adds another layer of stress when it involves your boss. How has that been affecting your work environment?"
        elif any(word in current_input for word in ['lose', 'fired', 'laid off']):
            return "That's such a scary thought, especially when you have responsibilities. What makes you feel like your job might be at risk?"
    
    elif 'sadness' in context_keywords:
        if any(word in current_input for word in ['weeks', 'months', 'started', 'began']):
            return "That's helpful to know the timeline. What was happening in your life around the time this started?"
        elif any(word in current_input for word in ['relationship', 'breakup', 'ended']):
            return "Relationship endings can be so painful. How are you processing that loss?"
        elif any(word in current_input for word in ['thoughts', 'negative']):
            return "When we're sad, our thoughts can get really dark. What kinds of thoughts have been coming up for you?"
    
    elif 'anxiety' in context_keywords:
        if any(word in current_input for word in ['panic', 'attack', 'physical']):
            return "Anxiety can be so physical. What symptoms do you notice when it gets really intense?"
        elif any(word in current_input for word in ['social', 'people', 'crowds']):
            return "Social anxiety can be really isolating. What situations tend to trigger it most for you?"
    
    elif 'sleep issues' in context_keywords:
        if any(word in current_input for word in ['thinking', 'mind', 'racing']):
            return "That's so common - when we're trying to sleep, our minds can just take off. What kinds of thoughts keep you awake?"
        elif any(word in current_input for word in ['work', 'job', 'stress']):
            return "Work stress can definitely mess with sleep. How long has this been going on?"
    
    return None

def get_natural_emotion_response(emotion, user_input, session_id):
    """Generate natural, conversational responses based on emotion"""
    
    # Natural responses that don't sound templated
    natural_responses = {
        'Stressed': [
            "That sounds really tough. What's been weighing on you the most?",
            "I can hear the stress in what you're saying. What's been the biggest source of pressure lately?",
            "Stress can be so overwhelming. What's been going on that's making you feel this way?",
            "That's a lot to deal with. How long have you been feeling this stressed?",
            "It sounds like you're under a lot of pressure. What's been the hardest part to handle?"
        ],
        'Anxious': [
            "Anxiety can be really tough to deal with. What's been making you feel most anxious?",
            "That sounds really unsettling. What's been on your mind that's causing these feelings?",
            "I can imagine how difficult that must be. What situations tend to trigger your anxiety?",
            "Anxiety can be so draining. What's been worrying you the most recently?",
            "That must feel really intense. How have you been coping with these anxious feelings?"
        ],
        'Sad': [
            "I'm sorry you're going through a rough time. What's been making you feel this way?",
            "That sounds really painful. Do you want to talk about what's been going on?",
            "I can hear that you're hurting. What's been the most difficult part for you?",
            "That must be really hard. How long have you been feeling like this?",
            "It sounds like you're going through something tough. What's been weighing on your heart?"
        ],
        'Angry': [
            "That sounds really frustrating. What's been making you feel so angry?",
            "I can hear the frustration in what you're saying. What's been bothering you?",
            "That must be really maddening. What situation has been triggering these feelings?",
            "Anger is such a valid emotion. What's been the source of your frustration?",
            "That sounds infuriating. What's been the most irritating thing you've been dealing with?"
        ],
        'Happy': [
            "That's wonderful to hear! What's been going well for you?",
            "I love hearing good news! What's been making you feel so positive?",
            "That's great! What's been the highlight of your day?",
            "It's so nice to hear you sounding happy. What's been bringing you joy?",
            "That's fantastic! What's been contributing to these good feelings?"
        ],
        'Depressed': [
            "I'm really sorry you're feeling so low. What's been going on that's contributing to this?",
            "That sounds incredibly difficult. How long have you been feeling this way?",
            "I can hear how much you're struggling. What's been the hardest part?",
            "That must feel so heavy. What's been different about your mood lately?",
            "I'm sorry you're going through this. What's been making things feel especially tough?"
        ],
        'Neutral': [
            "I'm here to listen. What's been on your mind?",
            "How have you been doing? What's going on with you?",
            "What would you like to talk about? I'm here for you.",
            "I'm listening. What's been happening in your life?",
            "How are you feeling? What's been on your heart lately?"
        ]
    }
    
    # Get responses for this emotion
    responses = natural_responses.get(emotion, natural_responses['Neutral'])
    
    # Simple selection without complex tracking for now
    import random
    return random.choice(responses)

def keyword_mood_detection(text):
    """Enhanced keyword-based mood detection as ultimate fallback"""
    text_lower = text.lower().strip()
    
    # Handle very short or simple responses
    if len(text_lower) <= 3:
        return "Neutral"
    
    # Check for simple greetings and neutral responses
    neutral_patterns = [
        'hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening',
        'how are you', 'what\'s up', 'nothing much', 'not much', 'fine', 'okay',
        'ok', 'alright', 'sure', 'yes', 'no', 'maybe', 'i guess', 'can u respond'
    ]
    
    if any(pattern in text_lower for pattern in neutral_patterns):
        return "Neutral"
    
    # Check for frustration/anger patterns first (most specific)
    if any(phrase in text_lower for phrase in [
        'not helping', 'not understanding', 'already said', 'told you',
        'going anywhere', 'not working', 'frustrated', 'angry', 'mad',
        'annoyed', 'irritated', 'pissed', 'furious'
    ]):
        return "Angry"
    
    # Check for anxiety patterns
    elif any(word in text_lower for word in [
        'anxious', 'nervous', 'worry', 'worried', 'scared', 'fear', 'panic',
        'terrified', 'overwhelming', 'presentation', 'meeting', 'performance'
    ]):
        return "Anxious"
    
    # Check for stress patterns
    elif any(word in text_lower for word in [
        'stress', 'stressed', 'overwhelmed', 'pressure', 'burden', 'exhausted',
        'tired', 'overworked', 'workload', 'deadline', 'demanding', 'boss'
    ]):
        return "Stressed"
    
    # Check for depression patterns (more severe)
    elif any(phrase in text_lower for phrase in [
        'hopeless', 'no point', 'empty', 'nothing matters', 'end it all',
        'can\'t go on', 'worthless', 'meaningless', 'depressed', 'despair'
    ]) or any(word in text_lower for word in [
        'hopeless', 'empty', 'worthless', 'meaningless', 'despair', 'depressed'
    ]):
        return "Depressed"
    
    # Check for sadness patterns (more temporary)
    elif any(word in text_lower for word in [
        'sad', 'unhappy', 'down', 'blue', 'miserable', 'disappointed',
        'devastated', 'heartbroken', 'lonely', 'relationship ended',
        'breakup', 'broke up'
    ]):
        return "Sad"
    
    # Check for happiness patterns
    elif any(word in text_lower for word in [
        'happy', 'joy', 'great', 'wonderful', 'excited', 'amazing', 'fantastic',
        'love', 'awesome', 'thrilled', 'delighted', 'pleased', 'good', 'well'
    ]):
        return "Happy"
    
    # Check for sleep/health issues (often stress-related)
    elif any(phrase in text_lower for phrase in [
        'trouble sleeping', 'can\'t sleep', 'insomnia', 'sleep problems',
        'keep thinking', 'racing thoughts', 'mind racing'
    ]):
        return "Anxious"
    
    else:
        return "Neutral"

def get_smart_fallback_response(user_input, emotion, session_id):
    """Intelligent fallback when AI models fail"""
    
    # Get conversation context
    conversation_context = current_session_memory.get(session_id, [])
    user_messages = [msg['content'].lower() for msg in conversation_context if msg['role'] == 'user']
    bot_messages = [msg['content'] for msg in conversation_context if msg['role'] == 'assistant']
    
    # Check for frustration patterns first
    frustration_patterns = [
        'already said', 'i told you', 'mentioned that', 'said that',
        'not helping', 'not understanding', 'going anywhere', 'not working',
        'same thing', 'keep asking', 'what i said', 'told you already'
    ]
    
    user_input_lower = user_input.lower()
    
    if any(pattern in user_input_lower for pattern in frustration_patterns):
        response = handle_user_frustration(user_input, user_messages, session_id)
        # Add the response to session memory
        current_session_memory[session_id].append({"role": "assistant", "content": response})
        return response
    
    # Check for conversation stagnation
    conversation_stagnation_patterns = [
        'this conversation', 'not going anywhere', 'getting nowhere',
        'same questions', 'not helping', 'not understanding'
    ]
    
    if any(pattern in user_input_lower for pattern in conversation_stagnation_patterns):
        response = handle_conversation_stagnation(user_input, user_messages, session_id)
        # Add the response to session memory
        current_session_memory[session_id].append({"role": "assistant", "content": response})
        return response
    
    # If we have context, try to build on it
    if len(user_messages) > 1:
        context_keywords = extract_context_keywords(user_messages)
        
        # Generate context-aware responses that avoid repetition
        context_responses = []
        
        if 'work' in context_keywords or 'work stress' in context_keywords:
            context_responses = [
                "I hear you've been dealing with work stress. What's been the most challenging part about your work situation?",
                "Work stress can be really overwhelming. What's been the biggest pressure you're facing at work?",
                "That sounds like a lot of work pressure. How long have you been feeling this overwhelmed?",
                "I can see work has been really stressful for you. What's been the most difficult aspect to handle?"
            ]
        elif 'sadness' in context_keywords:
            context_responses = [
                "You mentioned feeling sad. What's been weighing on your heart the most?",
                "I hear that you're going through a difficult time. What's been the hardest part for you?",
                "That sounds really painful. How long have you been feeling this way?",
                "I'm sorry you're struggling with sadness. What's been contributing to these feelings?"
            ]
        elif 'anxiety' in context_keywords:
            context_responses = [
                "I can hear that you've been feeling anxious. What situations tend to trigger these feelings for you?",
                "Anxiety can be really tough. What's been worrying you the most?",
                "That sounds really stressful. What thoughts go through your mind when you feel anxious?",
                "I understand you're dealing with anxiety. What makes it feel most intense for you?"
            ]
        elif 'sleep issues' in context_keywords:
            context_responses = [
                "You mentioned having trouble sleeping. How long has this been affecting you?",
                "Sleep issues can be so frustrating. What's been keeping you awake at night?",
                "That must be exhausting. What's been going through your mind when you can't sleep?",
                "I hear sleep has been difficult. What do you think is causing these sleep problems?"
            ]
        elif 'relationship' in context_keywords:
            context_responses = [
                "I understand you've been dealing with relationship challenges. What's been the most difficult part for you?",
                "Relationship issues can be really painful. What's been going on that's been hardest to handle?",
                "That sounds emotionally challenging. How has this been affecting you day to day?",
                "I hear there have been relationship struggles. What's been weighing on you most about this?"
            ]
        elif 'family' in context_keywords:
            context_responses = [
                "Family situations can be really tough. What's been going on that's been challenging?",
                "I understand there have been family issues. What's been the most difficult part to deal with?",
                "Family dynamics can be complex. What's been bothering you most about this situation?",
                "That sounds like a lot to handle with family. What's been the biggest challenge for you?"
            ]
        
        # Select a response that hasn't been used recently
        if context_responses:
            unused_responses = [r for r in context_responses if r not in bot_messages]
            if unused_responses:
                selected_response = random.choice(unused_responses)
                # Add the response to session memory
                current_session_memory[session_id].append({"role": "assistant", "content": selected_response})
                return selected_response
            else:
                # All responses used, pick one anyway but modify it slightly
                base_response = random.choice(context_responses)
                modified_response = base_response.replace("What's been", "What has been").replace("I hear", "I can hear")
                # Add the response to session memory
                current_session_memory[session_id].append({"role": "assistant", "content": modified_response})
                return modified_response
    
    # Emotion-based fallback responses with variety
    fallback_responses = {
        "Stressed": [
            "It sounds like you're under a lot of pressure. What's been the most overwhelming part of what you're dealing with?",
            "That sounds really stressful. What's been causing you the most stress lately?",
            "I can hear the pressure you're under. What's been the hardest thing to manage?",
            "Stress can be so exhausting. What's been weighing on you the most?"
        ],
        "Anxious": [
            "I can hear the anxiety in what you're sharing. What's been worrying you the most?",
            "That sounds really unsettling. What's been on your mind that's causing these feelings?",
            "Anxiety can be overwhelming. What situations tend to trigger these feelings for you?",
            "I understand you're feeling anxious. What's been the source of your worry?"
        ],
        "Sad": [
            "I'm sorry you're going through a difficult time. What's been the hardest part for you?",
            "That sounds really painful. What's been weighing on your heart?",
            "I can hear that you're hurting. What's been going on that's making you feel this way?",
            "I'm sorry you're feeling sad. What's been contributing to these feelings?"
        ],
        "Angry": [
            "I can sense your frustration. What's been making you feel this way?",
            "That sounds really maddening. What's been the source of your anger?",
            "I hear the frustration in what you're sharing. What's been bothering you most?",
            "That must be really irritating. What's been the biggest trigger for these feelings?"
        ],
        "Happy": [
            "It's wonderful to hear some positivity! What's been going well for you?",
            "That's great to hear! What's been making you feel so good?",
            "I love hearing good news! What's been the highlight for you?",
            "That sounds fantastic! What's been bringing you joy?"
        ],
        "Depressed": [
            "I'm really sorry you're feeling so low. What's been contributing to these feelings?",
            "That sounds incredibly difficult. What's been the hardest part about feeling this way?",
            "I can hear how much you're struggling. What's been weighing on you most?",
            "I'm sorry you're going through this darkness. What's been making things feel especially tough?"
        ],
        "Neutral": [
            "I'm here to listen and support you. What's been on your mind that you'd like to talk about?",
            "How have you been feeling lately? What's been going on with you?",
            "I'm here for you. What would you like to explore together?",
            "What's been happening in your life that you'd like to share?"
        ]
    }
    
    responses = fallback_responses.get(emotion, fallback_responses["Neutral"])
    
    # Avoid repeating recent responses
    unused_responses = [r for r in responses if r not in bot_messages]
    if unused_responses:
        selected_response = random.choice(unused_responses)
        # Add the response to session memory
        current_session_memory[session_id].append({"role": "assistant", "content": selected_response})
        return selected_response
    else:
        # All responses used, pick one anyway
        selected_response = random.choice(responses)
        # Add the response to session memory
        current_session_memory[session_id].append({"role": "assistant", "content": selected_response})
        return selected_response

def cleanup_old_sessions():
    """Clean up old session memory to prevent memory buildup"""
    import time
    current_time = time.time()
    
    # Remove sessions older than 1 hour
    sessions_to_remove = []
    for session_id in current_session_memory.keys():
        if '_' in session_id:
            try:
                # Extract timestamp from session ID
                session_timestamp = int(session_id.split('_')[-1])
                if current_time - session_timestamp > 3600:  # 1 hour
                    sessions_to_remove.append(session_id)
            except (ValueError, IndexError):
                # If we can't parse timestamp, remove old format sessions
                sessions_to_remove.append(session_id)
    
    # Remove old sessions
    for session_id in sessions_to_remove:
        current_session_memory.pop(session_id, None)
        session_questions.pop(session_id, None)
        recent_responses.pop(session_id, None)


def should_recommend_video(user_message, conversation_history, emotional_context):
    """
    Intelligent function to determine if a video should be recommended
    based on the therapeutic guidelines provided.
    """
    user_message_lower = user_message.lower()
    
    # Check if this is the start of conversation (greeting only)
    if len(conversation_history) <= 2:  # Only bot greeting and user's first message
        greeting_patterns = [
            'hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening',
            'how are you', 'what\'s up', 'greetings'
        ]
        if any(pattern in user_message_lower for pattern in greeting_patterns) and len(user_message.split()) <= 5:
            return False, "Initial greeting - building rapport first"
    
    # Check if user explicitly asks for help, tips, or coping strategies
    help_requests = [
        'help', 'tips', 'advice', 'what should i do', 'how can i', 'ways to cope',
        'suggestions', 'strategies', 'techniques', 'exercises', 'guide me',
        'show me', 'teach me', 'recommend', 'what would you suggest'
    ]
    
    if any(request in user_message_lower for request in help_requests):
        return True, "User explicitly requested help or guidance"
    
    # Check emotional intensity and mood match
    if emotional_context:
        primary_emotion = emotional_context.get('dominant_emotion', '').lower()
        intensity = emotional_context.get('intensity', 0)
        
        # High intensity negative emotions warrant video recommendations
        high_intensity_emotions = ['sad', 'anxious', 'angry', 'stressed', 'overwhelmed', 'depressed', 'frustrated']
        
        if primary_emotion in high_intensity_emotions and intensity >= 0.6:
            return True, f"High intensity {primary_emotion} emotion detected (intensity: {intensity})"
    
    # Check for specific coping-related keywords in context
    coping_keywords = [
        'stressed', 'overwhelmed', 'anxious', 'panic', 'worried', 'nervous',
        'can\'t sleep', 'insomnia', 'tired', 'exhausted', 'angry', 'frustrated',
        'sad', 'depressed', 'down', 'upset', 'crying', 'hopeless'
    ]
    
    if any(keyword in user_message_lower for keyword in coping_keywords):
        return True, "User expressed emotional distress that could benefit from video support"
    
    # Check conversation context - has the user been sharing problems for a while?
    if len(conversation_history) >= 6:  # After some back and forth
        # Look for pattern of emotional sharing in recent messages
        recent_user_messages = [msg['content'].lower() for msg in conversation_history[-6:] if msg['role'] == 'user']
        emotional_words_count = 0
        for msg in recent_user_messages:
            emotional_words_count += sum(1 for word in coping_keywords if word in msg)
        
        if emotional_words_count >= 2:
            return True, "User has been expressing emotional concerns over multiple messages"
    
    # Don't recommend videos for general conversation
    return False, "No clear indication that user needs video support at this time"


def get_video_recommendation_context(emotional_context, user_message):
    """
    Generate appropriate context for video recommendations based on user's emotional state
    """
    if not emotional_context:
        return "general"
    
    primary_emotion = emotional_context.get('dominant_emotion', '').lower()
    user_message_lower = user_message.lower()
    
    # Map emotions to video types as per guidelines
    emotion_video_mapping = {
        'sad': 'uplifting',
        'depressed': 'motivational', 
        'anxious': 'breathing_exercise',
        'nervous': 'guided_meditation',
        'angry': 'grounding',
        'frustrated': 'relaxation',
        'overwhelmed': 'mindfulness',
        'stressed': 'calming'
    }
    
    # Check for sleep-related issues
    if any(word in user_message_lower for word in ['sleep', 'insomnia', 'tired', 'exhausted', 'can\'t sleep']):
        return 'bedtime_relaxation'
    
    return emotion_video_mapping.get(primary_emotion, 'general')