
function view_container_create(element_idtoset) {
    div_main = document.getElementById("machine_dashboard");
    canvas_toadd = document.createElement("CANVAS");
    canvas_toadd.id = "canvas_".concat(element_idtoset);
    canvas_toadd.width = 500;
    canvas_toadd.height =230;
    
    div_to_add = document.createElement("DIV");
    div_to_add.style.width = 502;
    div_to_add.id = "div_".concat(element_idtoset);
    
    title_para = document.createElement("p");
    title_text = document.createTextNode(element_idtoset);
    
    script_injection = document.createElement('script');
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

view_container_create("terminal_gcode")
view_container_create("monitor_serial")
view_container_create("monitor_machine")




