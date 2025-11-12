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