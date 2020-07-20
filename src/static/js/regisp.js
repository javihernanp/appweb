$(document).ready(function() {
	$(".btn-add-product").click(function(){
		var nombre = $('#nombre').val();
		var precio = $('#precio').val();
		var tipo = $('#tipo').val();
		var descripcion = $('#descripcion').val();
		var cantidad = $('#cantidad').val();
		var Expresiontexto=/^[A-Za-z0-9\s]{3,25}$/;
		var textoLargo=/^[A-Za-z0-9\s]{3,150}$/;
		var Expresionnumero=/^[0-9]{1,9}$/;
		if (!Expresiontexto.test(nombre)){
			$('#errorAlert').text('Pon un nombre correcto').show();
			return false;
			} else {
				if (!Expresionnumero.test(precio)){
					$('#errorAlert').text('Pon un precio válido').show();
					return false;
					} else {
						if (!Expresiontexto.test(tipo)){
							$('#errorAlert').text('Pon un tipo correcto').show();
							return false;
							} else {
								if (!textoLargo.test(descripcion)){
									$('#errorAlert').text('Pon un descripcion válida').show();
									return false;
									} else {
										if (!Expresionnumero.test(cantidad)){
											$('#errorAlert').text('Pon una cantidad válida').show();
											return false;
											} else {
												return true;
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
                precio : $('#precio').val(),
				tipo : $('#tipo').val(),
                descripcion : $('#descripcion').val(),
                cantidad : $('#cantidad').val()
            },
            type : 'POST',
            url : '/pad'
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