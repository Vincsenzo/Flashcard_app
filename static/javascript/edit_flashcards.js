let flashcardsString = document.currentScript.getAttribute('data-cards');
let apiUrl = document.currentScript.getAttribute('data-url');
let stackId = document.currentScript.getAttribute('data-stack-id');
let flashcards = JSON.parse(flashcardsString);
let knownCounter = 0;
let unknownCounter = 0;
let messageDisplayed = false;
let markKnowElement = document.getElementById('numberOfKnown');
let markUnknowElement = document.getElementById('numberOfUnknown');
let knownCardsP = document.getElementById('knownCardsP');
let unknownCardsP = document.getElementById('unknownCardsP');
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
    markKnowElement.innerHTML = knownCounter;
    markUnknowElement.innerHTML = unknownCounter;
    knownCardsP.innerHTML = 'Known cards (' + knownCounter + '):'; 
    unknownCardsP.innerHTML = 'Unknown cards (' + unknownCounter + '):'; 
}

function renderCards() {
    const knownCards = flashcards.filter(card => {return card.known});
    const unknownCards = flashcards.filter(card => {return !card.known});
    unknownCardsDiv.innerHTML = '';
    knownCardsDiv.innerHTML = '';

    unknownCardsDiv.innerHTML = unknownCards.map(card =>`
        <article> ${card.term} <br><hr> ${card.definition} </article>
    `).join('');
    knownCardsDiv.innerHTML = knownCards.map(card =>`
        <article> ${card.term} <br><hr> ${card.definition} </article>
    `).join('');
}

// Add new cards:
let termInput;
let definitionInput;

function sendCardData(jsonData, apiURL) {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', apiURL, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function(){
        if (xhr.readyState === 4 && xhr.status === 200) {
            console.log('Response: ', xhr.responseText);
        }
    };
    xhr.send(JSON.stringify(jsonData));
}

function addNewCard() {
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
        const messageElement = document.getElementById('message');
        if (messageElement) {messageElement.remove()}
    }
    else {
        if (!messageDisplayed) {
            const newParagraph = document.createElement('article');
            newParagraph.setAttribute("id", "message")
            newParagraph.textContent = 'Fill in the card ☝️';
            addNewCardButton.parentNode.insertBefore(newParagraph, addNewCardButton);
            messageDisplayed = true;
        }
    }
}

countCards();
renderCards();
