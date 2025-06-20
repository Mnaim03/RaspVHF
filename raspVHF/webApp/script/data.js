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
        const anomaliaEl = document.getElementById("anomalia");

        const anomaliaPresente = dati.anomalia === "true";
        anomaliaEl.textContent = anomaliaPresente ? "Anomalia Rilevata" : "No Anomalie";
        anomaliaEl.style.color = anomaliaPresente ? "#fa7970" : "#7ce38b";
        });
}

setInterval(aggiornaDati, 1000);
window.onload = aggiornaDati;
