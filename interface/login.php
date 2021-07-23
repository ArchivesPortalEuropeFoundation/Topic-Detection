<?php
ob_start();

# Session lifetime of 3 hours
ini_set('session.gc_maxlifetime', 10800);

# Enable session garbage collection with a 1% chance of
# running on each session_start()
ini_set('session.gc_probability', 1);
ini_set('session.gc_divisor', 100);

session_start();

$_SESSION["email"]  = $_POST['email'];
$_SESSION["password"] = $_POST['password'];

$url= 'http://127.0.0.1:5000/login?';

$data = array(
			'email' => $_SESSION["email"],
			'pw' => $_SESSION["password"]
			);

$msg = http_build_query($data);

$url .= $msg;
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
//curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
$result = curl_exec($ch);

if (True == $result) {
	echo $result;	
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