
var ClientState = [0,1];
var ClientUpdates = 0

var img1 = new Image();  
img1.src = "./images/ExImage1.jpg";
var img2 = new Image();  
img2.src = "./images/ExImage2.jpg";
var img3 = new Image();  
img3.src = "./images/ExImage3.jpg";
var img4 = new Image();  
img4.src = "./images/ExImage4.jpg";
var img5 = new Image();  
img5.src = "./images/ExImage5.jpg";
Images = [img1,img1,img2,img3,img4,img5]

var ctx1 = document.getElementById("canvas1").getContext("2d");

async function draw_1(Pos = ClientState) {
	ctx1.drawImage(Images[Pos[1]],0,0,259,194,0,0,259,194)
}
	
async function UpdateClient() {
	//ctx1.clearRect(0,0,259,194);
    let value = await eel.UpdateClient()();
    ClientState = value;
	ClientUpdates++;
	draw_1();
	//console.log('ClientUpdated #'+ClientUpdates);
	}

var UpdateClientRoutine = setInterval(UpdateClient, 5);
//clearInterval(UpdateClientRoutine)

console.log('Index.js run');


