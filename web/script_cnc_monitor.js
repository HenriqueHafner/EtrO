var canvas_cnc = document.getElementById("canvas_cnc_monitor"); //instancia controladora do canvas_cnc
var ctx_cnc = canvas_cnc.getContext("2d"); //instancia do operador grafico 2d
ctx_cnc.beginPath();    
ctx_cnc.lineWidth = "2";
ctx_cnc.strokeStyle = "white";
ctx_cnc.rect(2, 105, 496, 18);

async function update_container_cnc() {
    let value = await eel.update_monitor_cnc()();
    ctx_cnc.fillStyle = '#808080'; //define estilo do que vai ser desenhado
    ctx_cnc.fillRect(0, 0, canvas_cnc.width, canvas_cnc.height); //Limpar area a ser desenhada
    ctx_cnc.fillStyle = '#ffffff'; //cor do texto
    ctx_cnc.font = '20px serif'; // formatting text   
    var linecount = 1;
    for (var i in value) {
        ctx_cnc.fillText(value[i],10,linecount*20);
        linecount ++
    ctx_cnc.stroke();
    }
}
var routine_container_cnc = setInterval(update_container_cnc, 500);
