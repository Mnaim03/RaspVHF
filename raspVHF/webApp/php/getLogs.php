<?php
header('Content-Type: application/json');

$filename = "../logs.txt";
if (!file_exists($filename)) {
    echo json_encode(["errore" => "File non trovato"]);
    exit;
}

$contenuto = file_get_contents($filename);
if ($contenuto === false) {
    echo json_encode(["errore" => "Impossibile leggere il file"]);
    exit;
}

$righe = preg_split('/\r\n|\r|\n/', $contenuto);

// Filtra eventuali righe vuote
$righe = array_filter($righe, fn($r) => trim($r) !== "");

echo json_encode($righe);
?>
