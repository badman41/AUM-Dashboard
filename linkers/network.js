const {
    app,
    BrowserWindow
} = require('electron')
let {
    PythonShell
} = require('python-shell');


async function serverIP() {
    PythonShell.run('./engine/get_ip.py', null, async function (err, results) {
        if (err) throw err;
        serverIp = results[0]
        let promise = new Promise((resolve, reject) => {
            setTimeout(() => resolve(serverIp), 1000)
        })

        textBlock = document.getElementById('serverip');

        let result = await promise;
        console.log("result is", result);

        var snackbarContainer = document.querySelector('#ipToast')
        let data = {
            message: "Server IPv4: " + result,
            timeout: 2000
        }
        //console.log("toast data",data)
        snackbarContainer.MaterialSnackbar.showSnackbar(data);

                
        textBlock.value = result;
        return (result);
    });
}

async function clientIP() {
    PythonShell.run("./engine/get_ip.py", null, async function (err, results) {
        if (err) throw err;



    });
}