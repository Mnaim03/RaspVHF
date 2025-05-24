<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $num = trim($_POST["frequence_num"]);
    $hz = trim($_POST["freuqnece_hz"]);

    $filename = "inputData";

    // Costruisci il contenuto da salvare
    $contenuto = "frequence_num = $num\nfreuqnece_hz = $hz\n";

    // Sovrascrivi completamente il file
    file_put_contents($filename, $contenuto);

    echo "<p>✅ File aggiornato con successo!</p>";
    echo "<pre>$contenuto</pre>";
    echo '<a href="index.html">Torna alla pagina principale</a>';
} else {
    header("Location: index.html");
    exit;
}
?>