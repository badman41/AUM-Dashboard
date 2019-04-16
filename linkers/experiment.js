var time = document.getElementById('duration');
var clientAddr = document.getElementById('clientAddr');
var eventNum = document.getElementById('eventNumber');
var events = document.getElementById('events');



function showDialog() {
    console.log("clicked to see dialog");
    var dialog = document.querySelector('dialog');
    var showDialogButton = document.querySelector('#show-dialog');
    if (!dialog.showModal) {
        dialogPolyfill.registerDialog(dialog);
    }
    dialog.showModal();
    dialog.querySelector('.close').addEventListener('click', function () {
        dialog.close();
    });
}

function clearVals() {
    console.log(time.value, clientAddr.value, eventNum.value);
    console.log("clearing values");
    time.value = "";
    clientAddr.value = "";
    eventNum.value = "";
    events.value = "";
}

function startExperiment() {
    var dialog = document.querySelector('dialog');
    dialog.close();
    showTimer();
    startCharting();
    //createSSH();
}


