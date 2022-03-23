<?php
ob_start();

#$whitelist = file("../whitelist.txt", FILE_IGNORE_NEW_LINES);
#$cred = file_get_contents("../cred.json");
#$cred = json_decode($cred, true);
$email = strtolower($_POST['email']);

#if( (in_array( $_POST['email'] ,$whitelist )) && (!isset($cred[$email])))

$user =$_POST['username'];
$pw = $_POST['password'];
$url= 'http://127.0.0.1:5000/registration?';

$data = array('user' => $user,
			'email' => $email,
			'pw' => $pw
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
	header('Location: login.html');
	ob_end_flush();
    die();
}

else{
	echo "wrong email";
	ob_end_flush();
    die();
	}
	

?>
