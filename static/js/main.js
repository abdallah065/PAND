$(document).ready(function () {
    // Init
    $('.image-section').hide();
    $('.loader').hide();
    $('#result').hide();
    $('#file_name').hide()
    $('#classes').hide()

    // Upload Preview
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#imagePreview').css('background-image', 'url(' + e.target.result + ')');
                $('#file_name').text(input.files[0].name).show();
                console.log(input.files[0].name)
                $('#imagePreview').hide();
                $('#imagePreview').fadeIn(650);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }
    $("#imageUpload").change(function () {
        $('.image-section').show();
        $('#btn-predict').show();
        $('#result').hide();
        readURL(this);
    });

    // Predict
    $('#btn-predict').click(function () {
        var form_data = new FormData($('#upload-file')[0]);

        // Show loading animation
        $(this).hide();
        $('.loader').show();

        // Make prediction by calling api /predict
        $.ajax({
            type: 'POST',
            url: '/predict',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (data) {
                console.log(data);
                // Get and display the result
                $('.loader').hide();
                data = data.replace(/'/g, '"');
                json_data = JSON.parse(data) //(plant,status,disease)
                console.log(json_data);
                //assign values to html the 3 html elements
                for(var i=0;i<3;i++){
                    $('#plant'+(i+1)).text(json_data[i].plant);
                if(json_data[i].status == "healthy"){
                    $('#status'+(i+1)).css('color', 'green');
                    $('#disease'+(i+1)).css('color', 'green');
                    $('#status'+(i+1)).text("Healthy");
                    $('#disease'+(i+1)).text("No disease detected");
                    $('#confidence'+(i+1)).text(json_data[i].confidance + " %").css('color', 'black');
                }else{
                    $('#status'+(i+1)).css('color', 'red');
                    $('#disease'+(i+1)).css('color', 'red');
                    $('#status'+(i+1)).text("Unhealthy");
                    $('#disease'+(i+1)).text(json_data[i].disease);
                    $('#confidence'+(i+1)).text(json_data[i].confidance + " %").css('color', 'black');
                }
                $('#result').fadeIn(600);
                console.log('Success!');
            }
            },
        });
    });

    // get clesses
    $('#get_classes').click(function () {

        // Make prediction by calling api /predict
        $.ajax({
            type: 'POST',
            url: '/get_classes',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (data) {
                console.log(data);
                // Get and display the result
                $('.loader').hide();
                json_data = data.replace(/'/g, '"');
                json_data = JSON.parse(data) //(plant,status,disease)
                console.log(json_data);
                $('#classes').text(data).show()
                console.log('Success!');
            },
        });
    });

});
