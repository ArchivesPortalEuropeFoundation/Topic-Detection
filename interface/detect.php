<?php

ini_set('session.gc_maxlifetime', 10800);

ini_set('session.gc_probability', 1);
ini_set('session.gc_divisor', 100);

session_start();

$time = date('Y-m-d H:i:s');;
  
$_SESSION["lang"] = $_POST['lang'];
$_SESSION["text"] = $_POST['text'];

$url= $ENV['URI_API_BACKEND'].'/detect?';

$data = array('lang' => $_SESSION['lang'],
              'text' => $_SESSION['text'],
            );

$msg = http_build_query($data);

$url .= $msg;
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
$result = curl_exec($ch);

echo $result;  
?>
