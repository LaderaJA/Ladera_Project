// home
  document.addEventListener("DOMContentLoaded", function() {
        const fadeText = document.getElementById('fadeText');

        setTimeout(function() {
            fadeText.classList.add('visible');
        }, 500);
    });



// about
 var words = [
  "I'm John Albert Ladera",
  "I'm a Student in CVSU",
  "I'm a BSIT Student",
  "I'm in Third Year"
];

var index = 0;
var typewriterText = "Initial text to be replaced";
var charIndex = 0;
var wordToChangeElement = document.getElementById("wordToChange");

function typeWriterEffect() {
  if (charIndex < typewriterText.length) {
    wordToChangeElement.textContent += typewriterText.charAt(charIndex);
    charIndex++;
    setTimeout(typeWriterEffect, 150);
  }
}

function changeWord() {
  charIndex = 0;
  wordToChangeElement.textContent = "";
  typewriterText = words[index];
  index = (index + 1) % words.length;
  typeWriterEffect();
}

setInterval(changeWord, 5000);
