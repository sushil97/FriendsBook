function validatepass() {
    var pass_rex = new RegExp("^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})");
    var mediumRegex = new RegExp("^(((?=.*[a-z])(?=.*[A-Z]))|((?=.*[a-z])(?=.*[0-9]))|((?=.*[A-Z])(?=.*[0-9])))(?=.{6,})");
    //var weakRegex = new RegExp("^(((?=.*[a-z]))|((?=.*[0-9]))|((?=.*[A-Z])))(?=.{6,})");

    var password = document.getElementById('id_password').value;
    if (pass_rex.test(password)) {
        document.getElementById('id_password').style.background = "#ccffcc";
        document.getElementById('pass_strength').style.color = 'green';
        document.getElementById('pass_strength').innerHTML = "Strong Password"
        return true;
    } else if (mediumRegex.test(password)) {
        document.getElementById('id_password').style.background = "rgba(255,195,0,0.44)";
        document.getElementById('pass_strength').style.color = 'orange';
        document.getElementById('pass_strength').innerHTML = "Medium Password"
    }
    // else if(weakRegex.test(password)){
    //     document.getElementById('id_password').style.background = "rgba(255,195,0,0.44)";
    //     document.getElementById('pass_strength').style.color = 'green';
    //     document.getElementById('pass_strength').innerHTML = "Strong Password"
    // }
    else {
        document.getElementById('id_password').style.background = 'rgba(255,10,0,0.19)';
        document.getElementById('pass_strength').style.color = 'red';
        document.getElementById('pass_strength').innerHTML = "Weak Password"
        return false;
    }
}

function checkpass() {
    var password = document.getElementById('id_password').value;
    var password1 = document.getElementById('id_password1').value;
    if (password == password1) {
        document.getElementById('id_password1').style.background = "#ccffcc";
        document.getElementById('pass_match_error').style.display = "none";
        document.getElementById('pass_strength').style.display = "none";
        return true;
    } else {
        document.getElementById('id_password1').style.background = 'rgba(255,10,0,0.19)';
        document.getElementById('pass_match_error').style.color = 'red';
        document.getElementById('pass_match_error').innerHTML = "Password doesn't match";
        return false;
    }
}


$(document).ready(function () {
    $('.close, [data-dismiss="modal"]').on("click", function () {
        $('#profile_pic').val('');
        $('#profile_pic_preview').attr('src', '');
        $('#profile_pic_preview').removeClass("img-thumbnail");
    });

    function showPreview(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            var imgFieldId = $(input).closest('form').find('img.img-preview').prop('id');
            reader.onload = function (e) {
                $('#' + imgFieldId).attr('src', e.target.result);
                $('#' + imgFieldId).addClass("img-thumbnail");
            };
            reader.readAsDataURL(input.files[0]);
        }
    }

    $('input[type=file]').change(function () {
        showPreview(this);
    });
});


function validate_username() {

}

/* Check whether username is available */

$("#id_username").keyup(function () {
    var username = $(this).val();
    if (username.length > 0) {
        $.ajax({
            url: '/validate_username/',
            data: {
                'username': username
            },
            success: function (data) {
                if (data === 'True') {
                    $("#username_status").css({"display": "block"});
                    $('#create_a').attr('disabled','disabled');

                }

                else {
                    $("#username_status").css({"display": "none"});
                    $('#create_a').removeAttr('disabled');

                }
            }
        });
    }
});
