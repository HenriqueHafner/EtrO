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
    
    script = document.createElement('script');
    script.src = "script_".concat(element_idtoset.concat(".js"))
    //script.src = "script_Gcode_Terminal.js";
    console.log(script.src);
    
    div_to_add.appendChild(canvas_toadd);
    div_main.appendChild(div_to_add);
    
    document.body.appendChild(script)
}




