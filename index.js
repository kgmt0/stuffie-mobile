function intercalate(delim, array)
{
	return array.reduce((p, x) => p+delim+x, array.shift());
}

function rpc(func, args)
{
	var debug = document.getElementById("debug");
	var args_str = (args && args.length > 0)?intercalate("-", args):"";

	debug.value +=	"/"+func+"/"+args_str+"\n";
}

function handle_game_area_button(e)
{
	document.getElementById("game-area").removeChild(e.currentTarget);
}

function handle_dir_button(e)
{
	var game_area = document.getElementById("game-area");
	var new_button = document.createElement("button");

	new_button.innerText = e.currentTarget.innerText;
	new_button.addEventListener("click", handle_game_area_button);
	game_area.appendChild(new_button);
}

function handle_start_button()
{
	var buttons = Array.from(document.getElementById("game-area").children);

	rpc("load-commands", buttons.map(x => x.innerText.toLowerCase()));
	rpc("start");
}

function handle_stop_button()
{
	rpc("stop");
}

function handle_clear_button()
{
	var game_area = document.getElementById("game-area");

	while(game_area.hasChildNodes())
	{
		game_area.removeChild(game_area.firstChild);
	}

	rpc("load-commands");
}

function init()
{
	var elem_handler_dict =
	{
		"up-button":	handle_dir_button,
		"down-button":	handle_dir_button,
		"left-button":	handle_dir_button,
		"right-button": handle_dir_button,
		"start-button": handle_start_button,
		"stop-button":	handle_stop_button,
		"clear-button":	handle_clear_button
	};

	for(var i in elem_handler_dict)
	{
		var elem = document.getElementById(i);

		elem.addEventListener("click", elem_handler_dict[i]);
	}

	document.getElementById("debug").value = "";
}
