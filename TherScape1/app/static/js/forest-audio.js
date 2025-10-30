/**
 * Forest Audio Player for TheraScape
 * Provides ambient forest sounds for enhanced therapeutic experience
 */

class ForestAudioPlayer {
    constructor() {
        this.audio = null;
        this.isPlaying = false;
        this.volume = 0.5;
        this.toggleButton = null;
        this.volumeSlider = null;
        this.statusElement = null;
        this.soundWaves = null;
        
        this.init();
    }

    init() {
        this.createAudioElement();
        this.createUI();
        this.attachEventListeners();
        this.showStatus('Forest sounds ready', 2000);
    }

    createAudioElement() {
        this.audio = new Audio();
        // Use local forest sounds MP3 file
        this.audio.src = '/static/audio/forest-sounds.mp3';
        this.audio.loop = true;
        this.audio.volume = this.volume;
        this.audio.preload = 'metadata';
        this.audio.crossOrigin = 'anonymous';
        
        this.audio.addEventListener('loadstart', () => {
            this.showStatus('Loading forest sounds...', 1500);
        });
        
        this.audio.addEventListener('canplaythrough', () => {
            this.showStatus('Forest sounds ready', 2000);
        });
        
        this.audio.addEventListener('ended', () => {
            // This shouldn't happen with loop=true, but just in case
            if (this.isPlaying) {
                this.audio.play();
            }
        });
        
        this.audio.addEventListener('error', (e) => {
            console.error('Audio loading error:', e);
            this.showStatus('Forest sounds unavailable', 3000);
            
            // Provide helpful error message
            const errorMessages = {
                1: 'Audio loading was aborted',
                2: 'Network error occurred',
                3: 'Audio decoding failed',
                4: 'Audio format not supported'
            };
            
            const errorCode = this.audio.error ? this.audio.error.code : 0;
            console.log('Audio error details:', errorMessages[errorCode] || 'Unknown error');
        });
        
        this.audio.addEventListener('pause', () => {
            if (this.isPlaying) {
                // Audio was paused externally, update UI
                this.pause();
            }
        });
    }

    createUI() {
        // Create main container
        const container = document.createElement('div');
        container.className = 'forest-audio-container';
        container.innerHTML = `
            <div class="forest-audio-controls">
                <span class="forest-audio-label">Forest Sounds</span>
                <input type="range" class="forest-audio-volume" min="0" max="1" step="0.1" value="${this.volume}">
                <div class="sound-waves" style="display: none;">
                    <div class="sound-wave"></div>
                    <div class="sound-wave"></div>
                    <div class="sound-wave"></div>
                    <div class="sound-wave"></div>
                    <div class="sound-wave"></div>
                </div>
            </div>
            <button class="forest-audio-toggle" title="Toggle Forest Sounds">
                <i class="fas fa-tree forest-audio-icon"></i>
            </button>
            <div class="forest-audio-status"></div>
        `;
        
        document.body.appendChild(container);
        
        // Get references
        this.toggleButton = container.querySelector('.forest-audio-toggle');
        this.volumeSlider = container.querySelector('.forest-audio-volume');
        this.statusElement = container.querySelector('.forest-audio-status');
        this.soundWaves = container.querySelector('.sound-waves');
        this.container = container;
    }

    attachEventListeners() {
        // Toggle button
        this.toggleButton.addEventListener('click', () => {
            this.toggle();
        });

        // Volume slider
        this.volumeSlider.addEventListener('input', (e) => {
            this.setVolume(parseFloat(e.target.value));
        });

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.key === 'm') {
                e.preventDefault();
                this.toggle();
            }
        });

        // Auto-hide controls
        this.container.addEventListener('mouseleave', () => {
            setTimeout(() => {
                this.container.classList.remove('show-controls');
            }, 1000);
        });
    }

    toggle() {
        if (this.isPlaying) {
            this.pause();
        } else {
            this.play();
        }
    }

    play() {
        if (!this.audio) {
            this.showStatus('Audio not initialized', 2000);
            return;
        }

        // Play the forest sounds audio
        const playPromise = this.audio.play();
        
        if (playPromise !== undefined) {
            playPromise
                .then(() => {
                    // Audio started successfully
                    this.isPlaying = true;
                    this.updateUIForPlaying();
                    this.showStatus('Forest sounds playing', 2000);
                })
                .catch((error) => {
                    console.error('Error playing audio:', error);
                    
                    // Handle autoplay policy restrictions
                    if (error.name === 'NotAllowedError') {
                        this.showStatus('Click to enable forest sounds', 3000);
                    } else {
                        this.showStatus('Cannot play forest sounds', 3000);
                    }
                    
                    this.isPlaying = false;
                });
        } else {
            // Fallback for older browsers
            this.isPlaying = true;
            this.updateUIForPlaying();
            this.showStatus('Forest sounds playing', 2000);
        }
    }

    updateUIForPlaying() {
        this.toggleButton.classList.add('playing');
        this.toggleButton.querySelector('.forest-audio-icon').classList.remove('fa-tree');
        this.toggleButton.querySelector('.forest-audio-icon').classList.add('fa-volume-up');
        this.soundWaves.style.display = 'flex';
        this.toggleButton.setAttribute('title', 'Pause Forest Sounds');
    }

    pause() {
        if (this.audio) {
            this.audio.pause();
        }
        
        this.isPlaying = false;
        this.updateUIForPaused();
        this.showStatus('Forest sounds paused', 2000);
    }

    updateUIForPaused() {
        this.toggleButton.classList.remove('playing');
        this.toggleButton.querySelector('.forest-audio-icon').classList.remove('fa-volume-up');
        this.toggleButton.querySelector('.forest-audio-icon').classList.add('fa-tree');
        this.soundWaves.style.display = 'none';
        this.toggleButton.setAttribute('title', 'Play Forest Sounds');
    }

    setVolume(volume) {
        this.volume = Math.max(0, Math.min(1, volume));
        if (this.audio) {
            this.audio.volume = this.volume;
        }
        this.volumeSlider.value = this.volume;
        
        const volumePercent = Math.round(this.volume * 100);
        this.showStatus(`Volume: ${volumePercent}%`, 1500);
    }

    showStatus(message, duration = 2000) {
        this.statusElement.textContent = message;
        this.statusElement.classList.add('show');
        
        setTimeout(() => {
            this.statusElement.classList.remove('show');
        }, duration);
    }

    // Additional helper methods
    getCurrentTime() {
        return this.audio ? this.audio.currentTime : 0;
    }

    getDuration() {
        return this.audio ? this.audio.duration : 0;
    }

    isAudioLoaded() {
        return this.audio && this.audio.readyState >= 2; // HAVE_CURRENT_DATA
    }

    // Error handling for audio loading
    handleAudioError() {
        this.showStatus('Error loading forest sounds', 3000);
        this.isPlaying = false;
        this.updateUIForPaused();
    }
}

// Initialize the forest audio player when the page loads
document.addEventListener('DOMContentLoaded', () => {
    // Wait a bit to ensure other elements are loaded
    setTimeout(() => {
        window.forestAudioPlayer = new ForestAudioPlayer();
    }, 1000);
});

// Export for potential external use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ForestAudioPlayer;
}
