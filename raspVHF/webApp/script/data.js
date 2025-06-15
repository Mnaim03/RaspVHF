function aggiornaDati() {
    fetch("../php/getData.php")
    .then(res => res.json())
    .then(dati => {
        console.log("Dati ricevuti:", dati);
        console.log("Chiavi esatte:", Object.keys(dati));
        for (const chiave in dati) {
            console.log(`→ ${chiave} = ${dati[chiave]}`);
        }

        document.getElementById("valore").textContent = (dati.frequence_num ?? "--") + " " + (dati.frequence_hz ?? "(missing)");
        document.getElementById("anomalia").textContent = dati.anomalia === "true" ? "Anomalia Rilevata" : "No Anomalie";
        });
}

setInterval(aggiornaDati, 1000);
window.onload = aggiornaDati;