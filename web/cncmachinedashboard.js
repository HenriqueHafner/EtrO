
var canvas = document.getElementById("canvasCNC"); //instancia controladora do Canvas
var ctx = canvas.getContext("2d"); //instancia do operador grafico 2d

async function UpdateClient() {
	//ctx1.clearRect(0,0,259,194);
    let value = await eel.UpdateClient()();
	ctx.fillStyle = '#808080'; //define estilo do que vai ser desenhado
	ctx.fillRect(0, 0, canvas.width, canvas.height); //Limpar area a ser desenhada
	ctx.fillStyle = '#ffffff'; //cor do texto
	ctx.font = '20px serif'; // formatting text
	
	var linecount = 1;
	for (var i in value) {
		ctx.fillText(value[i],10,linecount*20);
		linecount ++
	}
	
	//draw_1();
	//console.log('ClientUpdated #'+ClientUpdates);
	}

var UpdateClientRoutine = setInterval(UpdateClient, 5);
//clearInterval(UpdateClientRoutine)


console.log('cncmachinedashboard.js running.');


