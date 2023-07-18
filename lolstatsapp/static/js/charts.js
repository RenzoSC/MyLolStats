let target = document.getElementById("matchbar");
let wins = parseInt(target.dataset.win);
let def = parseInt(target.dataset.def);
let winbar = document.getElementById("winbar");
console.log(wins)
console.log(def)
let total = wins+def
// Calcular el porcentaje
let winPercentage = ((wins / total)* 100).toFixed(2);

winbar.style.width = winPercentage + "%";
console.log(winPercentage)