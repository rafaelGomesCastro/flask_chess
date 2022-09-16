// Controller keys
const UP    = "ArrowUp";
const DOWN  = "ArrowDown";
const LEFT  = "ArrowLeft";
const RIGHT = "ArrowRight";
const OK    = "Enter";

// Colors
const WHITE = 0;
const BLACK = 1;

var sel_idx      = 35;
var sel_piece    = null;
var sel_img      = '/static/marker.png';
var possible_img = '/static/possible_square.png';
var right_player = WHITE;

var possible_moves = [];

window.onload = init;

function init() {
	var id = "marker_" + (sel_idx).toString();
	document.getElementById(id).src = sel_img;
}

function calc_movement() {
	for (var i = 0; i < possible_moves.length; ++i) {
		var n = possible_moves[i];
		var id = "possible_" + (n).toString();
		document.getElementById(id).src = "";
	}

	console.log(sel_idx);

	fetch('/move', {
		headers: {
			'Content-Type': 'application/json'
		},
		method: 'POST',
		body: JSON.stringify({
			'sel_idx': sel_idx
		})
	})
	.then(function(response){
		if (response.ok) {
			response.json().then(function(response) {
				var json = JSON.parse(JSON.stringify(response));
				possible_moves = json['possible_moves'].split(',');
				for (var i = 0; i < possible_moves.length; ++i) {
					var n = possible_moves[i];
					var id = "possible_" + (n).toString();
					document.getElementById(id).src = possible_img;
				}
			});
		}
		else {
			throw Error('Something went wrong ):');
		}
	})
	.catch(function(error) {
		console.log(error);
	});
}

function move_piece() {
	var id_piece = "piece_" + (sel_piece).toString();
	var id_idx   = "piece_" + (sel_idx).toString();
	document.getElementById(id_idx).src = document.getElementById(id_piece).src;
	document.getElementById(id_piece).src = "";

	for (var i = 0; i < possible_moves.length; ++i) {
		var n  = possible_moves[i];
		var id = "possible_" + (n).toString();
		document.getElementById(id).src = "";
	}

	right_player = (right_player + 1) % 2;

	fetch('/complete_move', {
		headers: {
			'Content-Type': 'application/json'
		},
		method: 'POST',
		body: JSON.stringify({
			'sel_idx': sel_idx,
			'sel_piece': sel_piece
		})
	})
	.then(function(response){
		if (response.ok) {
			console.log("Move completed!");
		}
		else {
			throw Error('Something went wrong ):');
		}
	})
	.catch(function(error) {
		console.log(error);
	});
}

function main() {
	document.addEventListener("keydown", function(inEvent) {
		var keyCode = inEvent.key || inEvent.keyCode;
		// var idx     = board.select_idx;
		// var id      = "marker_" + (idx).toString();
		// document.getElementById(id).src = '';
		
		if      (keyCode == UP && Math.floor(sel_idx / 8) - 1 > -1) {
			var id = "marker_" + (sel_idx).toString();
			document.getElementById(id).src = '';
			sel_idx -= 8
			var id = "marker_" + (sel_idx).toString();
			document.getElementById(id).src = sel_img;
		}
		else if (keyCode == DOWN && Math.floor(sel_idx / 8) + 1 < 8) {
			var id = "marker_" + (sel_idx).toString();
			document.getElementById(id).src = '';
			sel_idx += 8
			var id = "marker_" + (sel_idx).toString();
			document.getElementById(id).src = sel_img;
		}            
		else if (keyCode == LEFT && (sel_idx % 8) + 1 < 8) {
			var id = "marker_" + (sel_idx).toString();
			document.getElementById(id).src = '';
			sel_idx += 1
			var id = "marker_" + (sel_idx).toString();
			document.getElementById(id).src = sel_img;
		}            
		else if (keyCode == RIGHT && (sel_idx % 8) - 1 > -1) {
			var id = "marker_" + (sel_idx).toString();
			document.getElementById(id).src = '';
			sel_idx -= 1
			var id = "marker_" + (sel_idx).toString();
			document.getElementById(id).src = sel_img;
		}            
		else if (keyCode == OK) {
			var id = "piece_" + (sel_idx).toString();
			var has_piece = document.getElementById(id).src != "";

			var player = -1;
			if      (has_piece && document.getElementById(id).src.includes("white")) player = WHITE;
			else if (has_piece && document.getElementById(id).src.includes("black")) player = BLACK;

			id = "possible_" + (sel_idx).toString();
			var has_possible = document.getElementById(id).src != "";

			if (has_piece && player == right_player) {
				sel_piece = sel_idx;
				calc_movement();
			}
			else if (has_possible) {
				move_piece();
			}
			else {
				for (var i = 0; i < possible_moves.length; ++i) {
					var n = possible_moves[i];
					var id = "possible_" + (n).toString();
					document.getElementById(id).src = "";
				}
			}
		}
		
		// idx = board.select_idx;
		// id = "marker_" + (idx).toString();
		// document.getElementById(id).src = board.select_url_img;

	});
}

main();