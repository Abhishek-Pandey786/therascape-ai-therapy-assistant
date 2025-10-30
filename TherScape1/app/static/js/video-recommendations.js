// Video Recommendation Functions for TheraScape
// Enhanced video display and interaction system

// Global video state
let currentVideoRecommendations = [];
let videoModal = null;

// Initialize video system when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeVideoSystem();
});

function initializeVideoSystem() {
    // Get video modal elements
    videoModal = document.getElementById('videoModal');
    const videoModalClose = document.getElementById('videoModalClose');
    
    // Close modal events
    if (videoModalClose) {
        videoModalClose.addEventListener('click', closeVideoModal);
    }
    
    if (videoModal) {
        videoModal.addEventListener('click', function(e) {
            if (e.target === videoModal) {
                closeVideoModal();
            }
        });
    }
    
    // Keyboard escape to close modal
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && videoModal && videoModal.style.display === 'flex') {
            closeVideoModal();
        }
    });
    
    console.log('Video system initialized');
}

// Enhanced addMessageToChat function to include video recommendations
function addMessageToChatWithVideos(sender, message, emotion = null, videos = []) {
    const chatMessages = document.getElementById('chatMessages');
    if (!chatMessages) return;

    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    
    // Create message wrapper for bot messages (to include avatar)
    if (sender === 'bot') {
        const messageWrapper = document.createElement('div');
        messageWrapper.className = 'bot-message-wrapper';
        
        // Add robot avatar
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

    // Add video recommendations if available
    if (videos && videos.length > 0 && sender === 'bot') {
        const videoRecommendations = createVideoRecommendationsElement(videos);
        messageContent.appendChild(videoRecommendations);
        
        // Update sidebar with videos
        updateSidebarVideoRecommendations(videos);
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
                triggerRobotTalking(avatarElement, message.length * 50);
            }, 300);
        }
        
        // Speak bot responses
        setTimeout(() => {
            speakResponse(message);
        }, 500);
    }

    messageDiv.style.animation = 'fadeInUp 0.3s ease-out';
}

// Create video recommendations element
function createVideoRecommendationsElement(videos) {
    const container = document.createElement('div');
    container.className = 'video-recommendations';
    
    // Header
    const header = document.createElement('div');
    header.className = 'video-recommendations-header';
    header.innerHTML = `
        <span class="material-icons">video_library</span>
        <span>Recommended Videos for You</span>
    `;
    container.appendChild(header);
    
    // Video cards
    videos.forEach(video => {
        const videoCard = createVideoCard(video);
        container.appendChild(videoCard);
    });
    
    return container;
}

// Create individual video card
function createVideoCard(video) {
    const card = document.createElement('div');
    card.className = 'video-card';
    
    // Add special classes based on video properties
    if (video.crisisSafe) {
        card.classList.add('crisis-safe');
    }
    if (video.duration <= 10) {
        card.classList.add('quick-help');
    }
    if (video.difficultyLevel === 'beginner') {
        card.classList.add('beginner');
    }
    
    card.innerHTML = `
        <div class="video-card-content">
            <div class="video-thumbnail">
                <img src="${video.thumbnailUrl || generateThumbnailUrl(video.videoUrl)}" 
                     alt="${video.title}" 
                     onerror="this.parentElement.innerHTML='<span class=\\"material-icons\\">play_circle</span>'">
                <div class="play-icon">
                    <span class="material-icons">play_arrow</span>
                </div>
            </div>
            <div class="video-info">
                <div class="video-title">${video.title}</div>
                <div class="video-description">${video.description || 'Therapeutic video content'}</div>
                <div class="video-meta">
                    <span class="video-duration">${video.duration}min</span>
                    ${video.primaryMoodCategory ? `<span class="video-tag">${video.primaryMoodCategory}</span>` : ''}
                    ${video.therapyTechnique ? `<span class="video-tag">${formatTherapyTechnique(video.therapyTechnique)}</span>` : ''}
                    ${video.averageRating ? `
                        <div class="video-rating">
                            <span class="star">★</span>
                            <span>${video.averageRating.toFixed(1)}</span>
                        </div>
                    ` : ''}
                </div>
            </div>
        </div>
    `;
    
    // Add click event to open video
    card.addEventListener('click', () => {
        openVideoModal(video);
        recordVideoInteraction(video.id, 'view');
    });
    
    return card;
}

// Update sidebar video recommendations
function updateSidebarVideoRecommendations(videos) {
    const sidebarPanel = document.getElementById('sidebarVideoPanel');
    const sidebarList = document.getElementById('sidebarVideoList');
    
    if (!sidebarPanel || !sidebarList) return;
    
    // Clear existing videos
    sidebarList.innerHTML = '';
    
    // Show panel
    sidebarPanel.style.display = 'block';
    
    // Add top 3 videos to sidebar
    const sidebarVideos = videos.slice(0, 3);
    
    sidebarVideos.forEach(video => {
        const item = document.createElement('div');
        item.className = 'sidebar-video-item';
        
        item.innerHTML = `
            <div class="sidebar-video-thumb">
                <span class="material-icons">play_arrow</span>
            </div>
            <div class="sidebar-video-details">
                <div class="sidebar-video-title">${video.title}</div>
                <div class="sidebar-video-duration">${video.duration}min • ${video.primaryMoodCategory || 'General'}</div>
            </div>
        `;
        
        // Add click event
        item.addEventListener('click', () => {
            openVideoModal(video);
            recordVideoInteraction(video.id, 'view');
        });
        
        sidebarList.appendChild(item);
    });
}

// Open video in modal
function openVideoModal(video) {
    if (!videoModal) return;
    
    const title = document.getElementById('videoModalTitle');
    const iframe = document.getElementById('videoModalIframe');
    const description = document.getElementById('videoModalDescription');
    const tagsContainer = document.getElementById('videoModalTags');
    const featuresList = document.getElementById('videoModalFeaturesList');
    
    // Set content
    if (title) title.textContent = video.title;
    if (description) description.textContent = video.description || 'No description available';
    
    // Set video URL (convert to embed URL if needed)
    if (iframe) {
        const embedUrl = convertToEmbedUrl(video.videoUrl);
        iframe.src = embedUrl;
    }
    
    // Set tags
    if (tagsContainer) {
        tagsContainer.innerHTML = '';
        const tags = [
            video.primaryMoodCategory,
            video.therapyTechnique,
            video.contentType,
            video.difficultyLevel
        ].filter(Boolean);
        
        tags.forEach(tag => {
            const tagElement = document.createElement('span');
            tagElement.className = 'video-modal-tag';
            tagElement.textContent = formatTherapyTechnique(tag);
            tagsContainer.appendChild(tagElement);
        });
    }
    
    // Set interactive features
    if (featuresList) {
        featuresList.innerHTML = '';
        const features = video.interactiveFeatures || ['Video content', 'Pause and reflect', 'Follow along'];
        
        features.forEach(feature => {
            const li = document.createElement('li');
            li.textContent = feature;
            featuresList.appendChild(li);
        });
    }
    
    // Show modal
    videoModal.style.display = 'flex';
    
    // Track interaction
    recordVideoInteraction(video.id, 'open_modal');
}

// Close video modal
function closeVideoModal() {
    if (!videoModal) return;
    
    videoModal.style.display = 'none';
    
    // Stop video playback
    const iframe = document.getElementById('videoModalIframe');
    if (iframe) {
        iframe.src = '';
    }
}

// Convert YouTube URL to embed URL
function convertToEmbedUrl(url) {
    if (!url) return '';
    
    // YouTube URL patterns
    const youtubeRegex = /(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})/;
    const match = url.match(youtubeRegex);
    
    if (match) {
        return `https://www.youtube.com/embed/${match[1]}?rel=0&modestbranding=1`;
    }
    
    // If it's already an embed URL or other format, return as is
    return url;
}

// Generate thumbnail URL for videos
function generateThumbnailUrl(videoUrl) {
    if (!videoUrl) return '/static/images/default-video-thumbnail.jpg';
    
    const youtubeRegex = /(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})/;
    const match = videoUrl.match(youtubeRegex);
    
    if (match) {
        return `https://img.youtube.com/vi/${match[1]}/maxresdefault.jpg`;
    }
    
    return '/static/images/default-video-thumbnail.jpg';
}

// Format therapy technique for display
function formatTherapyTechnique(technique) {
    if (!technique) return '';
    
    return technique
        .replace(/_/g, ' ')
        .split(' ')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
        .join(' ');
}

// Record video interaction for analytics
function recordVideoInteraction(videoId, interactionType) {
    if (!videoId || !window.userContext?.name) return;
    
    fetch('/api/video-interaction', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            videoId: videoId,
            username: window.userContext.name,
            interactionType: interactionType
        })
    }).catch(error => {
        console.log('Video interaction tracking failed:', error);
    });
}

// Add video recommendations to chat response
function addVideoRecommendationsToResponse(response, videos) {
    if (!videos || videos.length === 0) return response;
    
    let videoText = '\n\n🎬 I found some videos that might help:';
    videos.slice(0, 3).forEach((video, index) => {
        videoText += `\n${index + 1}. ${video.title} (${video.duration}min)`;
    });
    
    return response + videoText;
}

// Helper function to check if videos are available in response
function hasVideoRecommendations(responseData) {
    return responseData && responseData.videos && responseData.videos.length > 0;
}

// Update the existing addMessageToChat function to support videos
if (typeof window.addMessageToChat === 'function') {
    const originalAddMessageToChat = window.addMessageToChat;
    window.addMessageToChat = function(sender, message, emotion = null, videos = null) {
        if (videos && videos.length > 0) {
            addMessageToChatWithVideos(sender, message, emotion, videos);
        } else {
            originalAddMessageToChat(sender, message, emotion);
        }
    };
} else {
    // If addMessageToChat doesn't exist, create it
    window.addMessageToChat = function(sender, message, emotion = null, videos = null) {
        if (videos && videos.length > 0) {
            addMessageToChatWithVideos(sender, message, emotion, videos);
        } else {
            // Fallback basic message display
            console.log(`${sender}: ${message}`);
        }
    };
}
