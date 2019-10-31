function GetSelectedTextValue(formselect) {
        var selectedText = formselect.options[formselect.selectedIndex].innerHTML;
        var selectedValue = formselect.value;
        if(selectedValue != ""){
            document.getElementById('pay_upgrade').disabled=false;
        }
        else{
             document.getElementById('pay_upgrade').disabled=true;
        }
        document.getElementById('id_amount').value = selectedValue;
    }



$("#wallet_user").keyup(function () {
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
                    $('#payment_a').removeAttr('disabled');
                }

                else {
                     $("#username_status").css({"display": "block"});
                    $('#payment_a').attr('disabled','disabled');
                }
            }
        });
    }
});

