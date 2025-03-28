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