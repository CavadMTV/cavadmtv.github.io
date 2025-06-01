<?php
// proxy.php

// URL parametresi kontrolü
$url = isset($_GET['url']) ? $_GET['url'] : null;

if (!$url) {
    http_response_code(400);
    echo "URL parametresi belirtilmemiş.";
    exit;
}

// cURL başlat
$ch = curl_init($url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

// Sonucu al
$response = curl_exec($ch);
$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);

// Aynı cevap kodunu döndür
http_response_code($httpCode);

// Sonucu ekrana yazdır
echo $response;

curl_close($ch);
?>
