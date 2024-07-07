<?php
$name = $_GET["name"] ?? null;
$score = $_GET["score"] ? (int) $_GET["score"] : null;

$data = json_decode(file_get_contents("data.json"), true);

if (!empty($name) && !empty($score)) {
    $data[] = [
        "name" => substr($name, 0, 20),
        "score" => $score,
    ];

    file_put_contents("data.json", json_encode($data, true));
}

header("Content-Type: application/json; charset=UTF-8");

usort($data, function ($a, $b) {
    return $a["score"] < $b["score"] ? 1 : -1;
});

$data = array_slice($data, 0, 10);
echo json_encode($data);
exit();
