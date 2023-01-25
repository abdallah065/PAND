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
                $('#plant').text(json_data.plant);
                if(json_data.status == "healthy"){
                    $('#status').css('color', 'green');
                    $('#disease').css('color', 'green');
                    $('#status').text("Healthy");
                    $('#disease').text("No disease detected");
                }else{
                    $('#status').css('color', 'red');
                    $('#disease').css('color', 'red');
                    $('#status').text("Unhealthy");
                    $('#disease').text(json_data.disease);
                }
                $('#result').fadeIn(600);
                console.log('Success!');
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
