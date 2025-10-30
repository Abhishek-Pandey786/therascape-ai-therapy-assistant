document.addEventListener('DOMContentLoaded', function() {
    // Set up event listeners for all breathing animation start buttons
    const startButtons = document.querySelectorAll('.start-animation');
    startButtons.forEach(button => {
        button.addEventListener('click', function() {
            const targetId = this.getAttribute('data-target');
            startBreathingAnimation(targetId);
        });
    });

    // 4-7-8 Breathing Animation
    function start478Animation() {
        const circle = document.querySelector('#animation478 .circle');
        const instruction = document.querySelector('#animation478 .breathing-instruction');
        const button = document.querySelector('#animation478 .start-animation');
        
        // Hide button during animation
        button.style.display = 'none';
        
        // Animation sequence
        // Inhale for 4 seconds
        instruction.textContent = 'Inhale through nose';
        circle.classList.add('inhale');
        
        setTimeout(() => {
            // Hold for 7 seconds
            instruction.textContent = 'Hold breath';
            circle.classList.remove('inhale');
            circle.classList.add('hold');
            
            setTimeout(() => {
                // Exhale for 8 seconds
                instruction.textContent = 'Exhale through mouth';
                circle.classList.remove('hold');
                circle.classList.add('exhale');
                
                setTimeout(() => {
                    // Reset
                    circle.classList.remove('exhale');
                    instruction.textContent = 'Click to start again';
                    button.style.display = 'block';
                }, 8000); // 8 seconds exhale
            }, 7000); // 7 seconds hold
        }, 4000); // 4 seconds inhale
    }

    // Box Breathing Animation
    function startBoxAnimation() {
        const box = document.querySelector('#animationBox .box');
        const instruction = document.querySelector('#animationBox .breathing-instruction');
        const button = document.querySelector('#animationBox .start-animation');
        
        // Hide button during animation
        button.style.display = 'none';
        
        // Animation sequence
        // Inhale for 4 seconds
        instruction.textContent = 'Inhale';
        box.classList.add('box-inhale');
        
        setTimeout(() => {
            // Hold for 4 seconds
            instruction.textContent = 'Hold';
            box.classList.remove('box-inhale');
            box.classList.add('box-hold-full');
            
            setTimeout(() => {
                // Exhale for 4 seconds
                instruction.textContent = 'Exhale';
                box.classList.remove('box-hold-full');
                box.classList.add('box-exhale');
                
                setTimeout(() => {
                    // Hold empty for 4 seconds
                    instruction.textContent = 'Hold';
                    box.classList.remove('box-exhale');
                    box.classList.add('box-hold-empty');
                    
                    setTimeout(() => {
                        // Reset
                        box.classList.remove('box-hold-empty');
                        instruction.textContent = 'Click to start again';
                        button.style.display = 'block';
                    }, 4000); // 4 seconds hold empty
                }, 4000); // 4 seconds exhale
            }, 4000); // 4 seconds hold full
        }, 4000); // 4 seconds inhale
    }

    // Function to start the appropriate animation based on the target ID
    function startBreathingAnimation(targetId) {
        switch(targetId) {
            case 'animation478':
                start478Animation();
                break;
            case 'animationBox':
                startBoxAnimation();
                break;
            default:
                console.log('Animation not found for target:', targetId);
        }
    }
}); 