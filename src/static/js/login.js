$(document).ready(function() {
    $(".btn-enviar").click(function(){
	var email = $('#email').val();
	var pass = $('#password').val()
	var ExpresionEmail=/^[a-zA-Z0-9\._-]+@[a-zA-Z0-9-]{2,}[.][a-zA-Z]{2,4}$/;
	var Expresionpassword=/^[A-Za-z0-9\s]{3,25}$/g
	if (!ExpresionEmail.test(email)){
		$('#errorAlert').text('pon un correo válido').show();
		return false;
		} else {
			if (!Expresionpassword.test(pass)) {
					$('#errorAlert').text('pon una contraseña (solo texto)').show();
							return false;
			} else {
							return true;
						}
		}
	});
	$('form').on('submit', function(event) {
        
        $.ajax({
            data : {
				email : $('#email').val(),
				password : $('#password').val()
            },
            type : 'POST',
            url : '/login'
        })
        .done(function(data) {
            if (data.error) {
                $('#errorAlert').text(data.error).show();
                $('#cform')[0].reset();
				
            }
			else {
				
				window.location.href = "http://" + window.location.host + "";
			}
         
 
        });
        event.preventDefault();
    });
});
