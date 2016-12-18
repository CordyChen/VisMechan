$(document).ready(function () { 
    var bar = $('#bar1'); 
    var percent = $('#percent1'); 
    var progress = $("#progress1"); 
    var files = $("#files1"); 
    var btn = $("#btn1 span"); 
	var file_name = '';
    $("#fileupload").wrap("<form id='myupload' action='.../PHP/File_upload.php' method='post' enctype='multipart/form-data'></form>"); 

    $("#fileupload").change(function(){ //选择文件 
        $("#myupload").ajaxSubmit({ 
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
	
	$("#sub_contour").click(function() {
		if (file_name == ''){
			alert("No File Uploaded!");
			}
		else{
            $.ajax({
				url: ".../PHP/Draw_Contour.php",
				type:"POST",
				data:{filename: file_name},
				dataType:"html",
				error: function(){
					alert('error loading xml doc.');
				},
				success: function(data) {
					//alert(data);
					$("#disp_2").html(data);
				}
			});
		}
		});
});
