$(function () {
    $('#edit_details').click(function (e) {
        $("#account-form").delay(100).fadeIn(100);
        $("#password-change-form").fadeOut(100);
        $('#change_password_setting').removeClass('active');
        $(this).addClass('active');
        e.preventDefault();
    });
    $('#change_password_setting').click(function (e) {
        $("#password-change-form").delay(100).fadeIn(100);
        $("#account-form").fadeOut(100);
        $('#edit_details').removeClass('active');
        $(this).addClass('active');
        e.preventDefault();
    });
});

function validateAccountPassword() {
    var pass_rex = new RegExp("^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})");
    var mediumRegex = new RegExp("^(((?=.*[a-z])(?=.*[A-Z]))|((?=.*[a-z])(?=.*[0-9]))|((?=.*[A-Z])(?=.*[0-9])))(?=.{6,})");
    var password=document.getElementById('account_password').value;
    if(pass_rex.test(password)){
        document.getElementById('account_password').style.background = "#ccffcc";
        document.getElementById('account_strength').style.color = 'green';
        document.getElementById('account_strength').innerHTML = "Strong Password"
        return true;
    }
    else if(mediumRegex.test(password)){
        document.getElementById('account_password').style.background = "rgba(255,195,0,0.44)";
        document.getElementById('account_strength').style.color = 'orange';
        document.getElementById('account_strength').innerHTML = "Medium Password"
    }
    else{
        document.getElementById('account_password').style.background ='rgba(255,10,0,0.19)';
        document.getElementById('account_strength').style.color = 'red';
        document.getElementById('account_strength').innerHTML = "Weak Password"
        return false;
    }
}
function checkRepassword(){
    var password=document.getElementById('account_password').value;
    var password1=document.getElementById('account_password1').value;
    if(password==password1){
        document.getElementById('account_password1').style.background = "#ccffcc";
        document.getElementById('account_matching_error').style.display = "none";
        document.getElementById('account_strength').style.display = "none";
        return true;
    }
    else{
        document.getElementById('id_password1').style.background='rgba(255,10,0,0.19)';
        document.getElementById('account_matching_error').style.color='red';
        document.getElementById('account_matching_error').innerHTML = "Password doesn't match";
        return false;
    }
}