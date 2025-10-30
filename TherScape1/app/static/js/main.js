// TheraScape Main JavaScript - Material UI Compatible
document.addEventListener('DOMContentLoaded', function() {
    // Initialize the application
    initializeApp();
    
    // Initialize voices for speech synthesis
    preloadVoices();
});

// Preload voices for speech synthesis
function preloadVoices() {
    // Try to load voices immediately
    loadVoices();
    
    // Set up event listener for when voices are ready
    if (window.speechSynthesis) {
        // Some browsers (especially Chrome) load voices asynchronously
        if (speechSynthesis.onvoiceschanged !== undefined) {
            speechSynthesis.onvoiceschanged = loadVoices;
        }
        
        // Force voice loading by making a silent speech request
        setTimeout(() => {
            const silentUtterance = new SpeechSynthesisUtterance('');
            silentUtterance.volume = 0;
            silentUtterance.onend = () => {
                // Try loading voices again after silent utterance
                loadVoices();
            };
            speechSynthesis.speak(silentUtterance);
        }, 500);
    }
}

// Load available voices for speech synthesis
let availableVoices = [];
function loadVoices() {
    if (!window.speechSynthesis) return;
    
    availableVoices = window.speechSynthesis.getVoices();
    console.log(`Loaded ${availableVoices.length} voices for speech synthesis`);
    
    // Debug: List all available voices
    if (availableVoices.length > 0) {
        console.log('Available voices:');
        availableVoices.forEach(voice => {
            console.log(`- ${voice.name} (${voice.lang})${voice.default ? ' [default]' : ''}`);
        });
    }
}

// Personalized Greetings & Check-ins
let userName = null;
let userMessageCount = 0;

function showNameModal() {
    const modal = document.getElementById('nameModal');
    if (modal) modal.style.display = 'flex';
}

function hideNameModal() {
    const modal = document.getElementById('nameModal');
    if (modal) modal.style.display = 'none';
}

function getUserName() {
    // First check sessionStorage (from landing page)
    const sessionName = sessionStorage.getItem('userName');
    if (sessionName) {
        return sessionName;
    }
    // Fall back to localStorage for backward compatibility
    return localStorage.getItem('therascapeUserName') || null;
}

function setUserName(name) {
    // Store in both sessionStorage and localStorage
    sessionStorage.setItem('userName', name);
    localStorage.setItem('therascapeUserName', name);
    userName = name;
}

function insertPersonalizedWelcome() {
    const chatMessages = document.getElementById('chatMessages');
    if (!chatMessages) return;
    
    let greeting;
    if (userName) {
        if (window.userContext && window.userContext.mode === 'demo') {
            greeting = `Hello ${userName}! Welcome to TheraScape demo mode. I'm your AI therapy assistant. Note: This is a demo session and your conversation won't be saved. How are you feeling today?`;
        } else {
            greeting = `Hello ${userName}, I'm TheraScape, your AI therapy assistant. How are you feeling today?`;
        }
    } else {
        greeting = `Hello, I'm TheraScape, your AI therapy assistant. How are you feeling today?`;
    }
    
    addMessageToChat('bot', greeting);
    
    // Update robot header for personalized greeting
    if (userName) {
        setTimeout(() => {
            const robotStatus = document.getElementById('robotStatus');
            if (robotStatus && !window.userContext) {
                // Only update if not already set by backend template
                robotStatus.textContent = `Welcome ${userName}! Let's talk.`;
            }
        }, 2000);
    }
}

function insertCheckInMessage() {
    const checkIns = [
        "Just checking in—how are you feeling right now? Would you like to take a short break or continue?",
        "Remember, it's okay to pause and take a breath. How are you doing so far?",
        "If you need a moment, that's perfectly fine. Would you like to share how you're feeling at this point?"
    ];
    const msg = checkIns[Math.floor(Math.random() * checkIns.length)];
    addMessageToChat('bot', msg);
}

// Clear any cached user data and get fresh data from landing page
function clearCachedUserData() {
    // Clear old localStorage data to prevent conflicts
    localStorage.removeItem('therascapeUserName');
    console.log('Cleared cached user data');
}

// Load conversation history from server
async function loadConversationHistory() {
    try {
        const response = await fetch('/get_conversation_history', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        if (!response.ok) {
            console.log('No conversation history available or server error');
            return;
        }
        
        const data = await response.json();
        
        if (data.success && data.conversation && data.conversation.length > 0) {
            console.log(`Loading ${data.conversation.length} previous messages`);
            
            // Restore conversation to chat UI
            const chatMessages = document.getElementById('chatMessages');
            if (chatMessages) {
                // Clear any existing messages first
                chatMessages.innerHTML = '';
                
                // Add each message from history
                data.conversation.forEach(message => {
                    if (message.sender === 'user') {
                        addMessageToChat('user', message.content);
                        userMessageCount++; // Track user messages for check-ins
                    } else if (message.sender === 'bot') {
                        addMessageToChat('bot', message.content, message.emotion || null);
                        
                        // Update mood chart if emotion data exists
                        if (message.emotion) {
                            updateMoodChart(message.emotion);
                            updateRobotMood(message.emotion);
                        }
                    }
                });
                
                // Scroll to bottom of chat
                chatMessages.scrollTop = chatMessages.scrollHeight;
                
                console.log('Successfully restored conversation history');
            }
        } else {
            console.log('No previous conversation found');
        }
    } catch (error) {
        console.error('Error loading conversation history:', error);
        // Don't throw error - continue with app initialization
    }
}

// Clear conversation history
async function clearConversationHistory() {
    try {
        // Show loading state
        const startFreshBtn = document.getElementById('startFresh');
        if (startFreshBtn) {
            startFreshBtn.innerHTML = '<span class="material-icons">hourglass_empty</span> Clearing...';
            startFreshBtn.disabled = true;
        }
        
        const response = await fetch('/clear_conversation', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        if (response.ok) {
            const data = await response.json();
            if (data.success) {
                // Clear chat UI
                const chatMessages = document.getElementById('chatMessages');
                if (chatMessages) {
                    chatMessages.innerHTML = '';
                }
                
                // Reset user message count
                userMessageCount = 0;
                
                console.log('Conversation history cleared successfully');
                return true;
            }
        }
        
        console.error('Failed to clear conversation history');
        return false;
    } catch (error) {
        console.error('Error clearing conversation history:', error);
        return false;
    } finally {
        // Reset button state
        const startFreshBtn = document.getElementById('startFresh');
        if (startFreshBtn) {
            startFreshBtn.innerHTML = '<span class="material-icons">refresh</span> Start Fresh';
            startFreshBtn.disabled = false;
        }
    }
}

// Check for previous conversation and show continuation modal
async function checkForPreviousConversation() {
    console.log('🔍 Checking for previous conversation...');
    try {
        const response = await fetch('/check_previous_conversation', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        if (!response.ok) {
            console.log('❌ Error checking previous conversation - response not ok');
            // Fall back to loading any existing conversation
            loadConversationHistory().then(() => {
                const chatMessages = document.getElementById('chatMessages');
                if (!chatMessages || chatMessages.children.length === 0) {
                    insertPersonalizedWelcome();
                }
            });
            return;
        }
        
        const data = await response.json();
        console.log('📊 Previous conversation check result:', data);
        
        if (data.success && data.has_previous_conversation) {
            console.log(`✅ Found previous conversation with ${data.message_count} messages - showing modal`);
            showChatContinuationModal();
        } else {
            console.log('ℹ️ No previous conversation found - showing welcome');
            // No previous conversation, show welcome
            insertPersonalizedWelcome();
        }
    } catch (error) {
        console.error('❌ Error checking previous conversation:', error);
        // Fall back to loading any existing conversation
        loadConversationHistory().then(() => {
            const chatMessages = document.getElementById('chatMessages');
            if (!chatMessages || chatMessages.children.length === 0) {
                insertPersonalizedWelcome();
            }
        });
    }
}

// Show chat continuation modal
function showChatContinuationModal() {
    console.log('🎭 Attempting to show chat continuation modal...');
    const modal = document.getElementById('chatContinuationModal');
    console.log('🎭 Modal element found:', modal);
    
    if (modal) {
        console.log('✅ Showing chat continuation modal');
        modal.style.display = 'flex';
        
        // Set up event listeners for the buttons
        const continueBtn = document.getElementById('continueChat');
        const startFreshBtn = document.getElementById('startFresh');
        
        console.log('🔘 Continue button found:', continueBtn);
        console.log('🔘 Start fresh button found:', startFreshBtn);
        
        continueBtn.onclick = function() {
            console.log('👥 User chose to continue previous conversation');
            hideChatContinuationModal();
            // Load previous conversation
            loadConversationHistory().then(() => {
                console.log('Continued previous conversation');
            });
        };
        
        startFreshBtn.onclick = async function() {
            console.log('🆕 User chose to start fresh conversation');
            hideChatContinuationModal();
            // Clear conversation and start fresh
            const cleared = await clearConversationHistory();
            if (cleared) {
                console.log('Started fresh conversation');
                insertPersonalizedWelcome();
            } else {
                console.error('Failed to clear conversation');
                // Fall back to showing welcome anyway
                insertPersonalizedWelcome();
            }
        };
    }
}

// Hide chat continuation modal
function hideChatContinuationModal() {
    console.log('🙈 Hiding chat continuation modal');
    const modal = document.getElementById('chatContinuationModal');
    if (modal) {
        modal.style.display = 'none';
        console.log('✅ Modal hidden successfully');
    } else {
        console.log('❌ Modal element not found when trying to hide');
    }
}

// Override initializeApp to handle name modal and welcome
function initializeApp() {
    // Clear any cached data first
    clearCachedUserData();
    
    // Check if user context is available from backend
    if (window.userContext && window.userContext.name) {
        // User context provided by backend (authenticated or demo mode)
        userName = window.userContext.name;
        console.log('🌟 Using user context from backend:', window.userContext);
        
        // Set user name in storage for consistency
        setUserName(userName);
        
        // For authenticated users, check if they have previous conversation
        if (window.userContext.mode === 'authenticated' || window.userContext.saveSession) {
            console.log('✅ User is authenticated or saving session - checking for previous conversation');
            checkForPreviousConversation();
        } else {
            console.log('👥 Demo mode - loading session conversation');
            // Demo mode - load any session conversation and show welcome if needed
            loadConversationHistory().then(() => {
                const chatMessages = document.getElementById('chatMessages');
                if (!chatMessages || chatMessages.children.length === 0) {
                    insertPersonalizedWelcome();
                }
            });
        }
    } else {
        // Fallback to previous behavior for legacy support
        userName = getUserName();
        console.log('Initializing app with userName:', userName);
        console.log('SessionStorage userName:', sessionStorage.getItem('userName'));
        console.log('LocalStorage userName:', localStorage.getItem('therascapeUserName'));
        
        if (!userName) {
            showNameModal();
            const nameForm = document.getElementById('nameForm');
            nameForm.onsubmit = function(e) {
                e.preventDefault();
                const input = document.getElementById('userNameInput');
                if (input.value.trim()) {
                    setUserName(input.value.trim());
                    hideNameModal();
                    loadConversationHistory().then(() => {
                        // Only show welcome if no previous conversation
                        const chatMessages = document.getElementById('chatMessages');
                        if (!chatMessages || chatMessages.children.length === 0) {
                            insertPersonalizedWelcome();
                        }
                    });
                }
            };
        } else {
            loadConversationHistory().then(() => {
                // Only show welcome if no previous conversation
                const chatMessages = document.getElementById('chatMessages');
                if (!chatMessages || chatMessages.children.length === 0) {
                    insertPersonalizedWelcome();
                }
            });
        }
    }
    
    initializeChat();
    initializeMoodChart();
    initializeMoodDisplay(); // Initialize mood detection display
    initializeSessionTimer();
    initializeEmojiPicker();
    initializeRobotHeader(); // Initialize robot header
    initializeVoiceChat(); // Initialize voice chat functionality
    initializeLogoutButton(); // Initialize logout functionality
}

// Override initializeChat to count user messages and check-in
function initializeChat() {
    const chatForm = document.getElementById('chatForm');
    const userMessageInput = document.getElementById('userMessage');
    const chatMessages = document.getElementById('chatMessages');
    const typingIndicator = document.getElementById('typingIndicator');
    if (!chatForm || !userMessageInput || !chatMessages) {
        console.warn('Chat elements not found');
        return;
    }
    chatForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Don't process form submission in voice mode
        if (currentChatMode === 'voice') {
            return;
        }
        
        const message = userMessageInput.value.trim();
        if (!message) return;
        
        // Show analyzing mood state
        showMoodAnalyzing();
        
        addMessageToChat('user', message);
        userMessageInput.value = '';
        userMessageCount++;
        // Periodic check-in every 6 user messages
        if (userMessageCount > 0 && userMessageCount % 6 === 0) {
            setTimeout(() => insertCheckInMessage(), 1200);
        }            // Show typing indicator and delay before bot response
            showTypingIndicator();
            updateRobotStatus("Processing your message...");
            
            try {
                // Simulate human-like pause (1-2s)
                await new Promise(res => setTimeout(res, 1000 + Math.random() * 1000));
                
                // Send message to server
            console.log('Sending message with userName:', userName);
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    message: message, 
                    userName: userName,
                    voice_mode: false 
                })
            });
            const data = await response.json();
            hideTypingIndicator();
            if (data.success) {
                // Check if video recommendations are included
                const videos = data.videos || [];
                addMessageToChat('bot', data.response, data.emotion, videos);
                
                if (data.emotion) {
                    updateMoodChart(data.emotion);
                    updateRobotMood(data.emotion);
                    // Update mood detection display
                    updateMoodDisplay(data.emotion, Math.floor(80 + Math.random() * 20));
                }
                
                // Analyze mood with Java backend
                await analyzeMoodWithJavaBackend(message);
                
                // Trigger robot header talking animation
                triggerRobotHeaderTalking(data.response.length * 60);
            } else {
                addMessageToChat('bot', 'I apologize, but I\'m having trouble processing your message right now. Please try again in a moment.');
            }
        } catch (error) {
            console.error('Error sending message:', error);
            hideTypingIndicator();
            addMessageToChat('bot', 'I apologize, but I\'m experiencing technical difficulties. Please try again later.');
            updateRobotStatus("Ready to help you feel better");
        }
    });
    if (userMessageInput.tagName === 'TEXTAREA') {
        userMessageInput.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = this.scrollHeight + 'px';
        });
    }
}

function addMessageToChat(sender, message, emotion = null) {
    const chatMessages = document.getElementById('chatMessages');
    if (!chatMessages) return;
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    
    // Create message wrapper for bot messages (to include avatar)
    if (sender === 'bot') {
        const messageWrapper = document.createElement('div');
        messageWrapper.className = 'bot-message-wrapper';
        
        // Add robot avatar using the new function
        const avatar = createRobotAvatar(32);
        
        messageWrapper.appendChild(avatar);
        messageWrapper.appendChild(messageDiv);
        
        // Add the wrapper to chat instead of messageDiv directly
        chatMessages.appendChild(messageWrapper);
    } else {
        chatMessages.appendChild(messageDiv);
    }
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    
    const messageText = document.createElement('p');
    messageText.textContent = message;
    messageContent.appendChild(messageText);
    
    // Add emotion indicator if available
    if (emotion && sender === 'bot') {
        const emotionIndicator = document.createElement('span');
        emotionIndicator.className = `emotion-indicator emotion-${emotion.toLowerCase()}`;
        messageText.appendChild(emotionIndicator);
    }
    
    // Add timestamp
    const timestamp = document.createElement('div');
    timestamp.className = 'message-time';
    timestamp.textContent = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    messageContent.appendChild(timestamp);
    
    messageDiv.appendChild(messageContent);
    
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    // Add animation and speech for bot messages
    if (sender === 'bot') {
        // Animate the avatar with a slight bounce
        const avatarElement = messageDiv.parentElement?.querySelector('.bot-avatar');
        if (avatarElement) {
            avatarElement.style.animation = 'avatarBounce 0.6s ease-out';
            
            // Trigger talking animation
            setTimeout(() => {
                triggerRobotTalking(avatarElement, message.length * 50); // Duration based on message length
            }, 300);
        }
        
        // Always speak bot responses (regardless of input method)
        setTimeout(() => {
            speakResponse(message);
        }, 500); // Small delay to allow message to appear first
    }
    
    messageDiv.style.animation = 'fadeInUp 0.3s ease-out';
}

// Robot avatar video handling
function createRobotAvatar(size = 32) {
    const avatarDiv = document.createElement('div');
    avatarDiv.className = 'bot-avatar';
    
    const video = document.createElement('video');
    video.width = size - 4; // Account for border
    video.height = size - 4;
    video.autoplay = true;
    video.loop = true;
    video.muted = true;
    video.playsInline = true;
    
    const source = document.createElement('source');
    source.src = '/static/images/robot.webm';
    source.type = 'video/webm';
    
    video.appendChild(source);
    
    // Fallback SVG
    const fallbackSVG = `
        <svg width="${size - 8}" height="${size - 8}" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="8" y="12" width="24" height="20" rx="4" fill="#6C63FF" stroke="#4A47A3" stroke-width="2"/>
            <line x1="20" y1="8" x2="20" y2="12" stroke="#4A47A3" stroke-width="2" stroke-linecap="round"/>
            <circle cx="20" cy="6" r="2" fill="#FF6B6B"/>
            <circle cx="15" cy="18" r="2" fill="#FFFFFF"/>
            <circle cx="25" cy="18" r="2" fill="#FFFFFF"/>
            <circle cx="15" cy="18" r="1" fill="#4A47A3"/>
            <circle cx="25" cy="18" r="1" fill="#4A47A3"/>
            <rect x="17" y="24" width="6" height="3" rx="1.5" fill="#4A47A3"/>
            <rect x="12" y="32" width="16" height="8" rx="2" fill="#8B7CF6" stroke="#6C63FF" stroke-width="1"/>
            <rect x="4" y="34" width="8" height="3" rx="1.5" fill="#A78BFA"/>
            <rect x="28" y="34" width="8" height="3" rx="1.5" fill="#A78BFA"/>
            <circle cx="20" cy="36" r="1" fill="#FFFFFF" opacity="0.7"/>
            <rect x="18" y="38" width="4" height="1" rx="0.5" fill="#FFFFFF" opacity="0.7"/>
        </svg>
    `;
    
    // Error handling for video
    video.addEventListener('error', function() {
        console.log('Video failed to load, using SVG fallback');
        avatarDiv.innerHTML = fallbackSVG;
    });
    
    video.addEventListener('loadeddata', function() {
        console.log('Robot animation loaded successfully');
    });
    
    avatarDiv.appendChild(video);
    return avatarDiv;
}

// Enhanced robot talking animation
function triggerRobotTalking(avatarElement, duration = 3000) {
    if (!avatarElement) return;
    
    avatarElement.classList.add('talking');
    
    // Add some randomness to the talking animation
    const video = avatarElement.querySelector('video');
    if (video) {
        // Slightly change playback rate for variety
        video.playbackRate = 0.8 + Math.random() * 0.4; // 0.8 to 1.2
    }
    
    setTimeout(() => {
        avatarElement.classList.remove('talking');
        if (video) {
            video.playbackRate = 1; // Reset to normal speed
        }
    }, duration);
}

function showTypingIndicator() {
    const typingIndicator = document.getElementById('typingIndicator');
    if (typingIndicator) {
        typingIndicator.classList.add('show');
        typingIndicator.scrollIntoView({ behavior: 'smooth' });
    }
}

function hideTypingIndicator() {
    const typingIndicator = document.getElementById('typingIndicator');
    if (typingIndicator) {
        typingIndicator.classList.remove('show');
    }
}

function initializeMoodChart() {
    const chartCanvas = document.getElementById('moodChart');
    if (!chartCanvas) return;
    
    const ctx = chartCanvas.getContext('2d');
    
    // Initialize with empty data - we'll fetch real data from backend
    const moodData = {
        labels: [],
        datasets: [{
            label: 'Mood Level',
            data: [],
            borderColor: 'rgba(255, 255, 255, 0.3)',
            backgroundColor: 'rgba(255, 255, 255, 0.05)',
            pointBorderColor: [],  // Will be set dynamically based on mood
            pointBackgroundColor: [],  // Will be set dynamically based on mood
            pointRadius: 6,
            pointHoverRadius: 8,
            pointBorderWidth: 2,
            borderWidth: 2,
            fill: true,
            tension: 0.4
        }]
    };
    
    const moodChart = new Chart(ctx, {
        type: 'line',
        data: moodData,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const moodLabels = {
                                9: 'Happy',
                                6: 'Neutral',
                                4: 'Anxious/Stressed',
                                3: 'Sad',
                                2: 'Angry/Depressed'
                            };
                            const value = context.parsed.y;
                            const emotion = moodLabels[value] || 'Neutral';
                            return `Mood: ${emotion} (${value}/10)`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    ticks: {
                        color: 'rgba(255, 255, 255, 0.8)',
                        font: {
                            size: 10
                        }
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    }
                },
                y: {
                    beginAtZero: true,
                    max: 10,
                    ticks: {
                        color: 'rgba(255, 255, 255, 0.8)',
                        font: {
                            size: 10
                        }
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    }
                }
            },
            elements: {
                point: {
                    backgroundColor: 'rgba(255, 255, 255, 0.8)',
                    borderColor: 'rgba(255, 255, 255, 1)',
                    borderWidth: 2,
                    radius: 4
                }
            }
        }
    });
    
    // Store chart reference for updates
    window.moodChart = moodChart;
    
    // Fetch initial mood data from server
    fetchMoodData();
}

// Fetch mood data from server
async function fetchMoodData() {
    try {
        const response = await fetch('/get_mood_data');
        const data = await response.json();
        
        if (data.success && data.mood_data && data.mood_data.length > 0) {
            // Update chart with real mood data
            const chart = window.moodChart;
            if (!chart) return;
            
            // Clear existing data
            chart.data.labels = [];
            chart.data.datasets[0].data = [];
            
            // Add new data points
            data.mood_data.forEach(entry => {
                chart.data.labels.push(entry.date);
                chart.data.datasets[0].data.push(entry.score);
            });
            
            // Set different colors based on mood values FIRST
            setMoodChartColors(chart, data.mood_data);
            
            // Then update chart without animation for the initial load
            chart.update('none');
        }
    } catch (error) {
        console.error('Error fetching mood data:', error);
    }
}

// Set different colors for mood chart based on emotions
function setMoodChartColors(chart, moodData) {
    if (!chart || !moodData || !moodData.length) return;
    
    // Function to get color based on score
    const getColorForScore = (score) => {
        if (score >= 9) return 'rgba(46, 204, 113, 0.8)';      // Green for Happy (9-10)
        if (score >= 6) return 'rgba(52, 152, 219, 0.8)';      // Blue for Neutral (6-8)
        if (score >= 4) return 'rgba(241, 196, 15, 0.8)';      // Yellow for Anxious/Stressed (4-5)
        if (score >= 3) return 'rgba(243, 156, 18, 0.8)';      // Orange for Sad (3)
        return 'rgba(231, 76, 60, 0.8)';                       // Red for Angry/Depressed (1-2)
    };
    
    // Initialize point color arrays if they don't exist
    if (!chart.data.datasets[0].pointBorderColor) {
        chart.data.datasets[0].pointBorderColor = [];
        chart.data.datasets[0].pointBackgroundColor = [];
    }
    
    // Clear existing point colors
    chart.data.datasets[0].pointBorderColor = [];
    chart.data.datasets[0].pointBackgroundColor = [];
    
    // Set individual point colors based on mood scores
    moodData.forEach(entry => {
        const color = getColorForScore(entry.score);
        chart.data.datasets[0].pointBorderColor.push(color);
        chart.data.datasets[0].pointBackgroundColor.push(color);
    });
    
    // Set overall chart colors to a neutral gradient
    const ctx = chart.ctx;
    const chartArea = chart.chartArea;
    const gradient = ctx.createLinearGradient(0, chartArea.bottom, 0, chartArea.top);
    gradient.addColorStop(0, 'rgba(255, 255, 255, 0.05)');
    gradient.addColorStop(1, 'rgba(255, 255, 255, 0.1)');
    
    chart.data.datasets[0].backgroundColor = gradient;
    chart.data.datasets[0].borderColor = 'rgba(255, 255, 255, 0.3)';
    chart.update('none');
}

function updateMoodChart(emotion) {
    if (!window.moodChart) return;
    
    // Convert emotion to mood score (1-10)
    const emotionScores = {
        'happy': 9,
        'sad': 3,
        'anxious': 4,
        'angry': 2,
        'neutral': 6,
        'stressed': 4,
        'depressed': 2
    };
    
    // Mood colors to match the legend
    const moodColors = {
        'happy': 'rgba(46, 204, 113, 0.8)',     // Green for Happy (9-10)
        'neutral': 'rgba(52, 152, 219, 0.8)',   // Blue for Neutral (6-7)
        'anxious': 'rgba(241, 196, 15, 0.8)',   // Yellow for Anxious/Stressed (4-5)
        'stressed': 'rgba(241, 196, 15, 0.8)',  // Yellow for Anxious/Stressed (4-5)
        'sad': 'rgba(243, 156, 18, 0.8)',       // Orange for Sad (3)
        'angry': 'rgba(231, 76, 60, 0.8)',      // Red for Angry/Depressed (1-2)
        'depressed': 'rgba(231, 76, 60, 0.8)'   // Red for Angry/Depressed (1-2)
    };
    
    const score = emotionScores[emotion.toLowerCase()] || 6;
    const color = moodColors[emotion.toLowerCase()] || 'rgba(52, 152, 219, 0.8)';
    
    // Add new data point
    const chart = window.moodChart;
    const newLabel = new Date().toLocaleDateString('en-US', { weekday: 'short' });
    
    chart.data.labels.push(newLabel);
    chart.data.datasets[0].data.push(score);
    
    // Initialize point color arrays if they don't exist
    if (!chart.data.datasets[0].pointBorderColor) {
        chart.data.datasets[0].pointBorderColor = [];
    }
    if (!chart.data.datasets[0].pointBackgroundColor) {
        chart.data.datasets[0].pointBackgroundColor = [];
    }
    
    // Add the color for this specific data point
    chart.data.datasets[0].pointBorderColor.push(color);
    chart.data.datasets[0].pointBackgroundColor.push(color);
    
    // Keep only last 7 data points
    if (chart.data.labels.length > 7) {
        chart.data.labels.shift();
        chart.data.datasets[0].data.shift();
        chart.data.datasets[0].pointBorderColor.shift();
        chart.data.datasets[0].pointBackgroundColor.shift();
    }
    
    // Update chart with animation
    chart.update();
    
    // Update the mood data on the server
    fetchMoodData();
}

function initializeSessionTimer() {
    const sessionTimer = document.getElementById('sessionTimer');
    if (!sessionTimer) return;
    
    let startTime = Date.now();
    
    function updateTimer() {
        const elapsed = Date.now() - startTime;
        const minutes = Math.floor(elapsed / 60000);
        const seconds = Math.floor((elapsed % 60000) / 1000);
        
        sessionTimer.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    }
    
    // Update timer every second
    setInterval(updateTimer, 1000);
    updateTimer(); // Initial update
}

function initializeEmojiPicker() {
    const emojiBtn = document.querySelector('.emoji-btn');
    if (!emojiBtn) return;
    
    emojiBtn.addEventListener('click', function() {
        // Simple emoji picker - in a real app, you might want a more sophisticated one
        const emojis = ['😊', '😢', '😡', '😰', '😴', '😌', '🤗', '😔'];
        const randomEmoji = emojis[Math.floor(Math.random() * emojis.length)];
        
        const userMessageInput = document.getElementById('userMessage');
        if (userMessageInput) {
            userMessageInput.value += randomEmoji;
            userMessageInput.focus();
        }
    });
}

// Robot header management
function initializeRobotHeader() {
    const robotHeader = document.getElementById('chatRobotHeader');
    const robotStatus = document.getElementById('robotStatus');
    const robotMoodIndicator = document.getElementById('robotMoodIndicator');
    
    if (!robotHeader) return;
    
    // Add entrance animation
    robotHeader.style.animation = 'fadeInUp 0.8s ease-out';
    
    // Update robot status based on time of day
    updateRobotGreeting();
    
    // Add click interaction
    const robotAvatar = robotHeader.querySelector('.robot-avatar-large');
    if (robotAvatar) {
        robotAvatar.addEventListener('click', function() {
            triggerRobotHeaderAnimation();
        });
    }
}

function updateRobotGreeting() {
    const robotStatus = document.getElementById('robotStatus');
    if (!robotStatus) return;
    
    const hour = new Date().getHours();
    let greeting;
    
    if (hour < 12) {
        greeting = "Good morning! Ready to start your day positively?";
    } else if (hour < 17) {
        greeting = "Good afternoon! How are you feeling today?";
    } else {
        greeting = "Good evening! Let's unwind and reflect together.";
    }
    
    robotStatus.textContent = greeting;
}

function updateRobotMood(emotion) {
    const moodIndicator = document.getElementById('robotMoodIndicator');
    if (!moodIndicator) return;
    
    const moodIcon = moodIndicator.querySelector('.mood-icon');
    if (!moodIcon) return;
    
    const moodEmojis = {
        'Happy': '😊',
        'Sad': '😔',
        'Anxious': '😰',
        'Angry': '😠',
        'Stressed': '😵',
        'Depressed': '😞',
        'Neutral': '🤖'
    };
    
    const emoji = moodEmojis[emotion] || '🤖';
    moodIcon.textContent = emoji;
    
    // Add a little bounce animation
    moodIcon.style.animation = 'moodIconBounce 0.8s ease-out';
    setTimeout(() => {
        moodIcon.style.animation = 'moodIconBounce 2s ease-in-out infinite';
    }, 800);
}

function triggerRobotHeaderAnimation() {
    const robotAvatar = document.querySelector('.robot-avatar-large');
    const robotStatus = document.getElementById('robotStatus');
    
    if (robotAvatar) {
        robotAvatar.classList.add('talking');
        setTimeout(() => {
            robotAvatar.classList.remove('talking');
        }, 2000);
    }
    
    if (robotStatus) {
        const encouragements = [
            "I'm here to listen! 💙",
            "You're doing great! 🌟",
            "Let's work through this together! 🤝",
            "Your feelings are valid! ✨",
            "Take your time, I'm here! 🕐"
        ];
        
        const originalText = robotStatus.textContent;
        const randomEncouragement = encouragements[Math.floor(Math.random() * encouragements.length)];
        
        robotStatus.textContent = randomEncouragement;
        robotStatus.style.color = '#FFE066';
        
        setTimeout(() => {
            robotStatus.textContent = originalText;
            robotStatus.style.color = '';
        }, 3000);
    }
}

function updateRobotStatus(message) {
    const robotStatus = document.getElementById('robotStatus');
    if (!robotStatus) return;
    
    const statusMessages = [
        "Processing your message...",
        "Thinking about the best response...",
        "Understanding your feelings...",
        "Preparing a thoughtful reply..."
    ];
    
    const originalStatus = robotStatus.textContent;
    const randomStatus = statusMessages[Math.floor(Math.random() * statusMessages.length)];
    
    robotStatus.textContent = randomStatus;
    robotStatus.style.fontStyle = 'italic';
    robotStatus.style.opacity = '0.8';
    
    // Reset after response
    setTimeout(() => {
        robotStatus.textContent = originalStatus;
        robotStatus.style.fontStyle = '';
        robotStatus.style.opacity = '';
    }, 2000);
}

function triggerRobotHeaderTalking(duration = 3000) {
    const robotAvatar = document.querySelector('.robot-avatar-large');
    if (!robotAvatar) return;
    
    robotAvatar.classList.add('talking');
    
    // Add some variety to the animation
    const video = robotAvatar.querySelector('video');
    if (video) {
        video.playbackRate = 0.9 + Math.random() * 0.2; // 0.9 to 1.1
    }
    
    setTimeout(() => {
        robotAvatar.classList.remove('talking');
        if (video) {
            video.playbackRate = 1;
        }
    }, duration);
}

// Utility function to show loading state
function showLoading() {
    const chatMessages = document.getElementById('chatMessages');
    if (!chatMessages) return;
    
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'message bot-message loading-indicator';
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    
    const loadingText = document.createElement('p');
    loadingText.innerHTML = '<span class="dot"></span><span class="dot"></span><span class="dot"></span>';
    messageContent.appendChild(loadingText);
    
    loadingDiv.appendChild(messageContent);
    chatMessages.appendChild(loadingDiv);
    
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    return loadingDiv;
}

// Utility function to remove loading state
function removeLoading(loadingElement) {
    if (loadingElement && loadingElement.parentNode) {
        loadingElement.parentNode.removeChild(loadingElement);
    }
}

// Handle page visibility changes
document.addEventListener('visibilitychange', function() {
    if (document.hidden) {
        // Page is hidden - pause any ongoing animations or timers
        console.log('Page hidden');
    } else {
        // Page is visible again
        console.log('Page visible');
    }
});

// Handle window resize
window.addEventListener('resize', function() {
    // Recalculate any layout-dependent elements
    const chatMessages = document.getElementById('chatMessages');
    if (chatMessages) {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});

// Export functions for potential external use
window.TheraScape = {
    addMessageToChat,
    showTypingIndicator,
    hideTypingIndicator,
    updateMoodChart,
    showLoading,
    removeLoading
};

// Voice Chat Functionality
let currentChatMode = 'text'; // 'text' or 'voice'
let isRecording = false;
let speechRecognition = null;
let currentAudio = null;
let synth = window.speechSynthesis;

// Initialize voice chat functionality
function initializeVoiceChat() {
    const modeToggle = document.getElementById('chatModeToggle');
    const voiceControls = document.getElementById('voiceControls');
    const recordBtn = document.getElementById('recordBtn');
    
    if (!modeToggle || !voiceControls || !recordBtn) {
        console.warn('Voice chat elements not found');
        return;
    }
    
    // Mode toggle event listener
    modeToggle.addEventListener('change', function() {
        currentChatMode = this.checked ? 'voice' : 'text';
        toggleChatMode();
    });
    
    // Record button event listeners for better touch/click handling
    recordBtn.addEventListener('mousedown', startSpeechRecognition);
    recordBtn.addEventListener('touchstart', function(e) {
        e.preventDefault();
        startSpeechRecognition();
    });
    
    recordBtn.addEventListener('mouseup', stopSpeechRecognition);
    recordBtn.addEventListener('mouseleave', stopSpeechRecognition);
    recordBtn.addEventListener('touchend', stopSpeechRecognition);
    
    // Check for speech API support
    checkSpeechSupport();
}

function toggleChatMode() {
    const textInputArea = document.getElementById('textInputArea');
    const voiceInputArea = document.getElementById('voiceInputArea');
    const chatForm = document.getElementById('chatForm');
    
    if (currentChatMode === 'voice') {
        textInputArea.style.display = 'none';
        voiceInputArea.style.display = 'block';
        
        // Disable form submission for voice mode
        chatForm.style.pointerEvents = 'none';
        
        // Show voice mode indicator
        showVoiceModeIndicator();
    } else {
        textInputArea.style.display = 'block';
        voiceInputArea.style.display = 'none';
        
        // Re-enable form submission for text mode
        chatForm.style.pointerEvents = 'auto';
        
        // Hide voice mode indicator
        hideVoiceModeIndicator();
    }
}

function checkSpeechSupport() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const SpeechSynthesis = window.speechSynthesis;
    
    if (!SpeechRecognition) {
        showError('Your browser does not support speech recognition. Please use Chrome or Edge.');
        const modeToggle = document.getElementById('chatModeToggle');
        if (modeToggle) {
            modeToggle.disabled = true;
        }
        return false;
    }
    
    if (!SpeechSynthesis) {
        showError('Your browser does not support speech synthesis. Please use a modern browser.');
        return false;
    }
    
    return true;
}

function startSpeechRecognition() {
    if (!checkSpeechSupport()) return;
    
    try {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        speechRecognition = new SpeechRecognition();
        speechRecognition.lang = 'en-US';
        speechRecognition.continuous = false;
        speechRecognition.interimResults = false;
        
        // Request microphone permission before starting
        navigator.mediaDevices.getUserMedia({ audio: true })
            .then(stream => {
                // Stop tracks immediately, we just needed the permission
                stream.getTracks().forEach(track => track.stop());
                
                // Now start speech recognition
                speechRecognition.onstart = function() {
                    isRecording = true;
                    updateRecordButton();
                    showRecordingIndicator();
                    console.log('Speech recognition started');
                };
                
                speechRecognition.onresult = function(event) {
                    const transcript = event.results[0][0].transcript;
                    console.log('Recognized speech:', transcript);
                    processSpeechInput(transcript);
                };
                
                speechRecognition.onerror = function(event) {
                    console.error('Speech recognition error:', event.error);
                    showError(`Speech recognition error: ${event.error}`);
                    isRecording = false;
                    updateRecordButton();
                    hideRecordingIndicator();
                };
                
                speechRecognition.onend = function() {
                    isRecording = false;
        updateRecordButton();
                    hideRecordingIndicator();
                    console.log('Speech recognition ended');
                };
                
                speechRecognition.start();
            })
            .catch(err => {
                console.error('Microphone permission denied:', err);
                showError('Microphone permission denied. Please enable microphone access to use voice features.');
                isRecording = false;
                updateRecordButton();
            });
        
    } catch (error) {
        console.error('Error starting speech recognition:', error);
        showError('Could not access microphone. Please check your permissions and try again.');
    }
}

function stopSpeechRecognition() {
    if (speechRecognition && isRecording) {
        speechRecognition.stop();
    }
}

function updateRecordButton() {
    const recordBtn = document.getElementById('recordBtn');
    const recordText = recordBtn.querySelector('.record-text');
    const soundWaves = recordBtn.querySelector('.sound-waves');
    
    if (isRecording) {
        recordBtn.classList.add('recording');
        recordText.textContent = 'Release to Stop';
        
        // Show sound waves
        if (soundWaves) {
            soundWaves.style.opacity = '1';
        }
    } else {
        recordBtn.classList.remove('recording');
        recordText.textContent = 'Hold to Record';
        
        // Hide sound waves
        if (soundWaves) {
            soundWaves.style.opacity = '0';
        }
    }
}

async function processSpeechInput(transcript) {
    try {
        // Show processing indicator
        showVoiceProcessingIndicator();
        
        if (transcript) {
            // Add user message to chat
            addMessageToChat('user', transcript);
            userMessageCount++;
            
            // Periodic check-in every 6 user messages
            if (userMessageCount > 0 && userMessageCount % 6 === 0) {
                setTimeout(() => insertCheckInMessage(), 1200);
            }
            
            // Show typing indicator
            showTypingIndicator();
            updateRobotStatus("Processing your message...");
            
            // Get bot response
            await getBotResponseWithVoice(transcript);
        } else {
            throw new Error('No speech input detected');
        }
        
    } catch (error) {
        console.error('Error processing speech input:', error);
        showError('Sorry, I couldn\'t understand your voice input. Please try again.');
    } finally {
        hideVoiceProcessingIndicator();
    }
}

async function getBotResponseWithVoice(userMessage) {
    try {
        // Send message to chat endpoint (without voice_mode flag since we handle speech in browser now)
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                message: userMessage, 
                userName: userName
            })
        });
        
        const data = await response.json();
        hideTypingIndicator();
        
        if (data.success) {
            // Add bot message to chat
            addMessageToChat('bot', data.response, data.emotion);
            
            if (data.emotion) {
                updateMoodChart(data.emotion);
                updateRobotMood(data.emotion);
                // Update mood detection display
                updateMoodDisplay(data.emotion, Math.floor(80 + Math.random() * 20));
            }
            
            // Speech is now handled automatically in addMessageToChat for all bot responses
            
            // Trigger robot header talking animation
            triggerRobotHeaderTalking(data.response.length * 60);
            
        } else {
            addMessageToChat('bot', 'I apologize, but I\'m having trouble processing your message right now. Please try again in a moment.');
        }
        
    } catch (error) {
        console.error('Error getting bot response:', error);
        hideTypingIndicator();
        addMessageToChat('bot', 'I apologize, but I\'m experiencing technical difficulties. Please try again later.');
        updateRobotStatus("Ready to help you feel better");
    }
}

function speakResponse(text) {
    // Cancel any ongoing speech
    if (synth.speaking) {
        synth.cancel();
    }
    
    // Create utterance
    const utterance = new SpeechSynthesisUtterance(text);
    
    // Select a warm, comforting voice suitable for therapeutic animal companion
    if (availableVoices && availableVoices.length > 0) {
        // Log available voices to console for debugging
        console.log('Available voices:', availableVoices.map(v => v.name));
        
        // Priority list of preferred voices (based on common available voices across platforms)
        const preferredVoices = [
            // Google's natural-sounding voices
            'Google UK English Female', 
            'Google US English Female',
            
            // Microsoft's natural voices
            'Microsoft Zira',
            'Microsoft Hazel',
            'Microsoft Catherine',
            
            // Apple's natural voices
            'Samantha',
            'Ava',
            'Karen',
            
            // Other natural-sounding voices
            'Alex',
            'Moira',
            'Veena',
            'Fiona'
        ];
        
        // Try to find one of our preferred voices
        let selectedVoice = null;
        for (const voiceName of preferredVoices) {
            const voice = availableVoices.find(v => v.name === voiceName);
            if (voice) {
                selectedVoice = voice;
                break;
            }
        }
        
        // If no preferred voice found, try to find any female voice as backup
        if (!selectedVoice) {
            selectedVoice = availableVoices.find(voice => 
                voice.name.toLowerCase().includes('female') ||
                voice.name.includes('f') && !voice.name.toLowerCase().includes('male')
            );
        }
        
        // If still no voice found, use the first English voice
        if (!selectedVoice) {
            selectedVoice = availableVoices.find(voice => 
                voice.lang.startsWith('en')
            );
        }
        
        // Apply the selected voice
        if (selectedVoice) {
            utterance.voice = selectedVoice;
            console.log(`Using voice: ${selectedVoice.name} (${selectedVoice.lang})`);
        } else {
            console.log('No suitable voice found, using default voice');
        }
    } else {
        console.log('No voices available, using default voice');
    }
    
    // Add event listeners
    utterance.onstart = function() {
        console.log('Speech started');
    };
    
    utterance.onend = function() {
        console.log('Speech ended');
    };
    
    utterance.onerror = function(event) {
        console.error('Speech error:', event);
    };
    
    // Speak the text
    synth.speak(utterance);
}

// Voice UI indicator functions
function showVoiceModeIndicator() {
    const voiceModeIndicator = document.createElement('div');
    voiceModeIndicator.id = 'voiceModeIndicator';
    voiceModeIndicator.className = 'voice-mode-indicator';
    voiceModeIndicator.innerHTML = '<i class="fas fa-microphone"></i> Voice Mode Active';
    
    // Remove existing indicator if present
    const existingIndicator = document.getElementById('voiceModeIndicator');
    if (existingIndicator) {
        existingIndicator.remove();
    }
    
    // Add to the document
    document.body.appendChild(voiceModeIndicator);
    
    // Animate in
    setTimeout(() => {
        voiceModeIndicator.style.opacity = '1';
        voiceModeIndicator.style.transform = 'translateY(0)';
    }, 10);
}

function hideVoiceModeIndicator() {
    const indicator = document.getElementById('voiceModeIndicator');
    if (indicator) {
        indicator.style.opacity = '0';
        indicator.style.transform = 'translateY(20px)';
        setTimeout(() => {
        indicator.remove();
        }, 300);
    }
}

function showRecordingIndicator() {
    const recordingIndicator = document.getElementById('recordingIndicator') || document.createElement('div');
    recordingIndicator.id = 'recordingIndicator';
    recordingIndicator.className = 'recording-indicator';
    recordingIndicator.innerHTML = '<div class="pulse-ring"></div><span>Listening...</span>';
    
    if (!document.getElementById('recordingIndicator')) {
        document.body.appendChild(recordingIndicator);
    }
    
    // Animate in
    setTimeout(() => {
        recordingIndicator.style.opacity = '1';
        recordingIndicator.style.transform = 'translateY(0)';
    }, 10);
}

function hideRecordingIndicator() {
    const indicator = document.getElementById('recordingIndicator');
    if (indicator) {
        indicator.style.opacity = '0';
        indicator.style.transform = 'translateY(20px)';
        setTimeout(() => {
        indicator.remove();
        }, 300);
    }
}

function showVoiceProcessingIndicator() {
    const processingIndicator = document.getElementById('voiceProcessingIndicator') || document.createElement('div');
    processingIndicator.id = 'voiceProcessingIndicator';
    processingIndicator.className = 'voice-processing-indicator';
    processingIndicator.innerHTML = '<div class="spinner"></div><span>Processing voice...</span>';
    
    if (!document.getElementById('voiceProcessingIndicator')) {
        document.body.appendChild(processingIndicator);
    }
    
    // Animate in
    setTimeout(() => {
        processingIndicator.style.opacity = '1';
        processingIndicator.style.transform = 'translateY(0)';
    }, 10);
}

function hideVoiceProcessingIndicator() {
    const indicator = document.getElementById('voiceProcessingIndicator');
    if (indicator) {
        indicator.style.opacity = '0';
        indicator.style.transform = 'translateY(20px)';
        setTimeout(() => {
        indicator.remove();
        }, 300);
    }
}

// Error display function
function showError(message) {
    const errorToast = document.createElement('div');
    errorToast.className = 'error-toast';
    errorToast.textContent = message;
    
    document.body.appendChild(errorToast);
    
    // Animate in
        setTimeout(() => {
        errorToast.style.opacity = '1';
        errorToast.style.transform = 'translateY(0)';
    }, 10);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        errorToast.style.opacity = '0';
        errorToast.style.transform = 'translateY(-20px)';
        
        // Remove from DOM after animation completes
        setTimeout(() => {
            errorToast.remove();
        }, 300);
        }, 5000);
}

// Mood Detection Display Functions
let moodHistory = [];
let currentDetectedMood = null;

// Mood emoji mapping
const moodEmojis = {
    'Happy': '😊',
    'Sad': '😢',
    'Angry': '😠',
    'Anxious': '😰',
    'Stressed': '😤',
    'Neutral': '😐',
    'Depressed': '😔',
    'Excited': '🤗',
    'Calm': '😌'
};

// Mood colors mapping
const moodColors = {
    'Happy': '#4CAF50',
    'Sad': '#FF9800',
    'Angry': '#F44336',
    'Anxious': '#FFC107',
    'Stressed': '#FF5722',
    'Neutral': '#2196F3',
    'Depressed': '#9C27B0',
    'Excited': '#E91E63',
    'Calm': '#00BCD4'
};

function updateMoodDisplay(emotion, confidence = 85) {
    if (!emotion) return;
    
    // Update current mood display
    const moodIcon = document.getElementById('currentMoodIcon');
    const moodName = document.getElementById('currentMoodName');
    const moodConfidenceElement = document.getElementById('moodConfidence');
    
    if (moodIcon) {
        moodIcon.textContent = moodEmojis[emotion] || '🤔';
        moodIcon.className = 'mood-icon-large';
        
        // Add animation
        moodIcon.classList.add('analyzing');
        setTimeout(() => {
            moodIcon.classList.remove('analyzing');
        }, 2000);
    }
    
    if (moodName) {
        moodName.textContent = emotion;
        moodName.style.color = moodColors[emotion] || '#fff';
    }
    
    if (moodConfidenceElement) {
        moodConfidenceElement.textContent = `Confidence: ${confidence}%`;
    }
    
    // Add to mood history
    addToMoodHistory(emotion);
    
    // Update current detected mood
    currentDetectedMood = emotion;
}

function addToMoodHistory(emotion) {
    const timestamp = new Date();
    const moodEntry = {
        emotion: emotion,
        time: timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        timestamp: timestamp
    };
    
    // Add to history (keep last 5 entries)
    moodHistory.unshift(moodEntry);
    if (moodHistory.length > 5) {
        moodHistory = moodHistory.slice(0, 5);
    }
    
    // Update timeline display
    updateMoodTimeline();
}

function updateMoodTimeline() {
    const timeline = document.getElementById('moodTimeline');
    if (!timeline) return;
    
    timeline.innerHTML = '';
    
    moodHistory.forEach((entry, index) => {
        const timelineItem = document.createElement('div');
        timelineItem.className = `mood-timeline-item ${entry.emotion.toLowerCase()}`;
        
        const emoji = document.createElement('div');
        emoji.className = 'mood-timeline-emoji';
        emoji.textContent = moodEmojis[entry.emotion] || '🤔';
        
        const info = document.createElement('div');
        info.className = 'mood-timeline-info';
        
        const name = document.createElement('div');
        name.className = 'mood-timeline-name';
        name.textContent = entry.emotion;
        
        const time = document.createElement('div');
        time.className = 'mood-timeline-time';
        time.textContent = entry.time;
        
        info.appendChild(name);
        info.appendChild(time);
        
        timelineItem.appendChild(emoji);
        timelineItem.appendChild(info);
        
        timeline.appendChild(timelineItem);
        
        // Add animation
        setTimeout(() => {
            timelineItem.style.animation = 'fadeInLeft 0.5s ease-out';
        }, index * 100);
    });
}

function showMoodAnalyzing() {
    const moodIcon = document.getElementById('currentMoodIcon');
    const moodName = document.getElementById('currentMoodName');
    const moodConfidenceElement = document.getElementById('moodConfidence');
    
    if (moodIcon) {
        moodIcon.textContent = '🤔';
        moodIcon.className = 'mood-icon-large analyzing';
    }
    
    if (moodName) {
        moodName.textContent = 'Analyzing...';
        moodName.style.color = '#fff';
    }
    
    if (moodConfidenceElement) {
        moodConfidenceElement.textContent = 'Confidence: --';
    }
}

// Initialize mood display
function initializeMoodDisplay() {
    // Set initial state
    showMoodAnalyzing();
    
    // Add some sample mood history for demonstration
    if (moodHistory.length === 0) {
        // Add a neutral starting mood
        setTimeout(() => {
            updateMoodDisplay('Neutral', 75);
        }, 1000);
    }
}

// Java Backend Integration for Mood Analysis
async function analyzeMoodWithJavaBackend(messageText) {
    try {
        // Check if user is authenticated
        const authToken = localStorage.getItem('authToken');
        if (!authToken) {
            console.log('User not authenticated, skipping Java backend mood analysis');
            return;
        }

        // Send mood analysis request to Java backend
        const response = await fetch('http://localhost:8080/api/mood/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify({
                text: messageText,
                intensity: Math.floor(Math.random() * 10) + 1, // Random intensity for now
                preferences: {
                    includeRecommendations: true,
                    includeTherapeuticGoals: true
                }
            })
        });

        if (response.ok) {
            const moodData = await response.json();
            console.log('Java backend mood analysis:', moodData);
            
            // Update mood display with Java backend results
            if (moodData.primaryMood) {
                updateMoodDisplay(moodData.primaryMood, Math.round(moodData.confidenceScore * 100));
            }
            
            // Show therapeutic recommendations if available
            if (moodData.therapeuticGoals && moodData.therapeuticGoals.length > 0) {
                showTherapeuticGoals(moodData.therapeuticGoals);
            }
            
            // Show video recommendations if available
            if (moodData.recommendedVideos && moodData.recommendedVideos.length > 0) {
                showVideoRecommendations(moodData.recommendedVideos);
            }
            
            // Check for crisis risk
            if (moodData.crisisRisk) {
                showCrisisSupport();
            }
        } else if (response.status === 401) {
            console.log('Authentication token expired, redirecting to login');
            localStorage.removeItem('authToken');
            // Could redirect to auth page if needed
        } else {
            console.log('Failed to analyze mood with Java backend:', response.status);
        }
    } catch (error) {
        console.error('Error analyzing mood with Java backend:', error);
    }
}

// Show therapeutic goals in the sidebar
function showTherapeuticGoals(goals) {
    console.log('Showing therapeutic goals:', goals);
    
    // You could update a sidebar section or show a modal with goals
    const goalsList = document.getElementById('therapeuticGoals');
    if (goalsList) {
        goalsList.innerHTML = goals.map(goal => `
            <div class="goal-item">
                <span class="material-icons">flag</span>
                <span>${goal}</span>
            </div>
        `).join('');
    }
}

// Show video recommendations
function showVideoRecommendations(videos) {
    console.log('Showing video recommendations:', videos);
    
    // Add a subtle notification about video recommendations
    const chatMessages = document.getElementById('chatMessages');
    if (chatMessages && videos.length > 0) {
        const recommendationDiv = document.createElement('div');
        recommendationDiv.className = 'recommendation-notice';
        recommendationDiv.innerHTML = `
            <div class="recommendation-content">
                <span class="material-icons">video_library</span>
                <span>I found ${videos.length} helpful video${videos.length > 1 ? 's' : ''} for you. 
                <a href="/videos" target="_blank">View recommendations</a></span>
            </div>
        `;
        chatMessages.appendChild(recommendationDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
}

// Show crisis support
function showCrisisSupport() {
    console.log('Crisis risk detected, showing support options');
    
    const chatMessages = document.getElementById('chatMessages');
    if (chatMessages) {
        const crisisDiv = document.createElement('div');
        crisisDiv.className = 'crisis-support-notice';
        crisisDiv.innerHTML = `
            <div class="crisis-content">
                <span class="material-icons">warning</span>
                <div class="crisis-text">
                    <strong>I'm concerned about you.</strong>
                    <p>If you're having thoughts of self-harm, please reach out for support:</p>
                    <p>🔗 <a href="/crisis" target="_blank">Crisis support resources</a></p>
                    <p>📞 National Suicide Prevention Lifeline: 988</p>
                </div>
            </div>
        `;
        chatMessages.appendChild(crisisDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
}

// Initialize logout button functionality
function initializeLogoutButton() {
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', async function(e) {
            e.preventDefault();
            
            // Show confirmation for authenticated users
            if (window.userContext && window.userContext.mode !== 'demo') {
                const confirmed = confirm('Are you sure you want to logout? Your session will be saved.');
                if (!confirmed) return;
            }
            
            // Show loading state
            const originalContent = logoutBtn.innerHTML;
            logoutBtn.innerHTML = '<span class="material-icons">hourglass_empty</span>Logging out...';
            logoutBtn.disabled = true;
            
            try {
                // Call logout API
                const response = await fetch('/api/logout', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });
                
                const data = await response.json();
                
                if (data.success) {
                    // Clear local storage
                    sessionStorage.clear();
                    localStorage.removeItem('therascapeUserName');
                    
                    // Redirect to landing page
                    window.location.href = '/';
                } else {
                    alert('Logout failed: ' + data.message);
                    // Restore button state
                    logoutBtn.innerHTML = originalContent;
                    logoutBtn.disabled = false;
                }
            } catch (error) {
                console.error('Logout error:', error);
                alert('Logout failed. Please try again.');
                // Restore button state
                logoutBtn.innerHTML = originalContent;
                logoutBtn.disabled = false;
            }
        });
    }
}