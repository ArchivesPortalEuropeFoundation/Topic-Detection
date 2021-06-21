<?php
ob_start();

# Session lifetime of 3 hours
ini_set('session.gc_maxlifetime', 10800);

# Enable session garbage collection with a 1% chance of
# running on each session_start()
ini_set('session.gc_probability', 1);
ini_set('session.gc_divisor', 100);

session_start();

$cred = file_get_contents("../cred.json");
$cred = json_decode($cred, true);

$_SESSION["email"] = strtolower($_POST['email']);
$_SESSION["password"] = $_POST['password'];

if (isset($cred[$_SESSION["email"]]) && password_verify($_SESSION["password"], $cred[$_SESSION["email"]]["pw"]))
{
  $_SESSION["user"] = $cred[$_SESSION["email"]]["user"];
  
header('Location: index.html');
ob_end_flush();
die();

}
else {
            echo "incorrect login";
            ob_end_flush();
            die();        
        }
?>