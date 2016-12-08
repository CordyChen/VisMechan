<?php
	$FS_data = $_POST['data_3D'];

   	$Send = implode(',',$FS_data);
    $result_str = substr(exec('python Python/Draw_3D.py ' . $Send), 2, -2);
    $result_li = explode('], [', $result_str);
    $result = array();
    for($i = 0; $i < 15; $i++) {
    	$list = explode(',', $result_li[$i]);
    	for($j = 0; $j < 3; $j++) {
    		$list[$j] = floatval($list[$j]);
    	}
    	$result[$i] = $list;
    }
    // $myfile = fopen('tt.txt', 'w');
    // fwrite($myfile, implode(',', $result));
    echo json_encode($result);
    exit();
?>