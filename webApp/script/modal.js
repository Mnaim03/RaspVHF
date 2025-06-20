
    function openModal() {
    document.getElementById("myModal").style.display = "block";
}

    function closeModal() {
    document.getElementById("myModal").style.display = "none";
}

    // Chiudi cliccando fuori dal contenuto
    window.onclick = function(event) {
    const modal = document.getElementById("myModal");
    if (event.target == modal) {
    closeModal();
}
}
