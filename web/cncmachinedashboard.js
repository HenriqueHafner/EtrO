

//var canvas_gcode_terminal = document.createElement("CANVAS");
//canvas_gcode_terminal.id = "canvasCNC";
//canvas_gcode_terminal.width = 500;
//canvas_gcode_terminal.height =230;
//div_main.appendChild(canvas_gcode_terminal);

function view_container_create(element_idtoset) {
    div_main = document.getElementById("machine_dashboard");
    var canvas_toadd = document.createElement("CANVAS");
    canvas_toadd.id = "canvas_".concat(element_idtoset);
    canvas_toadd.width = 500;
    canvas_toadd.height =230;
    
    div_to_add = document.createElement("DIV");
    div_to_add.id = "div_".concat(element_idtoset);
    
    title_para = document.createElement("p");
    title_text = document.createTextNode(element_idtoset);
    
    var script_injection = document.createElement('script');
    script_injection.setAttribute("type","text/javascript");
    script_filename = "script_".concat(element_idtoset)
    script_filename = script_filename.concat(".js")
    script_injection.setAttribute("src", script_filename);
      
    title_para.appendChild(title_text);
    div_to_add.appendChild(title_para);
    div_to_add.appendChild(script_injection);  
    div_to_add.appendChild(canvas_toadd);
    div_main.appendChild(div_to_add);

}

view_container_create("gcode_terminal")
view_container_create("serial_console")




