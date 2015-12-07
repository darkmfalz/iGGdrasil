$(document).on('submit', '#parse', function(e){

	console.log('hi');
	document.getElementById("tree-container").innerHTML = "<div id='tree'></div>";
	if("".localeCompare($("#toparse").val()) == 0){
		drawParseEBNF();
	}
	$("#toparse").val("");

	e.preventDefault();
	return false;
});

function drawParseEBNF(){

	/*// create an array with nodes
	var nodes = new vis.DataSet([
		{id: 1, label: 'S'},
		{id: 2, label: '"-"'},
		{id: 3, label: 'FN'},
		{id: 4, label: 'DL'},
		{id: 5, label: '"."'},
		{id: 6, label: 'DL'},
		{id: 7, label: 'D'},
		{id: 8, label: '"3"'},
		{id: 9, label: 'D'},
		{id: 10, label: 'DL'},
		{id: 11, label: '"1"'},
		{id: 12, label: 'D'},
		{id: 13, label: '"4"'}
	]);

	// create an array with edges
	var edges = new vis.DataSet([
		{from: 1, to: 2},
		{from: 1, to: 3},
		{from: 3, to: 4},
		{from: 3, to: 5},
		{from: 3, to: 6},
		{from: 4, to: 7},
		{from: 7, to: 8},
		{from: 6, to: 9},
		{from: 6, to: 10},
		{from: 9, to: 11},
		{from: 10, to: 12},
		{from: 12, to: 13},
	]);*/

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

			var count = 1;
			var queue = [];
			var idqueue = [];
			var queuelength = 0;

			queue.push(data);
			queuelength++;
			idqueue.push(count);
			nodes.add([{id: count, label: data.tag}]);
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
					smooth: false
				}
			};

			// initialize your network!
			var network = new vis.Network(container, datum, options);
			$("#tree").removeClass("loading");

		}

	});

}