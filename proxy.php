<?php
// proxy.php

$url = isset($_GET['url']) ? $_GET['url'] : null;

if (!$url) {
    http_response_code(400);
    echo "URL parametresi belirtilmemiş.";
    exit;
}

// Uzak kaynağı al
$ch = curl_init($url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HEADER, false);

// Yanıtı al
$response = curl_exec($ch);
$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
$contentType = curl_getinfo($ch, CURLINFO_CONTENT_TYPE);

curl_close($ch);

// Eğer content-type m3u8 ise uygun header gönder
if (strpos($contentType, 'application/vnd.apple.mpegurl') !== false ||
    strpos($contentType, 'application/x-mpegurl') !== false ||
    strpos($url, '.m3u8') !== false) {
    header('Content-Type: application/vnd.apple.mpegurl');
} else {
    header('Content-Type: '.$contentType);
}

// HTTP kodunu ayarla
http_response_code($httpCode);

// Yanıtı döndür
echo $response;
?>
