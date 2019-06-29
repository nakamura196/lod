<?php
require 'vendor/autoload.php';

preg_match('|' . dirname($_SERVER['SCRIPT_NAME']) . '/([\w%/]*)|', $_SERVER['REQUEST_URI'], $matches);

$manifest = explode('/.php/', $_SERVER['REQUEST_URI'])[1];

$string = file_get_contents($manifest);
$json_a = json_decode($string, true);
$json_a["@context"] = "http://iiif.io/api/presentation/2/context.json";

header("Access-Control-Allow-Origin: *");

echo json_encode($json_a);

?>
            