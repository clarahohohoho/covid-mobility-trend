
// upadate values in multiselect filters
function update_filter_values(response){

    var $el = $("#geotype-select");
    $el.empty(); // remove old options
    for (let i = 0; i < response.geotype.length; i++) {
        $el.append($("<option></option>").attr("value", response.geotype[i]).text(response.geotype[i]));
    };

    var $el = $("#transportation-select");
    $el.empty(); // remove old options
    for (let i = 0; i < response.transportation.length; i++) {
        $el.append($("<option></option>").attr("value", response.transportation[i]).text(response.transportation[i]));
    };

    var $el = $("#region-select");
    $el.empty(); // remove old options
    for (let i = 0; i < response.region.length; i++) {
        $el.append($("<option></option>").attr("value", response.region[i]).text(response.region[i]));
    };

}


$("#filter-button").click(function (e) {
    $("#filter-button").addClass('loading').addClass('disabled');
    $('#filter-number').val("");
    $("#region-list").html("");
    render_filtered_chart();
});

$("#clear-filter-button").click(function (e) {

    $("#clear-filter-button").addClass('loading').addClass('disabled');
    $("#geotype-select").removeProp('selected').dropdown('clear');
    $("#region-select").removeProp('selected').dropdown('clear');
    $("#transportation-select").removeProp('selected').dropdown('clear');
    $.get("http://127.0.0.1:5000/filter/all", receiveData);

});

$("#clear-number-filter-button").click(function (e) {

    $("#clear-number-filter-button").addClass('loading').addClass('disabled');
    $("#filter-number").val("")
    $("#region-list").html("");
    $.get("http://127.0.0.1:5000/filter/all", receiveData);

});

// update filtered regions based on traffic number
function number_filter_handler(response){

    console.log(response.region);
    region_html = ""

    for (let i = 0; i < response.region.length; i++) {
        region_html += "<div class='item'>" + response.region[i] + "</div>";
    }

    $("#region-list").html(region_html);

    receiveData(response);
}

// when button for filtering by traffic number is clicked
$("#number-filter-button").click(function (e) {

    $("#number-filter-button").addClass('loading').addClass('disabled');
    $("#geotype-select").removeProp('selected').dropdown('clear');
    $("#region-select").removeProp('selected').dropdown('clear');
    $("#transportation-select").removeProp('selected').dropdown('clear');

    var trafficNumber = $('#filter-number').val();

    console.log(trafficNumber);

    $.ajax({
        type: "POST",
        contentType: "application/json; charset=utf-8",
        url: "http://127.0.0.1:5000/filter/filter-traffic-number",
        data: JSON.stringify({trafficNumber: trafficNumber}),
        success: number_filter_handler,
        dataType: "json"
    });

});