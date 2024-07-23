let flashcardsString = document.currentScript.getAttribute('data-cards');
let apiUrl = document.currentScript.getAttribute('data-url');
let stackId = document.currentScript.getAttribute('data-stack-id');
let flashcards = JSON.parse(flashcardsString);
let unknownCards = flashcards.filter(item => !item.known);
let index = 0;
let flipped = false;
let knownCounter = 0;
let unknownCounter = 0;
let articleElement = document.getElementById('article');
let textElement = document.getElementById('text');
let indexSpan = document.getElementById('indexSpan');
let totalSpan = document.getElementById('totalSpan');
let markKnowElement = document.getElementById('numberOfKnown');
let markUnknowElement = document.getElementById('numberOfUnknown');
let knowButton = document.getElementById('knowButton');
let learningButton = document.getElementById('learningButton');
let flipButton = document.getElementById('flipButton');
let previousButton = document.getElementById('previousButton');
let resetButton = document.getElementById('resetButton');

let total = Object.keys(flashcards).length;
totalSpan.innerHTML = total;

textElement.innerHTML = unknownCards[index] ? unknownCards[index].term : null;
if (!unknownCards[index] || unknownCards[index].term !== flashcards[index].term) { // hack so it is always diplaying the proper card
    switchToNext();
}

// Base functions:
function countCards(){
    knownCounter = 0;
    unknownCounter = 0;
    flashcards.forEach(card => {
        if (card.known === true){
            knownCounter++;
        } else {
            unknownCounter++;
        }
    });
    markKnowElement.innerHTML = knownCounter;
    markUnknowElement.innerHTML = unknownCounter;
    indexSpan.innerHTML = index + 1; // +1 so it shows the correct card at the moment
}

function switchToNext(){
    flipped = false;
    let initialIndex = index;

    do {
        if (index < flashcards.length - 1){
            index += 1;
        } else {
            index = 0;
        }
    } while (index !== initialIndex && flashcards[index].known === true);

    if (index === initialIndex && flashcards[index].known === true){
        textElement.innerHTML = "You know all the flashcards! 🎉"
    } else {
        let next_word = flashcards[index].term;
        textElement.innerHTML = next_word;
    }
}

function switchToPrevious(){ // TODO: make this work
    flipped = false;
    if (index != 0){
        index -= 1;
        textElement.innerHTML = flashcards[index].term;
    } else {
        index = flashcards.length - 1;
        textElement.innerHTML = flashcards[index].term;
    }
    countCards();
}

function flipCard(){
    if (flipped === false){
        let value = flashcards[index].definition;
        textElement.innerHTML = value;
        flipped = true;
    } else {
        let key = flashcards[index].term;
        textElement.innerHTML = key;
        flipped = false;
    }
}

function changeToKnow(){
    flashcards[index].known = true;
    let jsonData = {'card_id': flashcards[index].id, 'known': true};
    sendCardData(jsonData, apiUrl, 'PUT');
    switchToNext();
    countCards();
}

function changeToDontKnow(){
    flashcards[index].known = false;
    let jsonData = {'card_id': flashcards[index].id, 'known': false};
    sendCardData(jsonData, apiUrl, 'PUT');
    switchToNext();
    countCards();
}

function resetCards(){
    flashcards.forEach(card =>{
        card.known = false;
    });
    let jsonData = {'stack_id': stackId};
    sendCardData(jsonData, apiUrl, 'PUT');
    index = 0;
    countCards();
    textElement.innerHTML = flashcards[index].term;
}

// Animation functions:
function flipCardAnimation() {
    articleElement.classList.add("flip");
    setTimeout(() => {
        articleElement.classList.add("flip-transparent");
    }, 150);
    setTimeout(() => {
        articleElement.classList.remove("flip");
        articleElement.classList.remove("flip-transparent");
        flipCard();
    }, 500);
}

function changeToKnowAnimation() {
    articleElement.classList.add("fadeout-right");
    setTimeout(() => {
        articleElement.classList.remove("fadeout-right");
        changeToKnow();
    }, 500);
}

function changeToDontKnowAnimation() {
    articleElement.classList.add("fadeout-left");
    setTimeout(() => {
        articleElement.classList.remove("fadeout-left");
        changeToDontKnow();
    }, 500);
}

function switchToPreviousAnimation() {
    articleElement.classList.add("move-left");
    setTimeout(() => {
        articleElement.classList.remove("move-left");
        articleElement.classList.add("move-back-from-left");
        switchToPrevious();
    }, 550);
    setTimeout(() => {
        articleElement.classList.remove("move-back-from-left");
    }, 1000);
}

function resetCardsAnimation() {
    articleElement.classList.add("reset");
    setTimeout(() => {
        articleElement.classList.remove("reset");
        resetCards();
    }, 500);
}

// On button click events:
resetButton.addEventListener("click", resetCardsAnimation);
flipButton.addEventListener("click", flipCardAnimation);
knowButton.addEventListener("click", changeToKnowAnimation);
learningButton.addEventListener("click", changeToDontKnowAnimation);
previousButton.addEventListener("click", switchToPreviousAnimation);

// On key press events:
document.body.onkeyup = function(event) {
    if (event.key === " " || event.code === "Space" || event.keyCode === 32 || event.keyCode === 38) {
        event.preventDefault();
        flipCardAnimation();
    }
    else if (event.key === "ArrowRight" || event.code === "ArrowRight" || event.keyCode === 39) {
        event.preventDefault();
        changeToKnowAnimation();
    }
    else if (event.key === "ArrowLeft" || event.code === "ArrowLeft" || event.keyCode === 37) {
        event.preventDefault();
        changeToDontKnowAnimation();
    }
    else if (event.key === "p" || event.code === "p" || event.keyCode === 80) {
        event.preventDefault();
        switchToPreviousAnimation();
    }
    else if (event.key === "r" || event.code === "r" || event.keyCode === 82) {
        event.preventDefault();
        resetCardsAnimation();
    }
}

function sendCardData(jsonData, apiURL, method = 'POST') {
    var xhr = new XMLHttpRequest();
    xhr.open(method, apiURL, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function(){
        if (xhr.readyState === 4 && xhr.status === 200) {
            console.log('Response: ', xhr.responseText);
        }
    };
    xhr.send(JSON.stringify(jsonData));
}

countCards();
