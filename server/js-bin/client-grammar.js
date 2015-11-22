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

				url: "/cgi-bin/feed.py",

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

function titleinit(){

	$("#titlegrammar").val("Title");
	$("#titlegrammar").css("color", "gray");

}

function grammarinit(){

	$("#grammar").val("Enter your grammar here.");
	$("#grammar").css("color", "gray");

}

titleinit();
grammarinit();

$("#grammartitle").focus(function(){

	if("Title".localeCompare($("#grammartitle").val()) == 0){

		$("#grammartitle").val("");
		$("#grammartitle").css("color", "black");

	}
	
});

$("#grammartitle").focusout(function(){

	if("".localeCompare($("#grammartitle").val()) == 0){

		titleinit();

	}

});

$("#grammar").focus(function(){

	if("Enter your grammar here.".localeCompare($("#grammar").val()) == 0){

		$("#grammar").val("");
		$("#grammar").css("color", "black");

	}
	
});

$("#grammar").focusout(function(){

	if("".localeCompare($("#grammar").val()) == 0){

		grammarinit();

	}

});