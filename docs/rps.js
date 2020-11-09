const video = document.createElement('video');
video.autoplay = true;
const enableWebcamButton = document.getElementById('webcamButton');
const disableWebcamButton = document.getElementById('webcamButtonOff');
const canvas = document.getElementById('canvas')
var ctx = canvas.getContext('2d')

ctx.beginPath();
ctx.lineWidth = "2";
ctx.strokeStyle = "green";
ctx.rect(40, 40, 256, 256);
ctx.font = "18px Arial";
ctx.fillStyle = "blue";

function getUserMediaSupported() {
    return !!(navigator.mediaDevices &&
        navigator.mediaDevices.getUserMedia);
}

if (getUserMediaSupported()) {
    enableWebcamButton.addEventListener('click', enableCam);
} else {
    console.warn('getUserMedia() is not supported by your browser');
}

function enableCam(event) {
    event.target.classList.add('removed');
    const constraints = {
        video: true
    };
    navigator.mediaDevices.getUserMedia(constraints).then(function (stream) {
        video.srcObject = stream;
        video.addEventListener('loadeddata', predictMove);
    });
}

function choose(choices) {
    var index = Math.floor(Math.random() * choices.length);
    return choices[index];
}

async function predictMove() {
    var move = ''
    var classes = ['rock', 'paper', 'scissors']
    var prev = ''
    var comp_move = ''
    var disable_flag = false

    var rock = document.createElement('img')
    rock.src = 'https://raw.githubusercontent.com/saivinayb/rps/master/assets/rock.png'
    var paper = document.createElement('img')
    paper.src = 'https://raw.githubusercontent.com/saivinayb/rps/master/assets/paper.png'
    var scissor = document.createElement('img')
    scissor.src = 'https://raw.githubusercontent.com/saivinayb/rps/master/assets/scissors.png'

    const model = await tf.loadLayersModel('https://raw.githubusercontent.com/saivinayb/rps/master/models/rps_tfjs_model/model.json')

    const predict_loop = setInterval(function () {
        ctx.drawImage(video, 0, 0, 640, 480)
        ctx.stroke();
        var imgdata = tf.tidy(
            () => tf.browser.fromPixels(video).slice([40, 40, 0], [296, 296, 3]).resizeBilinear([100, 100]).mean(2).div(tf.scalar(255)).expandDims(0).expandDims(-1)
        )
        var pred = tf.tidy(
            () => model.predict(imgdata)
        )
        pred = pred.argMax(axis = 1).dataSync()[0]
        move = classes[pred]
        if (move != prev) {
            comp_move = choose([0, 1, 2])
        }
        prev = move;
        ctx.fillText("prediction: " + move, 85, 25);
        ctx.fillText("CPU's move: " + classes[comp_move], 410, 25);
        if (comp_move == 0) { ctx.drawImage(rock, 344, 40, 256, 256) }
        if (comp_move == 1) { ctx.drawImage(paper, 344, 40, 256, 256) }
        if (comp_move == 2) { ctx.drawImage(scissor, 344, 40, 256, 256) }
        disableWebcamButton.addEventListener('click', function () {
            disable_flag = true
        })
        if (disable_flag) {
            ctx.clearRect(0, 0, canvas.width, canvas.height)
            clearInterval(predict_loop);
            stream = video.srcObject;
            stream.getTracks().forEach(track => track.stop())
        }
    }, 35)
}

