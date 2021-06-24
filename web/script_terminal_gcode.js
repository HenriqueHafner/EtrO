class terminal_gcode {
    constructor() {
        this.canvas = document.getElementById("canvas_terminal_gcode"); //instancia controladora do canvas_gcode
        this.ctx = this.canvas.getContext("2d"); //instancia do operador grafico 2d
        this.ctx.beginPath();    
        this.ctx.lineWidth = "2";
        this.ctx.strokeStyle = "white";
        this.ctx.rect(2, 105, 496, 18);
    }
    updater(instance=this){
    setInterval( function() {instance.update(); }, 200);
    }
    async update() {
        var ctx = this.ctx
        var canvas = this.canvas
        var container_data = await eel.update_terminal_gcode()();
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
    async interface_setup_data(){
        var interface_data = await eel.call_terminal_gcode('setup')();
        var obj_pointer = this
        var div_main = document.getElementById('div_terminal_gcode');
        for (var i in interface_data){
            const gadget = interface_data[i]
            const label = gadget
            const button = document.createElement("BUTTON");
            button.type = 'button'
            button.innerHTML = label;
            button.onclick = function() {obj_pointer.gadgetcall(label)};
            div_main.appendChild(button);
            }
    }
    async gadgetcall(call) {
        const interface_data = await eel.call_terminal_gcode(call)();
    }
}

var obj_terminal_gcode = new terminal_gcode();
obj_terminal_gcode.interface_setup_data()
obj_terminal_gcode.updater()