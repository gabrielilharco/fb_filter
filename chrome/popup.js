$(document).ready(
	function (){
		
		$("#addButton").click(function() {
			//console.log("asudhuas");
			var theme = $("#addInput").val();
			$("#addInput").val("");
			var currentThemes = {};
			a = {};
			a[theme] = theme
			chrome.storage.local.set(a,function (){
			    console.log("Storage Succesful");
			});

			alert("Theme saved successfully!");
			str.push(theme);
			listIteracao(str);

		});

		var str = [];
		var themes = {};

		chrome.storage.local.get(null, function (obj){
			console.log(obj);
			themes = obj;
			for (var key in obj) {
				  //console.log(key + "*****");
			  if (obj.hasOwnProperty(key)) {
			  	str.push(obj[key]);
			  }
			}


			listIteracao(str);

		});
		
		function funcDelete(a) {
			str.splice(a,1);
			delete themes[$("#s".concat(a)).text()];
			listIteracao(str);
		}

		function listIteracao(a){
			if (a.length == 0)
				document.getElementById("vazio").innerHTML = "You have no filters yet."
			
			var aux = "";
			
			for (var i = 0; i < a.length; i++) {
				aux = aux.concat("<tr><td id = s\"".concat(i).concat("\">"));
				aux = aux.concat(a[i]);
				aux = aux.concat("</td><td>");
				aux = aux.concat("<button id =\"".concat(i).concat("\" class = \"btn btn-primary\">Remove</button>"));
				aux = aux.concat("</td></tr>");
			}
			//alert(aux);
			document.getElementById("tabela").innerHTML = aux;

		 	$(".btn.btn-primary").click(function(){
				//console.log("aaaa");
				//console.log($(this).attr("id"));
				funcDelete($(this).attr("id"));
			});
		    

		}


	});