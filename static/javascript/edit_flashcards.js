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
let editButton = document.getElementById('editButton');
const mainElement = document.getElementsByTagName('main')[0];


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

function mappingCards(cards, edit = false) {
    if (edit) {
        render = cards.map(card =>`
            <div class="bg-white dark:bg-slate-700 mt-2 mb-4 rounded-lg py-5 px-8 text-left font-medium"> 
                <div class="flex flex-row">
                    <div contenteditable="true" class="w-11/12 text-start">${card.term}</div>
                    <button onclick="deleteCard(${card.id})" class="text-gray-500 hover:text-red-500 text-xl w-1/12 text-end"><i class="fa fa-trash-o"></i></button>
                </div>
                <hr class="my-3">
                <div contenteditable="true" class="w-11/12 text-start">${card.definition}</div>
            </div>
        `).join('');
    } else {
        render = cards.map(card =>`
            <div class="bg-white dark:bg-slate-700 mt-2 mb-4 rounded-lg py-5 px-8 text-left font-medium"> 
                <div class="flex flex-row">
                    <div class="w-11/12 text-start">${card.term}</div>
                </div>
                <hr class="my-3">
                <div class="w-11/12 text-start">${card.definition}</div>
            </div>
        `).join('');
    }
    return render;
}

function renderCards(edit = false) {
    const knownCards = flashcards.filter(card => {return card.known});
    const unknownCards = flashcards.filter(card => {return !card.known});
    unknownCardsDiv.innerHTML = '';
    knownCardsDiv.innerHTML = '';

    unknownCardsDiv.innerHTML = mappingCards(unknownCards, edit);
    knownCardsDiv.innerHTML = mappingCards(knownCards, edit);
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
        sendCardData(newCardJsonData, apiUrl, 'POST', function(response){
            newCardJsonData.id = response.newCardId;
            flashcards.unshift(newCardJsonData);
            if (edit) {
                renderCards(edit = true);
            } else {
                renderCards();
            }
            countCards();
        });

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

// Delete card:
function deleteCard(cardId){
    let deleteCardJson = {'card_id': cardId};
    sendCardData(deleteCardJson, apiUrl, 'DELETE', function() {
        without_deleted = flashcards.filter(card => card.id !== cardId);
        flashcards = without_deleted;
        if (edit) {
            renderCards(edit = true);
        } else {
            renderCards();
        }
        countCards();
    });
}

// Edit button:
let edit = false;

function editTriger(){
    if (!edit) {
        // Switches it in edit mode
        edit = true;
        editButton.innerHTML = 'Done';
        renderCards(true);
    } else {
        // Switches back to non-edit mode
        edit = false
        editButton.innerHTML = 'Edit';
        renderCards();
    }
}

function sendCardData(jsonData, apiURL, method = 'POST', callback) {
    var xhr = new XMLHttpRequest();
    xhr.open(method, apiURL, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function(){
        if (xhr.readyState === 4 && xhr.status === 200) {
            console.log('Response: ', xhr.responseText);
            if (callback) {
                callback(JSON.parse(xhr.responseText));
            }
        }
    };
    xhr.send(JSON.stringify(jsonData));
    return xhr.responseText;
}

countCards();
renderCards();
