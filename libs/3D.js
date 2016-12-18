$(document).ready(function(e) {

//-----------------------------------------------------------------------------------------------------------------------
		//Load the scene and camera of the Three.js object
		var camera, scene, renderer, geometry_slp, geometry_wdg, mesh_slp, mesh_wdg, material_slp, material_wdg;
		var disp = document.getElementById('disp_4');
		init();
		animate();
		
		function init() {
			var init_data = [[0,0,0],[-16,-25,30],[-12,31,32],[-26,-2,13],[-28,-23,33],[-40,17,37],[-94,-8,47],[-7,-85,0],[-101,-76,0],[-100,-76,16],[-20,-83,28],[7,87,0],[-8,88,35],[-85,95,22],[-86,96,0]];
			
			renderer = new THREE.WebGLRenderer( { antialias: true } );
			// renderer.setPixelRatio( window.devicePixelRatio );
			renderer.setSize( window.innerWidth * 0.7, window.innerHeight * 0.7);
			// document.body.appendChild( renderer.domElement );
			// renderer.setSize(900, 600);
			disp.appendChild( renderer.domElement );

			
			camera = new THREE.PerspectiveCamera( 40, window.innerWidth / window.innerHeight, 1, 1000 );
			// camera = new THREE.PerspectiveCamera( 40, disp.width / disp.height, 1, 1000 );
			scene = new THREE.Scene();
			camera.position.set( 0, 200, 200 );
			scene.add( camera );
			
			controls = new THREE.OrbitControls(camera, renderer.domElement);
			controls.minDistance = 50;
			controls.maxDistance = 600;
			controls.maxPolarAngle = Math.PI;
			
			scene.add( new THREE.AmbientLight( 0x222222 ) );

			camera.add( new THREE.PointLight( 0xffffff, 1 ) );
			
			//scene.add( new THREE.AmbientLight( 0x888888, 0.2 ) );
			
			scene.add( new THREE.AxisHelper( 20 ) );

			// create the ground plane
	        var planeGeometry = new THREE.PlaneGeometry(300, 200, 1, 1);
	        var planeMaterial = new THREE.MeshLambertMaterial({color: 0xffffff, side: THREE.DoubleSide});
	        var plane = new THREE.Mesh(planeGeometry, planeMaterial);
	        plane.receiveShadow = true;

	        // rotate and position the plane
        	plane.rotation.x = -0.5 * Math.PI;

	        // add the plane to the scene
	        scene.add(plane);
			
			geometry_slp = new THREE.Geometry();
			geometry_wdg = new THREE.Geometry();
			for (var i = 0; i < 15; i++) {
				geometry_slp.vertices.push(new THREE.Vector3(init_data[i][1], init_data[i][2], init_data[i][0]));
				if (i < 6) {
					geometry_wdg.vertices.push(new THREE.Vector3(init_data[i][1], init_data[i][2], init_data[i][0]));
				}
			}
			
			//To draw the faces of the slope
			geometry_slp.faces.push(new THREE.Face3(0, 10, 7));
			geometry_slp.faces.push(new THREE.Face3(0, 1, 10));
			geometry_slp.faces.push(new THREE.Face3(0, 12, 2));
			geometry_slp.faces.push(new THREE.Face3(0, 11, 12));
			geometry_slp.faces.push(new THREE.Face3(7, 8, 11));
			geometry_slp.faces.push(new THREE.Face3(11, 8, 14));
			geometry_slp.faces.push(new THREE.Face3(8, 7, 10));
			geometry_slp.faces.push(new THREE.Face3(8, 10, 9));
			geometry_slp.faces.push(new THREE.Face3(11, 14, 12));
			geometry_slp.faces.push(new THREE.Face3(13, 12, 14));
			geometry_slp.faces.push(new THREE.Face3(8, 9, 14));
			geometry_slp.faces.push(new THREE.Face3(9, 13, 14));
			geometry_slp.faces.push(new THREE.Face3(9, 10, 1));
			geometry_slp.faces.push(new THREE.Face3(1, 4, 9));
			geometry_slp.faces.push(new THREE.Face3(4, 5, 9));
			geometry_slp.faces.push(new THREE.Face3(9, 5, 13));
			geometry_slp.faces.push(new THREE.Face3(5, 2, 13));
			geometry_slp.faces.push(new THREE.Face3(2, 12, 13));
			geometry_slp.faces.push(new THREE.Face3(3, 5, 4));
			geometry_slp.faces.push(new THREE.Face3(0, 4, 1));
			geometry_slp.faces.push(new THREE.Face3(0, 3, 4));
			geometry_slp.faces.push(new THREE.Face3(0, 2, 5));
			geometry_slp.faces.push(new THREE.Face3(0, 5, 3));
			geometry_slp.computeBoundingSphere();
			geometry_slp.computeFaceNormals();
			
			//To draw the faces of the wedge
			geometry_wdg.faces.push(new THREE.Face3(0, 1, 4));
			geometry_wdg.faces.push(new THREE.Face3(0, 4, 3));
			geometry_wdg.faces.push(new THREE.Face3(0, 5, 2));
			geometry_wdg.faces.push(new THREE.Face3(0, 3, 5));
			geometry_wdg.faces.push(new THREE.Face3(0, 2, 1));
			geometry_wdg.faces.push(new THREE.Face3(4, 5, 3));
			geometry_wdg.faces.push(new THREE.Face3(2, 5, 4));
			geometry_wdg.faces.push(new THREE.Face3(1, 2, 4));
			geometry_wdg.computeBoundingSphere();
			geometry_wdg.computeFaceNormals();
			
			//To define the material of the slope and the wedge
			material_slp = new THREE.MeshLambertMaterial({
					color: 0xffffff,
					opacity: 0.5
			});
			material_wdg = new THREE.MeshPhongMaterial({
					color: 0xcd2626,
					opacity: 0.5
			});
			
			//Create the mesh objects
			mesh_slp = new THREE.Mesh(geometry_slp, material_slp);
			mesh_wdg = new THREE.Mesh(geometry_wdg, material_wdg);
			
			scene.add(mesh_slp);
			scene.add(mesh_wdg);
		
			window.addEventListener( 'resize', onWindowResize, false );
		}
		
		function onWindowResize() {
			camera.aspect = window.innerWidth / window.innerHeight;
			camera.updateProjectionMatrix();
			renderer.setSize( window.innerWidth * 0.7, window.innerHeight *0.7);
		}

		var step = 0;
		function animate() {
			if(step <= 0.004){
				step += 0.00001;
				mesh_wdg.position.x += (-step)*mesh_slp.geometry.vertices[3].x;
				mesh_wdg.position.y += (-step)*mesh_slp.geometry.vertices[3].y;
				mesh_wdg.position.z += (-step)*mesh_slp.geometry.vertices[3].z;
			}
			requestAnimationFrame( animate );
			render();
		}
		
		function render() {
			renderer.render( scene, camera );
		}


//-----------------------------------------------------------------------------------------------
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
			var mydata_2 = [];
			var Point;
			for(var i = 0; i < 11; i++) {
				mydata_2[i] = mydata[i];
			}
			mydata_2[11] = mydata[17];
			$.ajax({
				url:".../PHP/Draw_3D.php",
				type:"POST",
				data: {data_3D: mydata_2},
				dataType:"json",
				error: function(){
					alert('error loading xml doc.');
				},
				success: function(data) {
					//alert(data[2][2]);
					Point = data;
					var vertices_slp = [];
					var vertices_wdg = [];
					for (var i = 0; i < 15; i++) {
						vertices_slp.push(new THREE.Vector3(Point[i][1], Point[i][2], Point[i][0]));
						if (i < 6) {
							vertices_wdg.push(new THREE.Vector3(Point[i][1], Point[i][2], Point[i][0]));
						}
					}

					mesh_slp.geometry.vertices = vertices_slp;
					mesh_slp.geometry.verticesNeedUpdate = true;
					mesh_slp.geometry.computeFaceNormals();
					mesh_slp.geometry.elementsNeedUpdate = true;
					
					mesh_wdg.geometry.vertices = vertices_wdg;
					mesh_wdg.geometry.verticesNeedUpdate = true;
					mesh_wdg.geometry.computeFaceNormals();
					mesh_wdg.geometry.elementsNeedUpdate = true;

					mesh_wdg.position.x = 0;
					mesh_wdg.position.y = 0;
					mesh_wdg.position.z = 0;
					step = 0;
				}
			});
		});

});