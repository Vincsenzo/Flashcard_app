let flashcardsString = document.currentScript.getAttribute('data-cards');
let apiUrl = document.currentScript.getAttribute('data-url');
let stackId = document.currentScript.getAttribute('data-stack-id');
let flashcards = JSON.parse(flashcardsString);
let knownCounter = 0;
let unknownCounter = 0;
let messageDisplayed = false;
let knownCardsCounter = document.getElementById('knownCardsCounter');
let unknownCardsCounter = document.getElementById('unknownCardsCounter');
let addNewCardButton = document.getElementById('addNewCardButton');
let unknownCardsDiv = document.getElementById('unknownCardsDiv');
let knownCardsDiv = document.getElementById('knownCardsDiv');
const mainElement = document.getElementsByTagName('main')[0];

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
    knownCardsCounter.innerHTML = 'Known cards (' + knownCounter + '):'; 
    unknownCardsCounter.innerHTML = 'Unknown cards (' + unknownCounter + '):'; 
}

function renderCards() {
    const knownCards = flashcards.filter(card => {return card.known});
    const unknownCards = flashcards.filter(card => {return !card.known});
    unknownCardsDiv.innerHTML = '';
    knownCardsDiv.innerHTML = '';

    unknownCardsDiv.innerHTML = unknownCards.map(card =>`
        <div class="bg-white dark:bg-slate-700 mt-2 mb-4 rounded-lg py-5 px-8 text-left font-medium"> ${card.term} <br> <br><hr> <br> ${card.definition} </div>
    `).join('');
    knownCardsDiv.innerHTML = knownCards.map(card =>`
        <div class="bg-white dark:bg-slate-700 mt-2 mb-4 rounded-lg py-5 px-8 text-left font-medium"> ${card.term} <br> <br><hr> <br> ${card.definition} </div>
    `).join('');
}

// Add new cards:
let termInput;
let definitionInput;

function addNewCard() {
    const inputDiv = document.getElementById('inputDiv');
    termInput = document.getElementById('termInput');
    definitionInput = document.getElementById('definitionInput');
    
    if (termInput.value.trim() !== "" && definitionInput.value.trim() !== "") {
        let newCardJsonData = {
            'term': termInput.value,
            'definition': definitionInput.value,
            'stack': stackId,
            'known': false,
        };
        termInput.value = "";
        definitionInput.value = "";
        sendCardData(newCardJsonData, apiUrl);
        flashcards.unshift(newCardJsonData);
        renderCards();
        countCards();

        messageDisplayed = false;
        inputDiv.classList.remove('border-2');
        inputDiv.classList.remove('border-solid');
        inputDiv.classList.remove('border-red-500');
    }
    else {
        if (!messageDisplayed) {
            inputDiv.classList.add('border-2');
            inputDiv.classList.add('border-solid');
            inputDiv.classList.add('border-red-500');
            messageDisplayed = true;
        }
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
renderCards();
