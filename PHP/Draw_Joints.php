<?php
	$file_name = $_POST['filename'];
	$method = $_POST['method'];
	$Send = 'upload_temp/'. $file_name;
	if($method == 'contour') {
		$result = exec('python Python/Draw_Joints_Contour.py ' . $Send);
	}
	elseif($method == 'rose') {
		$result = exec('python Python/Draw_Joints_Rose.py ' . $Send);
	}
	else {
		$result = exec('python Python/Draw_Joints_Density.py ' . $Send);
	}
	$replace = str_replace("\\\"", "\"", substr($result, 1, -1));
	$search = array("\\\\n", "\\n");
	$replace = str_replace($search, " ", $replace);
	
	echo $replace;
	exit();
?>