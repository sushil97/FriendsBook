$("#id_recipient").keyup(function () {
    var username = $(this).val();
    if (username.length > 0) {
        $.ajax({
            url: '/validate_username/',
            data: {
                'username': username
            },
            success: function (data) {
                if (data === 'True') {
                    $("#username_status").css({"display": "none"});
                    $('#send_email').removeAttr('disabled');
                }

                else {
                     $("#username_status").css({"display": "block"});
                    $('#send_email').attr('disabled','disabled');
                }
            }
        });
    }
});