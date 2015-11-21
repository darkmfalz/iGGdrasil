$(document).on('submit', '#createnewgrammar', function(e){

	//get the comment from the textarea
	var grammar = $("#grammar").val();

	$.ajax({

		url: "/cgi-bin/server-create-grammar.py",

		data: {
			input_grammar: grammar
		},

		type: "POST",

		dataType: "json",

		success: function(){

			console.log("Successfully submitted grammar.");
			$("#grammar").val("");

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