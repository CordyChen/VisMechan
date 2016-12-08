<?php
	$file_name = $_POST['filename'];
	$Send = 'upload_temp/'. $file_name;
	$result = exec('python Python/Draw_contour.py ' . $Send);
	echo str_replace("\\n"," ",substr($result, 1, -1));
	exit();
?>