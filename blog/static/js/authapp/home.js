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
