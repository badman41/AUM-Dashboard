const { app, BrowserWindow } = require("electron");
let { PythonShell } = require("python-shell");

async function serverIP() {
  PythonShell.run("./engine/get_ip.py", null, async function(err, results) {
    if (err) throw err;
    serverIp = results[0];
    let promise = new Promise((resolve, reject) => {
      setTimeout(() => resolve(serverIp), 1000);
    });

    textBlock = document.getElementById("serverip");

    let result = await promise;
    console.log("result is", result);

    var snackbarContainer = document.querySelector("#ipToast");
    let data = {
      message: "Server IPv4: " + result,
      timeout: 2000
    };
    //console.log("toast data",data)
    snackbarContainer.MaterialSnackbar.showSnackbar(data);

    textBlock.innerHTML = result;
    return result;
  });
}

async function clientIP() {
  PythonShell.run("./engine/get_ip.py", null, async function(err, results) {
    if (err) throw err;
  });
}

function createSSH() {
  //create a dialog to take in ssh user name and password
  var username = document.getElementById("uname");
  var password = document.getElementById("pwd");
  var command = "./client.py";
  var options = {
    args: [clientAddr, 22, uname, pwd, command]
  };
  PythonShell.run("./engine/get_ip.py", options, async function(err, results) {
    if (err) throw err;
    console.log("Connection Created!");
  });
}
