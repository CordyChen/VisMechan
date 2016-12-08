<?php
	$FS_data = $_POST['FS_data'];

   	$Send = implode(',',$FS_data);
    $result = exec('python Python/Draw_Hoek.py ' . $Send);
    // $myfile = fopen('tt.txt', 'w');
    // fwrite($myfile, $Send);
    echo $result;
    exit();
?>