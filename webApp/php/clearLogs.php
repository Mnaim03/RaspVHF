<?php
header('Content-Type: application/json');

$filename = "../logs.txt";

if (file_exists($filename)) {
    if (file_put_contents($filename, "") !== false) {
        echo json_encode(["success" => true]);
    } else {
        echo json_encode(["success" => false, "error" => "Errore durante la cancellazione del file"]);
    }
} else {
    echo json_encode(["success" => false, "error" => "File non trovato"]);
}
?>
