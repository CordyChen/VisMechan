$(document).ready(function () { 
    var bar = $('#bar2'); 
    var percent = $('#percent2'); 
    var progress = $("#progress2"); 
    var files = $("#files2"); 
    var btn = $("#btn2 span"); 
	var file_name = '';
    $("#fileupload2").wrap("<form id='myupload2' action='PHP/File_upload.php' method='post' enctype='multipart/form-data'></form>"); 
    $("#fileupload2").change(function(){ //选择文件 
        $("#myupload2").ajaxSubmit({ 
            dataType:  'json', //数据格式为json 
            beforeSend: function() { //开始上传 
                progress.show(); //显示进度条 
                var percentVal = '0%'; //开始进度为0% 
                bar.width(percentVal); //进度条的宽度 
                percent.html(percentVal); //显示进度为0% 
                btn.html("上传中..."); //上传按钮显示上传中 
            }, 
            uploadProgress: function(event, position, total, percentComplete) { 
                var percentVal = percentComplete + '%'; //获得进度 
                bar.width(percentVal); //上传进度条宽度变宽 
                percent.html(percentVal); //显示上传进度百分比 
            }, 
            success: function(data) { //成功 
                //获得后台返回的json数据，显示文件名，大小，以及删除按钮 
                files.html("<b>"+data.name+"("+data.size+"k)</b>"); 
				file_name = data.files;
                btn.html("添加附件"); //上传按钮还原 
            }, 
            error:function(xhr){ //上传失败 
                btn.html("上传失败"); 
                bar.width('0'); 
                files.html(xhr.responseText); //返回失败信息 
            } 
        }); 
    });  
	
	$("#sub_joints_contour").click(function() {
		if (file_name == ''){
			alert("No File Uploaded!");
			}
		else{
            $.ajax({
				url: "PHP/Draw_Joints.php",
				type:"POST",
				data:{filename: file_name, method: "contour"},
				dataType:"html",
				error: function(){
					alert('error loading xml doc.');
				},
				success: function(data) {
					//alert(data);
					$("#disp_3").html(data);
				}
			});
		}
	});
	
	$("#sub_rose").click(function(){
		if (file_name == ''){
			alert("No File Uploaded!");
			}
		else{
            $.ajax({
				url: "PHP/Draw_Joints.php",
				type:"POST",
				data:{filename: file_name, method: "rose"},
				dataType:"html",
				error: function(){
					alert('error loading xml doc.');
				},
				success: function(data) {
					//alert(data);
					$("#disp_3").html(data);
				}
			});
		}
	});
	
	$("#sub_density").click(function(){
		if (file_name == ''){
			alert("No File Uploaded!");
			}
		else{
            $.ajax({
				url: "PHP/Draw_Joints.php",
				type:"POST",
				data:{filename: file_name, method: "density"},
				dataType:"html",
				error: function(){
					alert('error loading xml doc.');
				},
				success: function(data) {
					//alert(data);
					$("#disp_3p").html(data);
				}
			});
		}
	});
});