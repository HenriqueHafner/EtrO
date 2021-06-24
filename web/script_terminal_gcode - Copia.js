var canvas_terminal_gcode = document.getElementById("canvas_terminal_gcode"); //instancia controladora do canvas_gcode
var ctx_terminal_gcode = canvas_terminal_gcode.getContext("2d"); //instancia do operador grafico 2d
ctx_terminal_gcode.beginPath();    
ctx_terminal_gcode.lineWidth = "2";
ctx_terminal_gcode.strokeStyle = "white";
ctx_terminal_gcode.rect(2, 105, 496, 18);

async function container_update_terminal_gcode() {
    let value = await eel.update_terminal_gcode()();
    ctx_terminal_gcode.fillStyle = '#808080'; //define estilo do que vai ser desenhado
    ctx_terminal_gcode.fillRect(0, 0, canvas_terminal_gcode.width, canvas_terminal_gcode.height); //Limpar area a ser desenhada
    ctx_terminal_gcode.fillStyle = '#ffffff'; //cor do texto
    ctx_terminal_gcode.font = '20px serif'; // formatting text   
    var linecount = 1;
    for (var i in value) {
        ctx_terminal_gcode.fillText(value[i],10,linecount*20);
        linecount ++
    ctx_terminal_gcode.stroke();
    }
}
var container_routine_update_terminal_gcode = setInterval(container_update_terminal_gcode, 200);
