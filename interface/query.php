<?php
session_start();
     


$_SESSION["lang"] = $_POST['lang'];
$_SESSION["type"] = $_POST['type'];
$_SESSION["text"] = $_POST['text'];
$_SESSION["n_res"] = $_POST['n_res'];
$_SESSION["fuzzy_entity"] = isset($_POST['fuzzy_entity']) ? "True" : "False";

$url= 'http://127.0.0.1:5000/query?';

$data = array('lang' => $_SESSION['lang'],
              'type' => $_SESSION['type'],
              'text' => $_SESSION['text'],
              'n_res' => $_SESSION['n_res'],
              'fuzzy_entity' => $_SESSION['fuzzy_entity']

            );

$msg = http_build_query($data);

$url .= $msg;
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
//curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
$result = curl_exec($ch);

echo $result;

die();

?>
