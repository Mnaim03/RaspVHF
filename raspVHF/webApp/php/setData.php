<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $num = trim($_POST["frequence_num"]);
    $hz = trim($_POST["scelta"]);

    $filename = "Data";

    if (file_exists($filename)) {
        $lines = file($filename, FILE_IGNORE_NEW_LINES);
        foreach ($lines as &$line) {
            if (str_starts_with($line, 'frequence_num =')) {
                $line = "frequence_num = $num";
            } elseif (str_starts_with($line, 'freuqnece_hz =')) {
                $line = "freuqnece_hz = $hz";
            }
        }
        file_put_contents($filename, implode("\n", $lines));
    } else {
        $lines = [
            "frequence_num = $num",
            "freuqnece_hz = $hz"
        ];
        file_put_contents($filename, implode("\n", $lines));
    }

    echo "<p>✅ File aggiornato con successo!</p>";
    echo "<pre>frequence_num = $num\nfreuqnece_hz = $hz</pre>";
    echo '<a href="./index.html">Torna alla pagina principale</a>';
} else {
    header("Location: ./index.html");
    exit;
}
?>