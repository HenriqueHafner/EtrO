div_main = document.getElementById("machine_dashboard");

//var canvas_gcode_terminal = document.createElement("CANVAS");
//canvas_gcode_terminal.id = "canvasCNC";
//canvas_gcode_terminal.width = 500;
//canvas_gcode_terminal.height =230;
//div_main.appendChild(canvas_gcode_terminal);

function view_container_create(element_idtoset) {
    
    var canvas_toadd = document.createElement("CANVAS");
    canvas_toadd.id = "canvas_".concat(element_idtoset);
    canvas_toadd.width = 500;
    canvas_toadd.height =230;
    
    div_to_add = document.createElement("DIV");
    div_to_add.id = "div_".concat(element_idtoset);
    title_para = document.createElement("p");
    title_text = document.createTextNode(element_idtoset);   
    title_para.appendChild(title_text);
    div_to_add.appendChild(title_para);
    
    div_to_add.appendChild(canvas_toadd);
    div_main.appendChild(div_to_add);
}

view_container_create("Gcode Terminal")
var canvas = document.getElementById("canvas_Gcode Terminal"); //instancia controladora do Canvas
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


