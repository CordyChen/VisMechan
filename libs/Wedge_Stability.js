$(document).ready(function() {
		//When click on the Calculate botton
        $("#sub-FS").click(function(){
			var mydata = [];
			var dip1 = $("#dip-ein").val(); mydata[0] = dip1;
			var dia1 = $("#dia-ein").val(); mydata[1] = dia1;
			var dip2 = $("#dip-zwei").val(); mydata[2] = dip2;
			var dia2 = $("#dia-zwei").val(); mydata[3] = dia1;
			var dipt = $("#dip-top").val(); mydata[4] = dipt;
			var diat = $("#dia-top").val(); mydata[5] = diat;
			var dips = $("#dip-slope").val(); mydata[6] = dips;
			var dias = $("#dia-slope").val(); mydata[7] = dias;
			var dipc = $("#dip-crack").val(); mydata[8] = dipc;
			var diac = $("#dia-crack").val(); mydata[9] = diac;
			var hslp = $("#slope-height").val(); mydata[10] = hslp;
			var gamma = $("#gamma").val(); mydata[11] = gamma;
			var gammawater = $("#gamma-water").val(); mydata[12] = gammawater;
			var C1 = $("#C1").val(); mydata[13] = C1;
			var fi1 = $("#fi1").val(); mydata[14] = fi1;
			var C2 = $("#C2").val(); mydata[15] = C2;
			var fi2 = $("#fi2").val(); mydata[16] = fi2;
			var Lcrack = $("#L-crack").val(); mydata[17] = Lcrack;
			var overhanged, water;
			if($("#overhanged").prop("checked") == true) {
				overhanged = -1;
			}
			else {
				overhanged = 1;
			}
			if($("#water").prop("checked") == true) {
				water = 1;
			}
			else {
				water = 0;
			}
			mydata[18] = overhanged;
			mydata[19] = water;
			var mark = 0;
			for(var i in mydata) {
				if(i == null) {
					mark = 1;
					alert("Form not completed!");
					break;
				}
			}
			if (mark == 0) {
				$.ajax({
					url: "PHP/FS.php",
					type: "POST",
					data: {FS_data: mydata},
					dataType:"html",
					error: function(){
						alert('error loading xml doc.');
					},
					success: function(data) {
						//alert(data);
						$("#FS-re").html(data);
					}
				});
								
			}
		});
    });