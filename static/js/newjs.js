$(document).ready(function () {
    // Initial UI setup
    $('.image-section').hide();
    $('.loader').hide();
    $('#result').hide();
    $('#soil-moisture-result').hide();

    // Preview uploaded image
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#imagePreview').attr('src', e.target.result);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }

    // Image upload change event
    $("#imageUpload").change(function () {
        $('.image-section').show();
        $('#btn-predict').show();
        $('#result').text('');
        $('#result').hide();
        readURL(this);
    });

    // Predict button
    $('#btn-predict').click(function () {
        var form_data = new FormData($('#upload-file')[0]);
        $(this).hide();
        $('.loader').show();
    
        $.ajax({
            type: 'POST',
            url: '/predict',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (data) {
                $('.loader').hide();
                $('#result').fadeIn(600);
                $('#result').html('<b>Result: </b>' + data); 
                console.log('Success!');
            },
        });
    });
    

    // Soil moisture fetching
let intervalId = null;

$('#get-moisture').click(function () {
    let ip = $('#esp32-ip').val().trim();

    if (!ip) {
        $('#soil-moisture-result')
            .show()
            .removeClass("alert-success")
            .addClass("alert-danger")
            .text("Please enter the ESP32 IP address.");
        return;
    }

    // Clear previous interval
    if (intervalId !== null) {
        clearInterval(intervalId);
    }

    $('#soil-moisture-result')
        .show()
        .removeClass("alert-danger")
        .addClass("alert-info")
        .text("Starting moisture monitoring...");

    function fetchMoisture() {
        let url = "http://" + ip + "/moisture";

        $.get(url, function (data) {
            let moistureValue = parseFloat(data);  // Assuming the returned data is the moisture value
            $('#soil-moisture-result')
                .removeClass("alert-danger")
                .addClass("alert-success")
                .html("Soil Moisture Value: <b>" + moistureValue + "</b>");

            // Check moisture value and display corresponding message
            if (moistureValue < 60) {
                $('#soil-moisture-result').append("<br><b>The plant must be watered!</b>");
            } else {
                $('#soil-moisture-result').append("<br><b>The plant is already watered.</b>");
            }
        }).fail(function () {
            $('#soil-moisture-result')
                .removeClass("alert-success")
                .addClass("alert-danger")
                .text("Failed to fetch from ESP32. Please check the IP address or your network connection.");
            clearInterval(intervalId);
            intervalId = null;
        });
    }

    fetchMoisture(); // Initial fetch
    intervalId = setInterval(fetchMoisture, 1000); // Fetch every second
});

// Optional: Stop button logic (if added)
$('#stop-moisture').click(function () {
    if (intervalId !== null) {
        clearInterval(intervalId);
        intervalId = null;
        $('#soil-moisture-result').text("Fetching stopped.");
    }
});
});
