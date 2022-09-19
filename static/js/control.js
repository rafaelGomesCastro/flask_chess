// Controller keys
const UP    = "ArrowUp";
const DOWN  = "ArrowDown";
const LEFT  = "ArrowLeft";
const RIGHT = "ArrowRight";
const OK    = "Enter";
const ST    = " ";

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

function calc_move() {
	for (var i = 0; i < possible_moves.length && possible_moves[i] != ''; ++i) {
		var n = possible_moves[i];
		var id = "possible_" + (n).toString();
		document.getElementById(id).src = "";
	}

	fetch('/calc_move', {
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
				for (var i = 0; i < possible_moves.length && possible_moves[i] != ''; ++i) {
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

function stockfish_move() {
	fetch('/stockfish_move', {
		headers: {
			'Content-Type': 'application/json'
		},
		method: 'POST'
	})
	.then(response => response.json())
	.then(function(json) {
		if (json.piece) {
			var id_orig = "piece_" + json.piece.split(',')[0];
			var id_dest = "piece_" + json.piece.split(',')[1];
			document.getElementById(id_dest).src = document.getElementById(id_orig).src;
			document.getElementById(id_orig).src = "";
		}
		if (json.castle) {
			var id_orig = "piece_" + json.castle.split(',')[0];
			var id_dest = "piece_" + json.castle.split(',')[1];
			document.getElementById(id_dest).src = document.getElementById(id_orig).src;
			document.getElementById(id_orig).src = "";
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
	possible_moves = [];

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
	.then(response => response.json())
	.then(function(json) {
		if (json.piece) {
			var id_rook = "piece_" + json.piece.split(',')[0];
			var id_dest = "piece_" + json.piece.split(',')[1];
			document.getElementById(id_dest).src = document.getElementById(id_rook).src;
			document.getElementById(id_rook).src = "";
		}
	})
	.catch(function(error) {
		console.log(error);
	});
}

function main() {
	document.addEventListener("keydown", function(inEvent) {
		var keyCode = inEvent.key || inEvent.keyCode;
		
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
			var has_piece = document.getElementById(id).src.includes('white');

			id = "possible_" + (sel_idx).toString();
			var has_possible = document.getElementById(id).src.includes('.png');

			if (has_piece) {
				sel_piece = sel_idx;
				calc_move();
			}
			else if (has_possible && sel_piece) {
				move_piece();
				sel_piece = null;
				stockfish_move();
			}
			else {
				for (var i = 0; i < possible_moves.length; ++i) {
					var n = possible_moves[i];
					var id = "possible_" + (n).toString();
					document.getElementById(id).src = "";
				}
			}
		}
		else if (keyCode == ST) {
			stockfish_move();
		}
	});
}

main();