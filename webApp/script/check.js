function validaFrequenza() {
    const numero = parseFloat(document.getElementById("frequence_num").value);
    const unita = document.getElementById("frequence_hz").value;

    if (isNaN(numero) || !unita) {
        alert("Inserisci un valore e seleziona un'unità valida.");
        return false;
    }

    // Converti tutto in MHz
    let valoreInMHz = numero;
    if (unita === "Hz") valoreInMHz = numero / 1e6;
    else if (unita === "KHz") valoreInMHz = numero / 1e3;
    else if (unita === "GHz") valoreInMHz = numero * 1e3;

    if (valoreInMHz < 20 || valoreInMHz > 1768) {
        alert("Valore fuori dal range consentito.");
        return false;
    }

    return true;
}