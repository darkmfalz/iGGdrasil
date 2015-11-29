$(document).on('submit', '#createnewcomment', function(e){

	//get the comment from the textarea
	var comment = $("#comment").val();
	var parent = $("#commentparent").val();
	var ithread = $("#threadparent").val();

	console.log(ithread);

	$.ajax({

		url: "/cgi-bin/server-create-comment.py",

		data: {
			input_comment: comment,
			input_parent: parent,
			input_root: ithread
		},

		type: "POST",

		dataType: "json",

		success: function(){

			console.log("Successfully submitted comment.");
			$("#comment").val("");

			$.ajax({

				url: "/cgi-bin/html-thread.py",

				data: {
					thread: ithread
				},

				type: "GET",

				dataType: "html",

				success: function(data){

					console.log('hi');
					$(".mainpage").html(data);

				}
			});

		},

		error: function(){

			alert("There was a problem: not logged in.");
			console.log("Failed to submit comment.");
			$("#comment").val("");

		}
	});

	e.preventDefault();

	return false;

});