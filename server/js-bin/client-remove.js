function removeGrammar(ithread, page){

	$.ajax({

		url: "/cgi-bin/server-remove-grammar.py",

		data: {
			thread: ithread
		},

		type: "POST",

		dataType: "json",

		success: function(data){

			console.log(data);

			$.ajax({

				url: "/cgi-bin/html-feed.py",

				data: {
				},

				type: "GET",

				dataType: "html",

				success: function(data){

					console.log(page);

					if(page == 0){

						$("#feed").html(data);

					}
					else if(page == 1){

						window.location.assign("/main");
						
					}
					else if(page == 2){

						$("#thread-grammars").html(data);
						
					}

				}
			});

		},

		error: function(){
			console.log("error");
		}

	});

}

function removeComment(ithread, page){

	$.ajax({

		url: "/cgi-bin/server-remove-comment.py",

		data: {
			thread: ithread
		},

		type: "POST",

		dataType: "json",

		success: function(data){

			console.log(data);

			$.ajax({

				url: "/cgi-bin/html-thread.py",

				data: {
					thread: ithread
				},

				type: "GET",

				dataType: "html",

				success: function(data){

					console.log(page);

					if(page == 1){

						$(".thread").html(data);
						
					}
					else if(page == 2){

						$("#thread-comments").html(data);
						
					}

				}
			});

		},

		error: function(){
			console.log("error");
		}

	});

}