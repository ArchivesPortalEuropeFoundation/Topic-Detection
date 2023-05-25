<?php

ini_set('session.gc_maxlifetime', 10800);

ini_set('session.gc_probability', 1);
ini_set('session.gc_divisor', 100);

session_start();

$ENV = parse_ini_file('../config/config.env');

$time = date('Y-m-d H:i:s');;
  
$_SESSION["lang"] = $_POST['lang'];
$_SESSION["type"] = $_POST['type'];
$_SESSION["text"] = $_POST['text'];
$_SESSION["n_res"] = $_POST['n_res'];
$_SESSION["broad_entity_search"] = isset($_POST['broad_entity_search']) ? "True" : "False";
$_SESSION["boolean_search"] = isset($_POST['boolean_search']) ? "True" : "False";
$_SESSION["topic"] = $_POST['topic'];

$url= $ENV['URI_API_BACKEND'].'/query?';

$data = array('lang' => $_SESSION['lang'],
              'type' => $_SESSION['type'],
              'text' => $_SESSION['text'],
              'n_res' => $_SESSION['n_res'],
              'broad_entity_search' => $_SESSION['broad_entity_search'],
              'boolean_search' => $_SESSION['boolean_search'],
              'topic' => $_SESSION['topic']
            );

$msg = http_build_query($data);

$url .= $msg;
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_HEADER, true);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
$result = curl_exec($ch);
$httpcode = curl_getinfo($ch, CURLINFO_HTTP_CODE);

error_log('TopicDetection: lang:'.$data['lang']. '@type:'.$data['type']. '@text:'.$data['text']. '@n_res:'.$data['n_res']. '@broad_entity_search:'.$data['broad_entity_search']. '@boolean_search:'.$data['boolean_search']. '@type:'.$data['topic'].'@status:'.$httpcode);

$whatIWant = substr($result, strpos($result, " GMT") +4);
echo $whatIWant;
?>
