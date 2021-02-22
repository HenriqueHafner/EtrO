var canvas_gcode_terminal = document.createElement("CANVAS");
canvas_gcode_terminal.id = "canvasCNC"
canvas_gcode_terminal.width = 500;
canvas_gcode_terminal.height =230;
document.body.appendChild(canvas_gcode_terminal)

function canvas_create(canvas_idtoset) {
    var canvas_toadd = document.createElement("CANVAS");
    canvas_toadd.id = canvas_idtoset
    canvas_toadd.width = 500;
    canvas_toadd.height =240;
    var ctx_canvas_toadd = canvas_toadd.getContext("2d");
    ctx_canvas_toadd.fillText(canvas_idtoset,10,20);
    document.body.appendChild(canvas_toadd)
}

var canvas = document.getElementById("canvasCNC"); //instancia controladora do Canvas
var ctx = canvas.getContext("2d"); //instancia do operador grafico 2d
ctx.beginPath();
ctx.lineWidth = "2";
ctx.strokeStyle = "white";
ctx.rect(2, 105, 496, 18);

async function UpdateClient() {
    let value = await eel.UpdateClient()();
	ctx.fillStyle = '#808080'; //define estilo do que vai ser desenhado
	ctx.fillRect(0, 0, canvas.width, canvas.height); //Limpar area a ser desenhada
	ctx.fillStyle = '#ffffff'; //cor do texto
	ctx.font = '20px serif'; // formatting text
	
	var linecount = 1;
	for (var i in value) {
		ctx.fillText(value[i],10,linecount*20);
		linecount ++
		

    ctx.stroke();
	}
}
var UpdateClientRoutine = setInterval(UpdateClient, 5);
//clearInterval(UpdateClientRoutine)


console.log('cncmachinedashboard.js running.');


