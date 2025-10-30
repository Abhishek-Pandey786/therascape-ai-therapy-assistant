# TheraScape - AI Therapy Assistant

TheraScape is an AI-powered therapy assistant designed to help users manage stress, anxiety, and depression through evidence-based therapeutic techniques.

## Features

- **AI-Powered Conversations**: Utilizes Google's Gemini 2.5 Flash model to provide empathetic and helpful responses.
- **Emotion Analysis**: Detects user emotions from text to provide more contextual responses.
- **Mood Tracking**: Visualizes mood changes over time through an interactive chart.
- **Voice Interaction**: Uses the Web Speech API for speech recognition and synthesis.
- **Therapeutic Resources**: Provides access to coping strategies, breathing exercises, and mindfulness techniques.
- **Responsive Design**: Works seamlessly on both desktop and mobile devices.

## Technology Stack

- **Backend**: Python with Flask
- **Frontend**: HTML, CSS, JavaScript
- **AI**: Google Gemini API via LangChain
- **Speech**: Web Speech API (browser-native)
- **UI Framework**: Bootstrap with Bootswatch Minty theme
- **Data Visualization**: Chart.js

## Setup Instructions

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv venv
   ```
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Create a `.env` file in the project root with the following:
   ```
   GOOGLE_API_KEY=your_gemini_api_key_here
   SECRET_KEY=your_secret_key_here
   FLASK_ENV=development
   ```
6. Run the application:
   ```
   python run.py
   ```
7. Access the application at `http://localhost:5000`

## Browser Compatibility

For voice functionality, please use a browser that supports the Web Speech API:

- Google Chrome (recommended)
- Microsoft Edge
- Safari (limited support)
- Firefox (limited support)

Voice features may not work correctly in older browsers or browsers without Web Speech API support.

## Project Structure

```
TherScape1/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── models/
│   │   ├── mood_scene_mapping.py
│   │   └── therapy_bot.py
│   ├── static/
│   │   ├── audio/
│   │   │   ├── forest-sounds.mp3
│   │   │   └── README.md
│   │   ├── css/
│   │   │   ├── breathing.css
│   │   │   ├── coping.css
│   │   │   ├── crisis.css
│   │   │   ├── forest-audio.css
│   │   │   ├── landing.css
│   │   │   ├── mindfulness.css
│   │   │   ├── style.css
│   │   │   └── therapeutic_tools.css
│   │   ├── images/
│   │   │   ├── robot-avatar.svg
│   │   │   └── robot.webm
│   │   └── js/
│   │       ├── breathing.js
│   │       ├── forest-audio.js
│   │       ├── landing.js
│   │       └── main.js
│   └── templates/
│       ├── breathing_exercises.html
│       ├── coping_strategies.html
│       ├── crisis.html
│       ├── index.html
│       ├── landing.html
│       └── mindfulness.html
├── .env
├── .gitignore
├── Backend_Integration_API_Documentation.md
├── Java_Developer_Quick_Guide.md
├── README.md
├── requirements.txt
└── run.py
```

## Important Notes

- This application is not a replacement for professional mental health treatment.
- Always seek help from qualified mental health professionals for serious concerns.
- The AI responses are generated based on patterns learned from data and may not always be appropriate for specific situations.
- Voice functionality requires a modern browser with Web Speech API support.

## Future Enhancements

- User authentication and personalized profiles
- Advanced voice customization options
- Integration with wearable devices for physiological data
- Expanded therapeutic techniques and resources
- Export and sharing of mood tracking data with healthcare providers
