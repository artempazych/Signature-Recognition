var canvas = document.getElementById('signature');
var ctx = canvas.getContext('2d');
ctx.fillStyle = '#FFF'; // color of the canvas
ctx.fillRect(0, 0, canvas.width, canvas.height); // crearing the canvas

addEventListener('keydown', function(evt) { // keyboard button event handler
    if (evt.keyCode == 27 || evt.keyCode == 8 || evt.keyCode == 46) { // check for backspace, del, esc
        evt.preventDefault();
        clearCanvas();
    }
});

function getRealMousePos(canvas, evt) { // the function of obtaining the coordinates of the mouse, relative to the canvas
    var rect = canvas.getBoundingClientRect();
    return {
        x: evt.clientX - rect.left,
        y: evt.clientY - rect.top
    };
}

var pos = { x: 0, y: 0 };

// events for drawing in canvas
canvas.addEventListener('mousemove', draw);
canvas.addEventListener('mousedown', setPosition);
canvas.addEventListener('mouseenter', setPosition);

function sendToServer(e)
{
 //sending picture to a server
    var dataURL = canvas.toDataURL("image/png");
    fetch("http://localhost:8000/", {
        method: "POST",
        body: dataURL
    }).then(d => d.json()).then(d =>
    {
        document.getElementById('result').innerHTML = d.status; // printing output
    });
}
function clearCanvas(e) // crearing the canvas 
{
    ctx.fillStyle = '#FFF';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    document.querySelector('#result').innerHTML = '';
}
function changeCanvasSize(e) // changing the size of canvas
{
    var w = parseInt(document.getElementById('canvasWidth').value);
    var h = parseInt(document.getElementById('canvasHeight').value);
    canvas.setAttribute('width', w);
    canvas.setAttribute('height', h);
}
function setPosition(e) { // Writing mouse position to pos variable
    pos = getRealMousePos(canvas, e);
}
function draw(e) { // draw function
    if (e.buttons !== 1)
        return;
    ctx.beginPath();
    ctx.lineWidth = 2;
    ctx.lineCap = 'round';
    ctx.strokeStyle = '#000000';
    ctx.moveTo(pos.x, pos.y);
    setPosition(e);
    ctx.lineTo(pos.x, pos.y);
    ctx.stroke();
}

function createSphere(button, evt) { // creating an expanding circle by pressing a button
    evt.preventDefault();
    var div = document.createElement('div');
    div.className = 'sphere';
    div.style.left = (evt.clientX - button.getBoundingClientRect().x - (150 / 2)) + 'px';
    div.style.top = (evt.clientY - button.getBoundingClientRect().y - (150 / 2)) + 'px';
    button.appendChild(div);
    setTimeout(function() {
        div.remove();
    }, 250)
}