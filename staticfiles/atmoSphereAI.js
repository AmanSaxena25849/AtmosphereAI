const input = document.querySelector('.message-input');
const button = document.querySelector('.send-button');

button.addEventListener('click', () => {
  if (input.value.length < 3) {
    input.style.animation= "shake 0.5s";
    input.style.border= "2px solid red";
    setTimeout(() => {
        input.style.animation= "unset";
        input.style.border= "none";
    }, 600);
    input.focus();
    return false; 
  }
  setTimeout(() => {
    input.value = '';
    input.style.opacity = '1';
  }, 10);
});





document.addEventListener('DOMContentLoaded', function() {
  const aboutButton = document.querySelector('.about-button');
  const aboutContainer = document.querySelector('.about-container');
  const closeAbout = document.querySelector('.close-about');
  
  // Initially hide the about section
  aboutContainer.style.display = 'none';
  
  aboutButton.addEventListener('click', function() {
      aboutContainer.style.display = 'block';
  });
  
  closeAbout.addEventListener('click', function() {
      aboutContainer.style.display = 'none';
  });
});

document.addEventListener('DOMContentLoaded', function() {
  const aboutButton = document.querySelector('.about-button');
  const aboutContainer = document.querySelector('.about-container');
  const closeAbout = document.querySelector('.close-about');
  
  // Initially hide the about section
  aboutContainer.style.display = 'none';
  
  aboutButton.addEventListener('click', function() {
      // First make the about container visible
      aboutContainer.style.display = 'block';
      
      // Wait a moment for the display change to take effect
      setTimeout(() => {
          // Then scroll to the about section smoothly
          aboutContainer.scrollIntoView({ 
              behavior: 'smooth',
              block: 'start'
          });
      }, 100);
  });
  
  closeAbout.addEventListener('click', function() {
      // Scroll back to top before hiding
      window.scrollTo({
          top: 0,
          behavior: 'smooth'
      });
      
      // After scrolling up, hide the about section
      setTimeout(() => {
          aboutContainer.style.display = 'none';
      }, 500);
  });
});