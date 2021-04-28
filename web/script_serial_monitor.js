// key name _serial
var canvas_serial = document.getElementById("canvas_serial_monitor"); //instancia controladora do Canvas
var ctx_serial = canvas_serial.getContext("2d"); //instancia do operador grafico 2d
ctx_serial.beginPath();
ctx_serial.lineWidth = "2";
ctx_serial.strokeStyle = "white";
ctx_serial.rect(2, 6, 496, 18);

async function update_container_serial() {
    let value = await eel.update_monitor_serial()();
	ctx_serial.fillStyle = '#808080'; //define estilo do que vai ser desenhado
	ctx_serial.fillRect(0, 0, canvas_serial.width, canvas_serial.height); //Limpar area a ser desenhada
	ctx_serial.fillStyle = '#ffffff'; //cor do texto
	ctx_serial.font = '20px serif'; // formatting text
	var linecount = 1;
	for (var i in value) {
		ctx_serial.fillText(value[i],10,linecount*20);
		linecount ++
    ctx_serial.stroke();
	}
}
var routine_container_serial = setInterval(update_container_serial, 200);


//orientar objeto aqui