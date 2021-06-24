class monitor_machine {
    constructor() {
        this.canvas = document.getElementById("canvas_monitor_machine"); //instancia controladora do canvas_gcode
        this.ctx = this.canvas.getContext("2d"); //instancia do operador grafico 2d
    }
    updater(instance=this) {
    setInterval( function() {obj_monitor_machine.update(); }, 500);
    }
    async update() {
        var ctx = this.ctx
        var canvas = this.canvas
        var container_data = await eel.update_monitor_machine()();
        ctx.fillStyle = '#808080'; //define estilo do que vai ser desenhado
        ctx.fillRect(0, 0,canvas.width,canvas.height); //Limpar area a ser desenhada
        ctx.fillStyle = '#ffffff'; //cor do texto
        ctx.font = '20px serif'; // formatting text   
        var linecount = 1;
        for (var i in container_data) {
            ctx.fillText(container_data[i],10,linecount*20);
            linecount ++;
        ctx.stroke();
        }
    }
}

var obj_monitor_machine = new monitor_machine()
obj_monitor_machine.updater()
