<?php
header('Content-Type: application/json');

// Leggi il file
$filename = "outputData";
if (!file_exists($filename)) {
    echo json_encode(["errore" => "File non trovato"]);
    exit;
}

$contenuto = file_get_contents($filename);
if ($contenuto === false) {
    echo json_encode(["errore" => "Impossibile leggere il file"]);
    exit;
}

// Divide il contenuto per righe in modo sicuro
$righe = preg_split('/\r\n|\r|\n/', $contenuto);

$dati = [];

foreach ($righe as $riga) {
    $parti = explode("=", $riga);
    if (count($parti) == 2) {
        $chiave = trim($parti[0]);
        $valore = trim($parti[1]);
        $dati[$chiave] = $valore;
    }
}

// Se $dati è vuoto, mostra errore utile
if (empty($dati)) {
    echo json_encode(["errore" => "Dati non trovati o formato errato"]);
    exit;
}

echo json_encode($dati);
?>