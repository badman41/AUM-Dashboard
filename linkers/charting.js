function getData() {
    //console.log("hit!");
    return Math.random();
}

Plotly.plot('chart', [{
    y: [getData()],
    type: 'line'
}]);

function startCharting(){
setInterval(function () {
    Plotly.extendTraces('chart', {
        y: [
            [getData()]
        ]
    }, [0])
}, 1000);
}