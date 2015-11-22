$(document).on('submit', '#login', function(e){

	//get the username and password from the textbox
	var username = $("#username").val();
	var password = $("#password").val();

	if (document.getElementById('persist_box').checked) {
		var checked = "TRUE";
	} 
	else {
		var checked = "FALSE";
	}
	console.log(username);
	console.log(checked);

	$.ajax({

		url: "/cgi-bin/server-login.py",

		data: {
			requested_username: username,
			requested_password: password,
			keep_loggedin: checked
		},

		type: "POST",

		dataType: "json",

		success: function(data){

			console.log("Successfully logged in as:");
			console.log(data.username);
			$("#username").val("");
			$("#password").val("");
			window.location.assign("/users/".concat(data.username));

		},

		error: function(){

			alert("There was a problem: invalid username/password combination.");
			$("#username").val("");
			$("#password").val("");

		}


	});

	e.preventDefault();

	return false;

});

$(document).on('submit', '#logout', function(e){
			
	$.ajax({

		url: "/cgi-bin/server-logout.py",

		data: {
		},

		type: "POST",

		datatype: "json",

		success: function(data){

			window.location.assign("/signup");

		},

		error: function(){

			console.log("Error logging out.");

		}

	});

	e.preventDefault();
	return false;
});