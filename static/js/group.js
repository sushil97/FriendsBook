/* Check whether username is available */

$("#id_name").keyup(function () {
    var name = $(this).val();
    if (name.length > 0) {
        $.ajax({
            url: '/validate_groupname/',
            data: {
                'name': name
            },
            success: function (data) {
                if (data === 'True') {
                    $("#groupname_status").css({"display": "block"});
                    $('#create_g').attr('disabled','disabled');
                } else {
                    $("#groupname_status").css({"display": "none"});
                    $('#create_g').removeAttr('disabled');
                }
            }
        });
    }

});
//
$("#invite").click(function (e) {
    e.preventDefault();
    var username = $('#id_invite_username').val();
    var name =$("#group_name").text();
    console.log(username);
    console.log(name);
    if (username.length > 0) {
        $.ajax({
            type: 'POST',
            url: '/group_invite/',
            data: {
                'name':name,
                'username': username
            },
            success: function (data) {
                if (data==='username_error') {
                    $("#username_avail").css({"display": "block"});
                    $("#group_signup").css({"display": "none"});
                    $("#already_sent").css({"display": "none"});
                    $("#sent").css({"display": "none"});
                } else if (data==='user_exist'){
                    $("#group_signup").css({"display": "block"});
                    $("#username_avail").css({"display": "none"});
                    $("#already_sent").css({"display": "none"});
                    $("#sent").css({"display": "none"});
                }
                else if(data==='already_sent'){
                    $("#group_signup").css({"display": "none"});
                    $("#username_avail").css({"display": "none"});
                    $("#already_sent").css({"display": "block"});
                    $("#sent").css({"display": "none"});
                }
                else if(data==='invitation_sent'){
                    $("#group_signup").css({"display": "none"});
                    $("#username_avail").css({"display": "none"});
                    $("#already_sent").css({"display": "none"});
                    $("#sent").css({"display": "block"});
                }
            }
        });
    }

});