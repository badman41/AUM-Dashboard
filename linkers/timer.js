function showTimer() {
    var progressBar = document.getElementById('progressBar');
    var timeleftIndicator = document.getElementById('timeLeft')
    var percComplete = document.getElementById('percComplete')
    var progressor = document.getElementById('needed');
    var percente = document.getElementById('perce');

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
    //progress(0);

    function update(progVal) {
        percent = Math.ceil((progVal / length) * 100);
        //timeleftIndicator.innerText = progVal
        //percComplete.innerText = Math.ceil(percent);
        var style = "c100" + " " + "p" + percent;
        //console.log(style);
        progressor.className = style;
        percente.innerHTML = percent;
        if(percent<100){
            setTimeout(function () {
                update(progVal + 1)
            }, 1000);
        }

    }
    update(0);

}

