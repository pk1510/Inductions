<?
  
  $line = '';
  /*$f = fopen( "./details.txt", "r" );
  $line = `tail -n 1 $f`;
  $cursor = -1;
  if ( $f ) {
    fseek($f, $cursor, SEEK_END);
    $char = fgetc($f);
    while( $char === "\n" || $char === "\r" ) {
       fseek($f, $cursor--, SEEK_END);
       $char = fgetc($f);
    }
    while( $char !== false && $char !== "\n" && $char !== "\r" ) {
       $line = $char . $line;
       fseek($f, $cursor--, SEEK_END);
       $char = fgetc($f);
    }*/                                      // to get the last line of the file
    $f = fopen( "./testing.txt". "r" ); 
    $line = fread($f, filesize("./testing.txt"));
    $credentials = explode ('&', $line);
    $userid = explode ('=', $credentials[0]);
    $password = explode ('=', $credentials[1]);
    $check = explode ('=', $credentials[2]);
     
    
    if ( $check[1] === "on" ) {
      setcookie ("userName", $userid[1], time() + 86400);
      setcookie ("passWord", $password[1], time() + 86400);
    }
  
?>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Satisfy|Tangerine&display=swap">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    <title>login</title>
    <link href="./my.css" rel="stylesheet" type="text/css">
    <link href="./sht.css" rel="stylesheet" type="text/css">
</head>

<body>
    <form action="index.php" method="post">
        <div class="txt_container">
            <label for="my_name"> User ID: </label>
            <input type="text" name="user_id" value="<?php if(isset($_COOKIE["userName"])) { echo $_COOKIE["userName"]; } ?>">     //setting the cookies
        </div>
        <div class="txt_container">
            <label for="my_name"> Password: </label>
            <input type="password" name="passd" value="<?php if(isset($_COOKIE["passWord"])) { echo $_COOKIE["passWord"]; } ?>">    // setting the cookies
        </div>
        <div class="txt_container">
	Remember Me: <input type="checkbox" name="check">
        </div>
        <div class="txt_container">
            <button> SUBMIT </button>
        </div>
    </form>

    <?php
        $username = $_POST["user_id"];
	$password = $_POST["passd"];
        $f = fopen( "./testing.txt". "r" );
        $line = fread($f, filesize("./testing.txt"));
        echo $line;
       
	if ( isset($_COOKIE["userName"]) && isset($_COOKIE["passWord"]) ){
          if ( $username === $_COOKIE["userName"] && $password === $_COOKIE["passWord"] ) {
            echo "User Id: $username \n";
	    echo "Password: $password";
          }
          else {
            echo "invalid login credentials, try again";
          }
        }
        else {
          echo "User Id: $username \n";
          echo "Password: $password";
        }
        
    ?>
</body>

</html>
