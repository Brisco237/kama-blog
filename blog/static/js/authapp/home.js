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
        .type("Pour un développement basé sur nos valeurs endogenes et notre culture.")
        .pause(5000)
        .delete(null)
        .go();
    }
    window.typeitInitialized = true;

});

// affichage dynamique des articles
let recent = document.querySelector('.recent');
let populaire = document.querySelector('.populaire');
let affichage_recent = document.getElementById("recent-affichage")
let affichage_populaire = document.getElementById("populaire-affichage")


populaire.addEventListener('click', () => {
    affichage_populaire.classList.remove('active')
    affichage_recent.classList.add('active')
});

recent.addEventListener('click', () => {
    affichage_populaire.classList.add('active')
    affichage_recent.classList.remove('active')
});