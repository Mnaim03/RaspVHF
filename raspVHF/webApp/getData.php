<?php
$contenuto = file_get_contents("outputData.txt");
$righe = explode("\n", $contenuto);
$dati = [];

foreach ($righe as $riga) {
    $parti = explode("=", $riga);
    if (count($parti) == 2) {
        $chiave = trim($parti[0]);
        $valore = trim($parti[1]);
        $dati[$chiave] = $valore;
    }
}

// Restituisci come JSON
header('Content-Type: application/json');
echo json_encode($dati);
?>