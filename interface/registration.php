<?php
ob_start();

$whitelist = file("../whitelist.txt", FILE_IGNORE_NEW_LINES);
$cred = file_get_contents("../cred.json");
$cred = json_decode($cred, true);
$email = strtolower($_POST['email']);

if( (in_array( $_POST['email'] ,$whitelist )) && (!isset($cred[$email])))
{
	$user =$_POST['username'];
	$pw = $_POST['password'];
	
	$tmp = array(
        'user' => $user,
        'pw' => password_hash($pw, PASSWORD_DEFAULT)
    );
	$cred[ $email ] =$tmp ;
	file_put_contents( "../cred.json", json_encode( $cred ) );
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