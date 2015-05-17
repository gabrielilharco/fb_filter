$(document).ready(
	function (){
		
		var currentThemes = [];

		chrome.storage.local.get(null,function (obj){
			currentThemes = obj;
	        //console.log(currentThemes);

			var sendPosts = function() {
				// for each post

				$("._5pbx.userContent").each(function() {
			    	if (currentThemes != [] && $(this).find('.marked').length == 0) {
			     		//mark post
			     		$(this).append($("<a class='marked'></a>"));
			     		
			     		//var POSTID = JSON.parse($(this).parent().attr("data-gt")).fbstory;
						//console.log(POSTID);
						
						var post = $(this);
			     		var TEXT_CONTENT = $(this).text();
			     		
			     		// post to server
			     		if (TEXT_CONTENT && TEXT_CONTENT != "") {
			     			TEXT_CONTENT = TEXT_CONTENT.replace(/[^a-z0-9 ,.?!]/ig, '');
			     			//console.log("*"+TEXT_CONTENT+"*");
			     			
			     			if (currentThemes != null) {

				     			var aux = {};
				     			aux["text_content"] = TEXT_CONTENT;

				     			var i = 0;
				     			for (var key in currentThemes) {
				     			  //console.log(key + "*****");
								  if (currentThemes.hasOwnProperty(key)) {
								    aux[String(i)] = currentThemes[key];
								  }
								  i++;
								}

								aux["size"] = String(i);
								//console.log(aux);
					     		$.post("https://big-formula-94718.appspot.com/", aux ,
									function(data){
										
										//console.log(data.filtered);
										if (data.filtered == "1") {
											console.log("entrou!!");
											post.parent().parent().remove();
										}
									});
			     			}
			     			
			     		}
					}
					
				});
				setTimeout(sendPosts, 100);
			};

			sendPosts();

		});	

		
	});