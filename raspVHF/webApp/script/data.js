function aggiornaDati() {
    fetch("./php/getData.php")
        .then(res => res.json())
        .then(dati => {
            console.log(dati);  // <--- stampa in console
            document.getElementById("valore").textContent = dati.frequence_num + " " + dati.freuqnece_hz;
            document.getElementById("anomalia").textContent = dati.anomalia === "true" ? "Anomalia Rilevata" : "No Anomalie";
        });
}

setInterval(aggiornaDati, 1000);
window.onload = aggiornaDati;