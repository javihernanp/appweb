$(document).ready(function() {
	$(".btn-update-product").click(function(){
		var nombre = $('#nombre').val();
		var precio = $('#precio').val();
		var tipo = $('#tipo').val();
		var descripcion = $('#descripcion').val();
		var cantidad = $('#cantidad').val();
		var Expresiontexto=/^[A-Za-z0-9\s]{3,25}$/;
		var Expresionnumero=/^[0-9]{1,9}$/;
		var textoLargo=/^[A-Za-z0-9\s]{3,150}$/;
		if (!Expresiontexto.test(nombre)){
			$('#errorAlert').text('pon un nombre correcto').show();
			return false;
			} else {
				if (!Expresionnumero.test(precio)){
					$('#errorAlert').text('pon un precio válido').show();
					return false;
					} else {
						if (!Expresiontexto.test(tipo)){
							$('#errorAlert').text('pon un tipo correcto').show();
							return false;
							} else {
								if (!textoLargo.test(descripcion)){
									$('#errorAlert').text('pon un descripcion válida').show();
									return false;
									} else {
										if (!Expresionnumero.test(cantidad)){
											$('#errorAlert').text('pon una cantidad válida').show();
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
            url : '/updateproducto'
        })
        .done(function(data) {
            if (data.error) {
                $('#errorAlert').text(data.error).show();
                $('#successAlert').hide();
                
				
            } else {
                $('#successAlert').text(data.name).show();
                $('#errorAlert').hide();
				
                
            }
            
 
        });
        event.preventDefault();
    });
});