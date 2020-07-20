
$(document).ready(function () {
	   
       $.ajax({
			url : '/tp',
			dateType: 'json',
			type: 'POST',
			
			success: function(payload) {
				var data = JSON.parse(payload);
				console.log(data);
				
				for (var i in data){
					var person=data[i];
					
					$("tbody").append('<tr><td>'+person.nombre+'</td><td>'+person.precio+'</td><td>'+person.cantidad+"</td><td><a href='/detalles/"+person.id +"'"+"class='btn btn-secondary'>Detalles</a><a href='/comprar/"+person.id +"'"+"class='btn btn-danger'>Comprar</a></td></tr>");
					
				};
				
            }
	   });
	  
	});

	


