let flashcardsString = document.currentScript.getAttribute('data-cards');
let apiUrl = document.currentScript.getAttribute('data-url');
let stackId = document.currentScript.getAttribute('data-stack-id');
let flashcards = JSON.parse(flashcardsString);

let knownCounter = 0;
let unknownCounter = 0;

let markKnowElement = document.getElementById('numberOfKnown');
let markUnknowElement = document.getElementById('numberOfUnknown');
let addNewCardButton = document.getElementById('addNewCardButton');
let knownCardsP = document.getElementById('knownCardsP');
let unknownCardsP = document.getElementById('unknownCardsP');

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
}

function renderCards(cards) {
    const knownCards = flashcards.filter(card => {return card.known});
    const unknownCards = flashcards.filter(card => {return !card.known});

    knownCardsP.insertAdjacentHTML('beforeend', knownCards.map(card =>`
        <article> ${card.term} <br><hr> ${card.definition} </article>
    `).join(''));
    unknownCardsP.insertAdjacentHTML('beforeend', unknownCards.map(card =>`
        <article> ${card.term} <br><hr> ${card.definition} </article>
    `).join(''));
}

countCards();
renderCards(flashcards);