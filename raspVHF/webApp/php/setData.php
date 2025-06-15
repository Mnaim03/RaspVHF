<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $num = trim($_POST["frequence_num"]);
    $hz = trim($_POST["freuqnece_hz"]);

    $filename = "../Data";

    if (file_exists($filename)) {
        $lines = file($filename, FILE_IGNORE_NEW_LINES);
        foreach ($lines as &$line) {
            if (str_starts_with($line, 'frequence_num =')) {
                $line = "frequence_num = $num";
            } elseif (str_starts_with($line, 'frequence_hz =')) {
                $line = "frequence_hz = $hz";
            }
        }
        file_put_contents($filename, implode("\n", $lines));
    } else {
        $lines = [
            "frequence_num = $num",
            "frequence_hz = $hz"
        ];
        file_put_contents($filename, implode("\n", $lines));
    }

    echo "<script>
        alert('🫐📡 File aggiornato con successo!');
        window.location.href = '../index.html';
        </script>";

} else {
    header("Location: ../index.html");
    exit;
}
?>