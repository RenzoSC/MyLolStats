function changeFilter(event){
    target = event.currentTarget;
    let filterId = target.getAttribute("data-filterId");
    let filters = ["all", "soloq", "flex"];
    let last_selected = document.getElementsByClassName("f_selected");
    last_selected[0].classList.remove("f_selected");
    target.classList.add("f_selected");

    let gamemodes_div = document.getElementsByClassName("gamemodes");
    for (let i = 0; i < gamemodes_div.length; i++) {
        gamemodes_div[i].className = "gamemodes hidden";
    }
    let filter_target = document.getElementById(filters[filterId]);
    filter_target.classList.remove("hidden");
    filter_target.classList.remove("visible");

}