<?php
    $filename = $_FILES['myfile']['name']; 
    $filesize = $_FILES['myfile']['size']; 
    if ($filename != "") { 
        $type = strstr($filename, '.'); //限制上传格式 
        if ($type != ".txt") { 
            echo 'Wrong File Type!'; 
            exit; 
        } 
        $files = date("YmdHis"). $filename; //命名文件名称 
        //上传路径 
        $file_path = "upload_temp/". $files; 
        move_uploaded_file($_FILES['myfile']['tmp_name'], $file_path); 
    } 
    $size = round($filesize/1024,2); //转换成kb 
    $arr = array( 
        'name'=>$filename, 
        'files'=>$files, 
        'size'=>$size
    ); 
    echo json_encode($arr); //输出json数据 
?>