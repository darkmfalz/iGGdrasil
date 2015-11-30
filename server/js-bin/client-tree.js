$(document).on('submit', '#parse', function(e){

	console.log('hi');
	document.getElementById("tree-container").innerHTML = "<div id='tree'></div>";
	draw();

	e.preventDefault();
	return false;
});

function draw(){
	// create an array with nodes
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
	]);

	// create a network
	var container = document.getElementById('tree');

	// provide the data in the vis format
	var data = {
		nodes: nodes,
		edges: edges
	};
	var options = {
		layout: {
			hierarchical: {sortMethod: 'directed',}
		},
		physics:{
			enabled: false,
		},
		interaction:{
			dragNodes: false,
			dragView: false,
		},
		nodes:{
			color:{
				background: '#8b9dc3',
				border: '#637aad'
			},
			font:{
				color: '#FFFFFF'
			}
		},
	};

	// initialize your network!
	var network = new vis.Network(container, data, options);
}