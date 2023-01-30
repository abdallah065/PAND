$(document).ready(function () {
    // Init
    $('.image-section').hide();
    $('.loader').hide();
    $('#result').hide();
    $('#highest_card').hide();
    $('#file_name').hide()
    $('#classes').hide()
    $('#all_results').hide()

    // Upload Preview
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#imagePreview').css('background-image', 'url(' + e.target.result + ')');
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
        $('#highest_card').hide();
        $('#all_results').hide()
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
                // Get and display the result
                $('.loader').hide();
                data = data.replace(/'/g, '"');
                json_data = JSON.parse(data); //(plant,status,disease)
                console.log(json_data);
                $('#all_results').show();
                // log all child and subchild elements names indside highest_result
                highest_status="";
                highest_plant="";
                highest_confidence="";
                highest_disease_desc="";
                $('#highest_result').children().each(function() {
                    console.log($(this).attr('id'));
                    $(this).children().each(function() {
                        console.log($(this).attr('id'));
                        $(this).children().each(function() {
                            // if its id is highest_status
                            if($(this).attr('id') == 'highest_status'){
                                if (json_data[0].status == 'Healthy'){
                                    $(this).text("Healthy 🌱").css('color', 'green !important');
                                }else{
                                    $(this).text(json_data[0].disease).css('color', 'red !important');
                                }

                            }else if($(this).attr('id') == 'highest_plant_name'){
                                $(this).text("🌿 "+json_data[0].plant+" 🌿");

                            }else if($(this).attr('id') == 'highest_confidence'){
                                $(this).text("Confidence: "+json_data[0].confidance+ "%");
                                
                            }else if($(this).attr('id') == 'highest_disease_desc'){
                                $(this).text('Comming Soon...');

                            }
                        });
                    });
                });
                $('#highest_card').fadeIn(500);
                if(json_data[0].confidance < 99){
                    plants = [];
                    statuses = [];
                    confidences = [];
                    diseases_desc = [];
                    // log all child and subchild elements names indside result div
                    $('#result').children().each(function() {
                        console.log($(this).attr('id'));
                        $(this).children().each(function() {
                            console.log($(this).attr('id'));
                            $(this).children().each(function() {
                                $(this).children().each(function() {
                                    console.log($(this).attr('id'));
                                    // if its id is status1,2,3 add it to list called statuses
                                    if($(this).attr('id') == 'status1' || $(this).attr('id') == 'status2' || $(this).attr('id') == 'status3'){
                                        statuses.push($(this).attr('id'));
                                    }else if($(this).attr('id') == 'plant_name1' || $(this).attr('id') == 'plant_name2' || $(this).attr('id') == 'plant_name3'){
                                        plants.push($(this).attr('id'));
                                    }else if($(this).attr('id') == 'confidence1' || $(this).attr('id') == 'confidence2' || $(this).attr('id') == 'confidence3'){
                                        confidences.push($(this).attr('id'));
                                    }else if($(this).attr('disease_desc1') == 'disease_desc1' || $(this).attr('disease_desc2') == 'disease_desc2' || $(this).attr('disease_desc3') == 'disease_desc3'){
                                        diseases_desc.push($(this).attr('id'));
                                    }
                                });
                            });
                        });
                    });
                    //assign values to html the 3 html elements
                    for(var i=0;i<3;i++){
                        // add plant leaf imoji and plant name
                        $('#'+plants[i]).text("🌿 "+json_data[i+1].plant+" 🌿");
                        // add status
                        if (json_data[i].status == 'Healthy'){
                            $('#'+statuses[i]).text("Healthy 🌱").css('color', 'green !important');
                        }else{
                            $('#'+statuses[i]).text(json_data[i+1].disease).css('color', 'red !important');
                        }
                        // add disease description
                        $('#'+diseases_desc[i]).text(json_data[i+1].disease);
                        // add confidence
                        $('#'+confidences[i]).text("Confidence: "+json_data[i+1].confidance+ "%");
                        // add disease description
                        $('#'+diseases_desc[i]).text('Comming Soon...');
                    }

                    $('#result').fadeIn(650);
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
