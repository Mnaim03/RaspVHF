function aggiornaLogs() {
    fetch("../php/getLogs.php")
        .then(res => res.json())
        .then(righe => {
            if (!Array.isArray(righe)) {
                document.getElementById("logs").innerHTML = "Errore: " + (righe.errore || "Formato sconosciuto");
                return;
            }
            document.getElementById("logs").innerHTML = righe.map(riga => `${riga}<br>`).join('');
        })
        .catch(err => {
            document.getElementById("logs").innerHTML = "Errore nel caricamento: " + err;
        });
}

setInterval(aggiornaLogs, 1000);
window.onload = aggiornaLogs;
