
// run function when lock button is clicked
$("#lock-button").click(function(e) {

    $("#lock-button").addClass("loading").addClass("disabled");

    var geotypevalues = $('#geotype-select').val();
    var regionvalues = $('#region-select').val();

    if(document.getElementById('unlock-data-radio').checked) {
        var lockStatus = "unlock"
    } else if(document.getElementById('lock-data-radio').checked) {
        var lockStatus = "lock"
    }

    console.log(lockStatus)

    $.ajax({
        type: "POST",
        contentType: "application/json; charset=utf-8",
        url: "http://127.0.0.1:5000/file/lock-data",
        data: JSON.stringify({lockStatus: lockStatus, geotype: geotypevalues, region:regionvalues}),
        success: function(response){
            if(response != 0){
                if(response.lockStatus == 'lock'){
                    $('#lock-status').text('Data locked successfully!').css('color', 'green');
                    setTimeout(function() {
                        $("#lockstatus").text('');
                    }, 3000);
                    $("#lock-button").removeClass("loading").removeClass("disabled");
                }
                else{
                    $('#lock-status').text('Data unlocked successfully!').css('color', 'green');
                    setTimeout(function() {
                        $("#lockstatus").text('');
                    }, 3000);
                    $("#lock-button").removeClass("loading").removeClass("disabled");
                };
            }
            else{
                $('#lock-status').text('Data locking/unlocking failed. Please try again.').css('color', 'red');
                setTimeout(function() {
                    $("#lockstatus").text('');
                }, 3000);
                $("#lock-button").removeClass("loading").removeClass("disabled");
            }
        },
        dataType: "json"
    });

});
