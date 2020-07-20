$(document).ready(function() {
    
	
	$(".btn-enviar").click(function(){
		var nombre = $('#nombre').val();
		var apellido = $('#apellido').val();
		var dni = $('#dni').val();
		var direccion = $('#direccion').val();
		var phone = $('#phone').val();
		var email = $('#email').val();
		var pass = $('#password').val();
		var ExpresionTexto=/^[a-zA-Z]{3,25}$/;
		var ExpresionEmail=/^[a-zA-Z0-9\._-]+@[a-zA-Z0-9-]{2,}[.][a-zA-Z]{2,4}$/;
		var NIF=/^\d{8}[a-zA-Z]{1}$/;
		var Expresionpassword=/^[A-Za-z0-9\s]{3,25}$/
		var ExpresionPhone=/^[0-9]{9}$/;
		if (!ExpresionTexto.test(nombre)){
				$('#errorAlert').text('pon un nombre correcto').show();
				return false;
		} else {
			if (!ExpresionTexto.test(apellido)){
				$('#errorAlert').text('pon un apellido correcto').show();
				return false;
				
				} else {
					if (!NIF.test(dni)){
						$('#errorAlert').text('pon un dni válido').show();
						return false;
						} else {
							letra = 'TRWAGMYFPDXBNJZSQVHLCKE';
							numero = dni.substr(0,dni.length-1);
							letr = dni.substr(dni.length-1,1);
							numero = numero % 23;
							letra=letra.substring(numero,numero+1);
							if (letra!=letr.toUpperCase()) {
								$('#errorAlert').text('La letra del DNI esta mal').show();
								return false;
							} else {
								if (!ExpresionTexto.test(direccion)){
									$('#errorAlert').text('pon una direccion válida').show();
									return false;
								} else{
										if (!ExpresionPhone.test(phone)){
											$('#errorAlert').text('pon un número válido').show();
											return false;
										} else {
											if (!ExpresionEmail.test(email)){
												$('#errorAlert').text('pon un correo válido').show();
												return false;
											} else {
												if (!Expresionpassword.test(pass)) {
													$('#errorAlert').text('pon una contraseña minimo 3 caracteres)').show();
													return false;
												} else {
													return true;
												}
											}
										}
									}
							}
						
						
						}
				

				
				}
		

		}	
	});
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	$('form').on('submit', function(event) {   
			$.ajax({
				data : {
					name : $('#nombre').val(),
					apellido : $('#apellido').val(),
					dni : $('#dni').val(),
					direccion : $('#direccion').val(),
					phone : $('#phone').val(),
					email : $('#email').val(),
					password : $('#password').val()
					},
					type : 'POST',
					url : '/process'
				})
				.done(function(data) {
					if (data.error) {
						$('#errorAlert').text(data.error).show();
						$('#successAlert').hide();
                
				
					} else {
						$('#successAlert').text(data.name).show();
						$('#errorAlert').hide();
						$('#cform')[0].reset();
                
					}
 
				});
        event.preventDefault();
    });
});


