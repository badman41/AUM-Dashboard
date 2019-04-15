function showTimer() {
    var progressBar = document.getElementById('progressBar');
    var timeleftIndicator = document.getElementById('timeLeft')
    var percComplete = document.getElementById('percComplete')
    length = document.getElementById('duration').value;
    console.log(length);

    function progress(progVal) {
        percent = (progVal / length) * 100;
        timeleftIndicator.innerText = progVal
        percComplete.innerText = Math.ceil(percent);
        //console.log(percent + "%");
        progressBar.MaterialProgress.setProgress(percent);
        //progressBar.MaterialProgress.setBuffer(100 - percent);
        if (progVal < length) {
            //console.log("Prog :" + progVal);
            setTimeout(function () {
                progress(progVal + 1);
            }, 1000);
        }

    }
    progress(0);

}

