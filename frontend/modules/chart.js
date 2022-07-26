const data = {}
// numeral.locale('pt-br');
const ctx = document.getElementById('myChart').getContext('2d');
const myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: data.label,
        datasets: [
            {
                label: 'Overall Mobility Rate',
                data: data.values,
                borderColor: "#B19CD9",
                backgroundColor: "#B19CD9",
                yAxisID: "y"
            },
            {
                label: 'Mobility Rate - Driving',
                data: data.values,
                borderColor: "#A7C7E7",
                backgroundColor: "#A7C7E7",
                yAxisID: "y"
            },
            {
                label: 'Mobility Rate - Walking',
                data: data.values,
                borderColor: "#8EE3EF",
                backgroundColor: "#8EE3EF",
                yAxisID: "y"
            },
            {
                label: 'Mobility Rate - Transit',
                data: data.values,
                borderColor: "#AEF3E7",
                backgroundColor: "#AEF3E7",
                yAxisID: "y"
            },
            {
                label: 'Number of new COVID-19 Cases',
                data: data.values,
                borderColor: "#FFD1DC",
                backgroundColor: "#FFD1DC",
                yAxisID: "y1"
            },
        ]
    },
    options: {
        scales: {
            x: {
                type: 'time',
                time: {
                    unit: 'month',
                    minUnit: 'month',
                    displayFormats: {
                        month: 'MMM-YY'
                     },
                },
                ticks: {
                    min: "2020-01-13",
                    max: "2021-07-27"
                }
            },
            y: {
                stacked: false,
                position: 'left',
                type: 'linear',
                // id: 'y-axis-0'
            }, 
            y1: {
                stacked: true,
                position: 'right',
                type: 'linear',
                grid: {
                    display: false
                 }
                // id: 'y-axis-1',
            }
        }
    }
});

function receiveData(response) {
    // const data = response
    myChart.data.labels = [];
    myChart.data.datasets[0].data = [];
    myChart.data.datasets[1].data = [];
    myChart.data.datasets[2].data = [];
    myChart.data.datasets[3].data = [];
    myChart.data.datasets[4].data = [];

    console.log(response);

    for (let i = 0; i < response.mobility.label.length; i++) {
        var dateObject = moment(response.mobility.label[i], 'MM-YYYY');
        myChart.data.labels.push(dateObject);
    }
    for (let i = 0; i < response.mobility.values.length; i++) {
        myChart.data.datasets[0].data.push(response.mobility.values[i]);
    }

    if (response.mobility_driving.values.length != 0){
        myChart.show(1)
    }
    else{
        myChart.hide(1)
    }
    if (response.mobility_walking.values.length != 0){
        myChart.show(2)
    }
    else{
        myChart.hide(2)
    }
    if (response.mobility_transit.values.length != 0){
        myChart.show(3)
    }
    else{
        myChart.hide(3)
    }
    if (response.covid.values.length != 0){
        myChart.show(4)
    }
    else{
        myChart.hide(4)
    }
    for (let i = 0; i < response.covid.values.length; i++) {
        myChart.data.datasets[4].data.push(response.covid.values[i]);
    }

    for (let i = 0; i < response.mobility_driving.values.length; i++) {
        myChart.data.datasets[1].data.push(response.mobility_driving.values[i]);
    }
    for (let i = 0; i < response.mobility_walking.values.length; i++) {
        myChart.data.datasets[2].data.push(response.mobility_walking.values[i]);
    }
    for (let i = 0; i < response.mobility_transit.values.length; i++) {
        myChart.data.datasets[3].data.push(response.mobility_transit.values[i]);
    }

    myChart.update();
    $("#filter-button").removeClass('loading').removeClass('disabled');
    $("#clear-filter-button").removeClass('loading').removeClass('disabled');
    $("#number-filter-button").removeClass('loading').removeClass('disabled');
    $("#clear-number-filter-button").removeClass('loading').removeClass('disabled');
}

function render_filtered_chart(){

    var geotypevalues = $('#geotype-select').val();
    var regionvalues = $('#region-select').val();
    var transportationvalues = $('#transportation-select').val();

    console.log(geotypevalues)

    $.ajax({
        type: "POST",
        contentType: "application/json; charset=utf-8",
        url: "http://127.0.0.1:5000/filter/filter-values",
        data: JSON.stringify({geotype: geotypevalues, region: regionvalues, transportation: transportationvalues}),
        success: receiveData,
        dataType: "json"
    });
}