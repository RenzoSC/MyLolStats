let target = document.getElementById("matchbar");
let wins = parseInt(target.dataset.win);
let def = parseInt(target.dataset.def);
let winbar = document.getElementById("winbar");

let total = wins+def
let winPercentage = ((wins / total)* 100).toFixed(2);

winbar.style.width = winPercentage + "%";