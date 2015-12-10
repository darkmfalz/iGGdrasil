$(document).on('submit', '#parse', function(e){

	console.log('hi');
	document.getElementById("tree-container").innerHTML = "<div id='tree'></div>";
	if("".localeCompare($("#toparse").val()) == 0){
		drawParseEBNF();
	}
	else{
		drawParseGrammar();
	}
	$("#toparse").val("");

	e.preventDefault();
	return false;
});

function drawParseEBNF(){

	// create an array with nodes
	var nodes = new vis.DataSet([
	]);

	// create an array with edges
	var edges = new vis.DataSet([
	]);

	var threadid = $("#threadparent").val();

	console.log(threadid);

	$("#tree").addClass("loading");

	$.ajax({

		url: "/cgi-bin/server-parse-ebnf.py",

		data: {
			thread: threadid
		},

		type: "POST",

		dataType: "json",

		success: function(data){

			console.log(data);

			if(data.success == true){

				var count = 1;
				var queue = [];
				var idqueue = [];
				var queuelength = 0;

				queue.push(data.data);
				queuelength++;
				idqueue.push(count);
				nodes.add([{id: count, label: data.data.tag}]);
				count++;
				var currentid = 1;

				while(queuelength != 0){
					var current = queue.shift();
					queuelength--;
					var id = idqueue.shift();

					if(current.content != null){
						for(var i = 0; i < current.content.length; i++){
							queue.push(current.content[i]);
							queuelength++;
							idqueue.push(count);
							if(current.content[i].tag != null){
								console.log(current.content[i].tag);
								nodes.add([{id: count, label: current.content[i].tag}]);
							}
							else{
								console.log(current.content[i]);
								nodes.add([{id: count, label: current.content[i]}]);
							}
							edges.add([{from: id, to: count}]);
							count++;
						}
					}
					else if(current.tag != null){
						
						queue.push("\u03B5");
						queuelength++;
						idqueue.push(count);
						console.log("\u03B5");
						nodes.add([{id: count, label: "\u03B5"}]);
						edges.add([{from: id, to: count}]);
						count++;

					}
				}

				console.log(count);

				// create a network
				var container = document.getElementById('tree');

				// provide the data in the vis format
				var datum = {
					nodes: nodes,
					edges: edges
				};
				var options = {
					layout: {
						hierarchical: {
							sortMethod: 'directed',
						}
					},
					physics:{
						hierarchicalRepulsion: {
							nodeDistance: 150
						},
						stabilization: {
							iterations: 2500
						}
					},
					interaction:{
						dragNodes: false,
						dragView: true,
						zoomView: true,
						navigationButtons: true,
					},
					nodes:{
						color:{
							background: '#8b9dc3',
							border: '#637aad'
						},
						font:{
							color: '#FFFFFF'
						},
						scaling:{
							label:{
								enabled: true
							}
						}
					},
					edges:{
						smooth: true
					}
				};

				// initialize your network!
				var network = new vis.Network(container, datum, options);
				$("#tree").removeClass("loading");

			}
			else{
				//$("#tree").removeClass("loading");
				$("#tree").addClass("error");
				alert(data.message);
			}

		},

		error: function(){
			$("#tree").addClass("error");
			alert("500 Error: Your grammar isn't really a grammar.");
		}

	});

}

function drawParseGrammar(){

	// create an array with nodes
	var nodes = new vis.DataSet([
	]);

	// create an array with edges
	var edges = new vis.DataSet([
	]);

	var threadid = $("#threadparent").val();
	var input = $("#toparse").val();

	console.log(threadid);
	console.log(input);

	$("#tree").addClass("loading");

	$.ajax({

		url: "/cgi-bin/server-parse-grammar.py",

		data: {
			thread: threadid,
			value: input,
		},

		type: "POST",

		dataType: "json",

		success: function(data){

			console.log(data);

			if(data.success == true){

				var count = 1;
				var queue = [];
				var idqueue = [];
				var queuelength = 0;

				queue.push(data.data);
				queuelength++;
				idqueue.push(count);
				nodes.add([{id: count, label: data.data.tag}]);
				count++;
				var currentid = 1;

				while(queuelength != 0){
					var current = queue.shift();
					queuelength--;
					var id = idqueue.shift();

					if(current.content != null){
						for(var i = 0; i < current.content.length; i++){
							queue.push(current.content[i]);
							queuelength++;
							idqueue.push(count);
							if(current.content[i].tag != null){
								console.log(current.content[i].tag);
								nodes.add([{id: count, label: current.content[i].tag}]);
							}
							else{
								console.log(current.content[i]);
								nodes.add([{id: count, label: current.content[i]}]);
							}
							edges.add([{from: id, to: count}]);
							count++;
						}
					}
					else if(current.tag != null){
						
						queue.push("\u03B5");
						queuelength++;
						idqueue.push(count);
						console.log("\u03B5");
						nodes.add([{id: count, label: "\u03B5"}]);
						edges.add([{from: id, to: count}]);
						count++;

					}
				}

				console.log(count);

				// create a network
				var container = document.getElementById('tree');

				// provide the data in the vis format
				var datum = {
					nodes: nodes,
					edges: edges
				};
				var options = {
					layout: {
						hierarchical: {
							sortMethod: 'directed',
						}
					},
					physics:{
						hierarchicalRepulsion: {
							nodeDistance: 150
						},
						stabilization: {
							iterations: 2500
						}
					},
					interaction:{
						dragNodes: false,
						dragView: true,
						zoomView: true,
						navigationButtons: true,
					},
					nodes:{
						color:{
							background: '#8b9dc3',
							border: '#637aad'
						},
						font:{
							color: '#FFFFFF'
						},
						scaling:{
							label:{
								enabled: true
							}
						}
					},
					edges:{
						smooth: true
					}
				};

				// initialize your network!
				var network = new vis.Network(container, datum, options);
				$("#tree").removeClass("loading");

			}
			else{
				//$("#tree").removeClass("loading");
				$("#tree").addClass("error");
				alert(data.message);
			}

		},

		error: function(){
			$("#tree").addClass("error");
			alert("500 Error: Your grammar isn't really a grammar.");
		}

	});

}