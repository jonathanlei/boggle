"use strict";

const $playedWords = $("#words");
const $form = $("#newWordForm");
const $wordInput = $("#wordInput");
const $message = $(".msg");
const $table = $("table");

let gameId;


/** Start */

async function start() {
  let response = await axios.get("/api/new-game");
  gameId = response.data.gameId;
  let board = response.data.board;

  displayBoard(board);

  //add event listener for submit form
  $form.on("submit", submitWord)
}

/** Display board */

function displayBoard(board) {
  let $tbody = $("tbody");
  $tbody.empty();
  // loop over board and create the DOM tr/td structure
  for (let row of board) {
    let newRow = $('<tr>')
    for (let ltr of row) {
      let newLtr = $('<td>').text(ltr);
      newRow.append(newLtr);
    }
    $tbody.append(newRow);
  }
}

/** Listens to word being submitted and sends POST request
 *  Returns: 
 */

async function submitWord(evt) {
  evt.preventDefault();
  let word = $wordInput.val().toUpperCase();
  let response = await axios.post("/api/score-word", { gameId, word });
  // console.log(response.data);
  playUpdate(response.data.result, word);
}

/** Checks if word submitted is a legal play and update DOM with play */

function playUpdate(result, word) {
  // console.log(word);
  // console.log(result);
  if (result === "ok") {
    $message.empty();
    $playedWords.append($(`<li>${word}</li>`));
  }
  else if (result === "not-on-board") {
    $message.text(`${word} is not on board`);
  }
  else if (result === "not-word") {
    $message.text(`${word} is not a word`);
  }
}

start();