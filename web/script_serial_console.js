view_container_create("gcode_Terminal")
var canvas = document.getElementById("canvas_gcode_Terminal"); //instancia controladora do Canvas
var ctx = canvas.getContext("2d"); //instancia do operador grafico 2d
ctx.beginPath();
ctx.lineWidth = "2";
ctx.strokeStyle = "white";
ctx.rect(2, 105, 496, 18);

async function update_client() {
    let value = await eel.update_client()();
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
var UpdateClientRoutine = setInterval(update_client, 5);


