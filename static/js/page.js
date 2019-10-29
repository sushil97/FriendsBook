$("#id_page").keyup(function () {
    var page = $(this).val();
    if (page.length > 0) {
        $.ajax({
            url: '/validate_pagename/',
            data: {
                'page': page
            },
            success: function (data) {
                if (data === 'True') {
                    $("#pagename_status").css({"display": "block"});
                    $('#create_p').attr('disabled','disabled');
                } else {
                    $("#pagename_status").css({"display": "none"});
                    $('#create_p').removeAttr('disabled');
                }
            }
        });
    }

});