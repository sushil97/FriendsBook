window.onload = function() {
 const myInput = document.getElementById('login[password]');
 if (myInput!=null) {
     myInput.onpaste = function (e) {
         e.preventDefault();
     }
 }
}
function showkeyboard() {
    document.getElementById('keyboard').style.display="block";
}
function hidekeyboard()
{
    document.getElementById('keyboard').style.display="none";
}