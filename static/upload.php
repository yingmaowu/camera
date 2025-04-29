<?php
$data = json_decode(file_get_contents("php://input"), true);
if (!$data || !isset($data['image'])) {
    echo "無效圖片資料";
    exit;
}

$image = $data['image'];
$image = str_replace('data:image/png;base64,', '', $image);
$image = str_replace(' ', '+', $image);
$imageData = base64_decode($image);

$filename = 'uploads/photo_' . time() . '.png';
file_put_contents($filename, $imageData);

echo "圖片已儲存：" . $filename;
?>
