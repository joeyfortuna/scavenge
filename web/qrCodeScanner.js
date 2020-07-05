/* 
  This code is taken from https://codesandbox.io/s/qr-code-scanner-ilrm9?file=/src/qrCodeScanner.js
  by Dmitri Lau (https://www.sitepoint.com/author/dlau) and Paul Orac (https://www.sitepoint.com/author/porac)
*/

const myqrcode = window.qrcode;

const video = document.createElement("video");
const canvasElement = document.getElementById("qr-canvas");
const canvas = canvasElement.getContext("2d");

const qrResult = document.getElementById("qr-result");
const outputData = document.getElementById("outputData");
const btnScanQR = document.getElementById("btn-scan-qr");

let scanning = false;
let initialized = false;

myqrcode.callback = res => {
  if (res) {
    outputData.innerText = res;
    scanning = false;
    document.getElementById('jinglePlayer').play();

    video.srcObject.getTracks().forEach(track => {
      track.stop();
    });

    qrResult.hidden = false;
    canvasElement.hidden = true;
    btnScanQR.hidden = false;
  }
};

btnScanQR.onclick = () => {

  btnScanQR.classList.add("wobbler");
  if (!initialized) {
    initialized = true;
    document.getElementById('jinglePlayer').play();
  }
  navigator.mediaDevices
    .getUserMedia({ video: { facingMode: "environment" } })
    .then(function(stream) {
      scanning = true;
      qrResult.hidden = true;
      btnScanQR.hidden = true;
      canvasElement.hidden = false;
      video.setAttribute("playsinline", true); // required to tell iOS safari we don't want fullscreen
      video.srcObject = stream;
      video.play();
      tick();
      scan();
    });
};

function tick() {
  canvasElement.height = video.videoHeight;
  canvasElement.width = video.videoWidth;
  canvas.drawImage(video, 0, 0, canvasElement.width, canvasElement.height);

  scanning && requestAnimationFrame(tick);
}

function scan() {
  try {
    myqrcode.decode();
  } catch (e) {
    setTimeout(scan, 300);
  }
}
