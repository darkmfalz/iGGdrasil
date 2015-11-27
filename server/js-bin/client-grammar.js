$(document).on('submit', '#createnewgrammar', function(e){

	//get the comment from the textarea
	var grammar = $("#grammar").val();
	var title = $("#grammartitle").val();

	$.ajax({

		url: "/cgi-bin/server-create-grammar.py",

		data: {
			input_grammar: grammar,
			input_title: title
		},

		type: "POST",

		dataType: "json",

		success: function(){

			console.log("Successfully submitted grammar.");
			$("#grammartitle").val("");
			$("#grammar").val("");

			$.ajax({

				url: "/cgi-bin/html-feed.py",

				data: {
				},

				type: "GET",

				dataType: "html",

				success: function(data){

					console.log('hi');
					$("#feed").html(data);

				}
			});

		},

		error: function(){

			alert("There was a problem: not logged in.");
			console.log("Failed to submit grammar.");
			$("#grammar").val("");

		}
	});

	e.preventDefault();

	return false;

});