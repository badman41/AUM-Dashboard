const spawn  = require("child_process").spawn;

function get_ip(){
    var pyProcess = spawn("python.exe", ['./linkers/get_ip.py']);

    //pyProcess.stdout.setEncoding("utf8");
    console.log("Starting")
    pyProcess.stdout.on('data', (data)=>{
    console.log(data);
    });
    
    pyProcess.stderr.on('data',(err)=>{
        console.log(err);
    });

    pyProcess.on('exit', (code)=>{
        console.log(code);
    });
}
