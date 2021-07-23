<?php

ini_set('session.gc_maxlifetime', 10800);

ini_set('session.gc_probability', 1);
ini_set('session.gc_divisor', 100);

session_start();

//$url= 'http://127.0.0.1:5000/login?';

//$data = array(
//			'email' => $_SESSION["email"],
//			'pw' => $_SESSION["password"]
//			);

//$msg = http_build_query($data);

//$url .= $msg;
//$ch = curl_init();
//curl_setopt($ch, CURLOPT_URL, $url);
//curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
//curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
//$result = curl_exec($ch);

//if (True == $result) {
$time = date('Y-m-d H:i:s');;
  
$_SESSION["lang"] = $_POST['lang'];
$_SESSION["type"] = $_POST['type'];
$_SESSION["text"] = $_POST['text'];
$_SESSION["n_res"] = $_POST['n_res'];
$_SESSION["broad_entity_search"] = isset($_POST['broad_entity_search']) ? "True" : "False";
$_SESSION["boolean_search"] = isset($_POST['boolean_search']) ? "True" : "False";

$url= 'http://127.0.0.1:5000/query?';

$data = array('lang' => $_SESSION['lang'],
              'type' => $_SESSION['type'],
              'text' => $_SESSION['text'],
              'n_res' => $_SESSION['n_res'],
              'broad_entity_search' => $_SESSION['broad_entity_search'],
              'boolean_search' => $_SESSION['boolean_search']

            );

$msg = http_build_query($data);

$url .= $msg;
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
//curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
$result = curl_exec($ch);

echo $result;

//}
//else {
//  echo "incorrect login";
//  ob_end_flush();
//  die();        
//}      
?>
