<?php
$db_name = "id19863519_sensors";
$db_user = "id19863519_aubis5d";
$db_host = "localhost";
$db_pass = "****93&RH<@{****";

if(isset($_GET["submit"])){
    $data = array();
    $mysqli = new mysqli($db_host, $db_user, $db_pass, $db_name);
    if ($mysqli->connect_errno) {
        $data['status'] = "error";
        $data['error'] = "Failed to connect to MySQL: (" . $mysqli->connect_errno . ") " . $mysqli->connect_error;
    }else{
        $data['status'] = "success";
        $con = mysqli_connect($db_host, $db_user, $db_pass, $db_name);
        #get the last image link
        $sql = "SELECT * FROM `images` ORDER BY `id` DESC LIMIT 1";
        $result = mysqli_query($con, $sql);
        if (mysqli_num_rows($result) > 0) {
            $row = mysqli_fetch_array($result);
            $data['link'] = $row['link'];
        }else
            $data['status'] = "error";
            $data['error'] = "No image found";
    }
    echo json_encode($data);
}

?>