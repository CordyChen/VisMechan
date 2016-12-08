<?php
	$dip1 = $_POST['dip1'];
    $dia1 = $_POST['dia1'];
    $dip2 = $_POST['dip2'];
    $dia2 = $_POST['dia2'];
    $dips = $_POST['dips'];
    $dias = $_POST['dias'];

    if((!empty($dip1)&&!empty($dia1))||(!empty($dip2)&&!empty($dia2))||(!empty($dips)&&!empty($dias))) {
    	//$rtn =  "<button>".($dip1+$dia1+$dip2+$dia2)."</button>";
    	//echo $rtn;
    	$Send = strval($dip1).','.strval($dia1).','.strval($dip2).','.strval($dia2).','.strval($dips).','.strval($dias);
    	$result = exec('python Python/Draw_arc.py ' . $Send);
    	echo str_replace("\\n"," ",substr($result, 1, -1));
    	exit();
    }
?>