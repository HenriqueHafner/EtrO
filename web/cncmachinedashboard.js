var canvas_test = document.createElement("CANVAS");
canvas_test.id = "canvas_test_id"
canvas_test.width = 500;
canvas_test.height =300;
var ctx_test = canvas_test.getContext("2d");
ctx_test.fillRect(0, 0, ctx_test.width, ctx_test.height);
ctx_test.fillText("CanvasTemplate",10,20);
document.body.appendChild(canvas_test)

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
	
	}

var UpdateClientRoutine = setInterval(UpdateClient, 5);
//clearInterval(UpdateClientRoutine)


console.log('cncmachinedashboard.js running.');


