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

document.getElementById("clearLogsBtn").addEventListener("click", () => {
    if (confirm("Sei sicuro di voler cancellare tutti i log?")) {
        fetch("../php/clearLogs.php", { method: "POST" })
            .then(res => res.json())
            .then(async response => {
                if (response.success) {
                    document.getElementById("logs").innerHTML = "Log cancellati.";
                    await sleep(4000);
                } else {
                    document.getElementById("logs").innerHTML = "Errore: " + (response.error || "Impossibile cancellare i log.");
                }
            })
            .catch(err => {
                document.getElementById("logs").innerHTML = "Errore nella richiesta: " + err;
            });
    }
});
