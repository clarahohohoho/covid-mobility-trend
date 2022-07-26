
// DOWNLOAD - START

function download_prompt(response){

    console.log(response);
};


// upon clicking on download button
$("#download-button").click(function (e) {

    $("#download-button").addClass("loading").addClass("disabled");

    var geotypevalues = JSON.stringify($('#geotype-select').val());
    var regionvalues = JSON.stringify($('#region-select').val());
    window.location = 'http://localhost:5000/file/download?geotype='+geotypevalues+'&region='+regionvalues;

    console.log(geotypevalues)
    $("#download-button").removeClass("loading").removeClass("disabled");

});

// DOWNLOAD - END

// UPLOAD - START

// handling function for upload response
function upload_handler(response){

    console.log(response)

    if (response.response === "false"){
        $('#upload-modal').modal('show');         
    }
    else if (response.response === "true"){
        $('#upload-status').text('File uploaded successfully!').css('color', 'green');
        setTimeout(function() {
            $("#upload-status").text('');
        }, 3000);
        $('#upload-button').text('Uploaded').addClass('green');
        setTimeout(function() {
            $("#upload-button").text('Upload').removeClass('green');
        }, 3000);
        render_filtered_chart();
        $('#file').val("");
    }
    else {
        $('#upload-status').text(response.response).css('color', 'red');
        setTimeout(function() {
            $("#upload-status").text('');
        }, 8000);
    }

    $("#upload-button").removeClass("loading").removeClass("disabled");

};

// functions for buttons in upload modal
$('#yes-modal').click(function(e){
    let override = true
    upload_function(override);
});
$('#no-modal').click(function(e){
    $('#upload-status').text('File not uploaded, please try again.').css('color', 'red');
    setTimeout(function() {
        $("#upload-status").text('');
    }, 3000);
    $('#file').val("");
});  

// function to post upload file to endpoint
function upload_function(override){
    var geotypevalues = JSON.stringify($('#geotype-select').val());
    var regionvalues = JSON.stringify($('#region-select').val());
    var trafficLimit = $('#traffic-limit-number').val();

    if (trafficLimit == ""){
        trafficLimit = 3000;
    };

    console.log(trafficLimit)

    var fd = new FormData();
    var files = $('#file')[0].files[0];
    fd.append('file', files);
    fd.append('geotype', geotypevalues);
    fd.append('region', regionvalues);
    fd.append('trafficLimit', trafficLimit);
    fd.append('override', override);

    $.ajax({
        url: 'http://127.0.0.1:5000/file/upload',
        type: 'post',
        data: fd,
        contentType: false,
        processData: false,
        success: function(response){
            if(response != 0){
                upload_handler(response);
            }
            else{
                $('#upload-status').text('File not uploaded, please try again.').css('color', 'red');
                $("#upload-button").removeClass("loading").removeClass("disabled");
            }
        },
    });
}

// function when upload button is clicked, file prompt appears
$(document).ready(function() {
    $("#upload-button").click(function(e) {

        $("#upload-button").addClass("loading").addClass("disabled");
        $("#upload-status").text("");

        $("#file").click();
    });
});

// function when upload file changes from file prompt
$("#file").change(function() {
    //if no file selected and file prompt is exited, restore upload button functionalities 
    if ($(this).get(0).files.length === 0){
        $("#upload-button").removeClass("loading").removeClass("disabled");
        return;
    }
    // else proceed with upload function
    upload_function(false);

});

// if user cancels upload prompt or clicks out of screen, restore upload button functionalities
$(window).focus(function() {
    if ($("#file").get(0).files.length === 0){
        $("#upload-button").removeClass("loading").removeClass("disabled");
    }
});

// UPLOAD - END