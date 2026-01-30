// TypeIt js
document.addEventListener("DOMContentLoaded", function () {
    if (!window.typeitInitialized){
        new TypeIt(".subtitle", {
            speed:95,
            loop:true
        })
        .type("Pour éclairer le futur.")
        .pause(5000)
        .delete(null)
        .type("Pour mieux comprendre le présent.")
        .pause(5000)
        .delete(null)
        .type("Pour une rennaissance Africaine digne et souveraine.")
        .pause(5000)
        .delete(null)
        .type("Pour un développement basé sur nos valeurs endogènes et notre culture.")
        .pause(5000)
        .delete(null)
        .go();
    }
    window.typeitInitialized = true;

});

// affichage dynamique des articles
let Btnrecent = document.querySelector('.recent');
let Btnpopulaire = document.querySelector('.populaire');
let container = document.getElementById("container")

function loadArticles(url) {
    fetch(url)
        .then(response => response.text())
        .then(html => {
            container.innerHTML = html;
            container.classList.remove("hidden");
        })
        .catch(err => console.error(err));
}

Btnrecent.addEventListener("click", () => {
    loadArticles("/authapp/recent/");
});

Btnpopulaire.addEventListener("click", () => {
    loadArticles("/authapp/populaire/");
});

container.addEventListener("click", (e) => {
    e.stopPropagation();
});

// Clic PARTOUT ailleurs sur la page
document.addEventListener("click", () => {
    if (!container.classList.contains("hidden")) {
        container.classList.add("hidden");
    }
});