var canvas_gcode = document.getElementById("canvas_gcode_terminal"); //instancia controladora do canvas_gcode
var ctx_gcode = canvas_gcode.getContext("2d"); //instancia do operador grafico 2d
ctx_gcode.beginPath();    
ctx_gcode.lineWidth = "2";
ctx_gcode.strokeStyle = "white";
ctx_gcode.rect(2, 105, 496, 18);

async function update_container_terminal() {
    let value = await eel.update_container_gcode_terminal()();
    ctx_gcode.fillStyle = '#808080'; //define estilo do que vai ser desenhado
    ctx_gcode.fillRect(0, 0, canvas_gcode.width, canvas_gcode.height); //Limpar area a ser desenhada
    ctx_gcode.fillStyle = '#ffffff'; //cor do texto
    ctx_gcode.font = '20px serif'; // formatting text   
    var linecount = 1;
    for (var i in value) {
        ctx_gcode.fillText(value[i],10,linecount*20);
        linecount ++
    ctx_gcode.stroke();
    }
}
var routine_container_terminal = setInterval(update_container_terminal, 200);
