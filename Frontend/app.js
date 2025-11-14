/* === SCROLLREVEAL ANIMATIONS === */

// Initialize ScrollReveal with some default settings
const sr = ScrollReveal({
    origin: 'top',      // Animate from the top
    distance: '60px',   // Distance element moves
    duration: 1500,     // Animation duration in ms
    delay: 200,         // Delay before animation starts
    reset: false        // Animations only play once
});

/* --- Header / Navbar --- */
// Animate header elements one by one
sr.reveal('.logo', { delay: 100, origin: 'left' });
sr.reveal('.nav-links', { delay: 200, origin: 'bottom' });
sr.reveal('.nav-right', { delay: 300, origin: 'right' });

/* --- Hero Section --- */
// Animate hero content from different directions
sr.reveal('.hero-content h1', { origin: 'left', delay: 400 });
sr.reveal('.hero-content p', { origin: 'right', delay: 500 });
sr.reveal('.hero-buttons', { origin: 'bottom', delay: 600 });

/* --- Features Section --- */
// Animate the feature cards one by one (staggered)
sr.reveal('.feature-card', {
    origin: 'bottom',
    interval: 200 // Each card appears 200ms after the previous one
});

/* --- Featured Events Section --- */
// Animate the section titles
sr.reveal('.events h2', { origin: 'top' });
sr.reveal('.events .subheading', { origin: 'top', delay: 300 });

// Animate the event cards one by one (staggered)
sr.reveal('.event-card', {
    origin: 'bottom',
    interval: 200
});

/* --- View All Events Section --- */
sr.reveal('.btn-view-all', { origin: 'bottom' });

/* --- Footer Section --- */
// Animate the footer columns
sr.reveal('.footer-brand', { origin: 'left', distance: '30px' });
sr.reveal('.footer-links', { origin: 'bottom', distance: '30px', delay: 300 });
sr.reveal('.footer-social', { origin: 'right', distance: '30px', delay: 500 });
sr.reveal('.footer-bottom', { origin: 'bottom', delay: 800 });

/* === AI SUGGESTION MODAL === */

// 1. Get all the new elements
const aiButton = document.querySelector('.btn-secondary'); // Your "AI Suggestion Events" button
const aiModal = document.getElementById('ai-modal');
const closeAiModalBtn = document.getElementById('close-ai-modal');
const aiContent = document.getElementById('ai-suggestion-content');

// 2. Create functions to open and close the modal
function openAiModal() {
    aiModal.classList.add('visible');
}

function closeAiModal() {
    aiModal.classList.remove('visible');
}

// 3. Create the function to call your Python backend
async function getAiSuggestions() {
    console.log("Button clicked! Getting AI suggestions...");
    
    // Show the modal and the loading spinner
    aiContent.innerHTML = '<div class="loader"></div>';
    openAiModal();

    try {
        // This calls your local Python server
        const response = await fetch('http://127.0.0.1:5000/get-suggestions');
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Format the AI's text (it has newlines) to HTML (with <br> tags)
        const formattedText = data.suggestion.replace(/\n/g, '<br>');
        
        // Put the suggestions in the modal
        aiContent.innerHTML = formattedText;

    } catch (error) {
        console.error("Could not fetch AI suggestions:", error);
        aiContent.innerHTML = "<strong>Error:</strong> Could not connect to the AI server. <br/> (Did you remember to run `python server.py`?)";
    }
}

// 4. Connect the button click to the function
aiButton.addEventListener('click', (e) => {
    e.preventDefault(); // Stop the link from trying to go anywhere
    getAiSuggestions();
});

// 5. Connect the close button
closeAiModalBtn.addEventListener('click', closeAiModal);
aiModal.addEventListener('click', (e) => {
    if (e.target === aiModal) {
        closeAiModal();
    }
});