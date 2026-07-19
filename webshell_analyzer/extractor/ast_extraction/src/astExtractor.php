<?php
error_reporting(0);
ini_set('display_errors', 0);
ini_set('log_errors', 0);

ob_start();


require_once __DIR__ . '/../vendor/autoload.php';
require_once __DIR__ . '/astBuilder.php';

if($argc < 2) {
    echo json_encode("Error: No file path provided") . "\n";
    exit(1);
}

$filepath = $argv[1];

if(!file_exists($filepath)) {
    echo json_encode("Error: File not found: $filepath") . "\n";
    exit(1);
}


$code = file_get_contents($filepath);
$code = trim($code);


if ($code === false || trim($code) === '') {
    echo json_encode("Error Empty file");
    exit(1);
}

$builder = new astBuilder();

$result = $builder->builder($code);


if (!is_array($result)) {
    echo json_encode(["error" => "Builder did not return array"]);
    exit(1);
}

if(ob_get_length()){
    ob_clean();
}

// Output valid
echo json_encode($result);
?>