<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $num = trim($_POST["frequence_num"]);
    $hz = trim($_POST["freuqnece_hz"]);

    $filename = "Data";

    // Costruisci il contenuto da salvare
    $contenuto = "frequence_num = $num\nfreuqnece_hz = $hz\n";

    // Sovrascrivi completamente il file
    $existingData = file_exists($filename) ? file_get_contents($filename) : "";
    parse_str(str_replace(["\n", " = "], ["&", "="], $existingData), $data);
    $data['frequence_num'] = $num;
    $data['freuqnece_hz'] = $hz;
    $newContent = "";
    foreach ($data as $key => $value) {
        $newContent .= "$key = $value\n";
    }
    file_put_contents($filename, $newContent);

    echo "<p>✅ File aggiornato con successo!</p>";
    echo "<pre>$contenuto</pre>";
    echo '<a href="index.html">Torna alla pagina principale</a>';
} else {
    header("Location: index.html");
    exit;
}
?>