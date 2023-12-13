<?php
    /*
    ini_set('display_errors', '1');
    ini_set('display_startup_errors', '1');
    error_reporting(E_ALL);*/

    $servername = "BNY-S-560";
    $username = "Nlng.Tia";
    $password = "Digital@1234";
    $database = "dataEntryDB";
    $port = "1433";
    $conn="";

    /*$servername_oci = "BNY-S-352/energy";
    $username_oci = "BIM_MRV";
    $password_oci = "UserMrv1";
    $database_oci = "energy";
    $conn_oci="";*/

    try {
        $conn = new PDO("sqlsrv:server=$servername;Database=$database;", $username, $password);
        //$conn_oci = new PDO("oci:server=$servername_oci;Database=$database_oci;", $username_oci, $password_oci);
    } catch (PDOException $e) {
        //echo ("Error connecting to SQL Server: " . $e->getMessage());
        echo ("Error connecting to Oracle Server: " . $e->getMessage());
    }
    //echo "Connected to SQL Server\n";
    //echo "Connected to Oracle Server\n";  
?>