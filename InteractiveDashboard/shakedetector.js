let lastX = 0, lastY = 0, lastZ = 0;
let threshold = 15;
let shakeTimeout;

window.addEventListener("devicemotion", function(event) {
    let acceleration = event.accelerationIncludingGravity;
    if (!acceleration) return;

    let deltaX = Math.abs(acceleration.x - lastX);
    let deltaY = Math.abs(acceleration.y - lastY);
    let deltaZ = Math.abs(acceleration.z - lastZ);

    if ((deltaX > threshold && deltaY > threshold) || (deltaX > threshold && deltaZ > threshold) || (deltaY > threshold && deltaZ > threshold)) {
        if (!shakeTimeout) {
            shakeTimeout = setTimeout(triggerEmergencyAlert, 500);
        }
    }

    lastX = acceleration.x;
    lastY = acceleration.y;
    lastZ = acceleration.z;
});

function triggerEmergencyAlert() {
    clearTimeout(shakeTimeout);
    shakeTimeout = null;
    alert("Emergency! Shake detected! Siren will sound.");
    playSiren();
}

function playSiren() {
    let siren = new Audio("siren.mp3");
    siren.loop = true;
    siren.play();
}