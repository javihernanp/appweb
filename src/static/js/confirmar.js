$(document).ready(function () {
$(".btn-delete").click(function(){
    if (!confirm("¿Estas seguro de que deseas borrarlo?")){
      return false;
    }
  });
  $(".btn-delete-tabla").click(function(){
    if (!confirm("¿Estas seguro de que deseas restaurar la tabla productos?, Se vaciara los datos de todos los carritos")){
      return false;
    }
  });
  $(".btn-delete-product").click(function(){
    if (!confirm("¿Estas seguro de que deseas borrar el producto?")){
      return false;
    }
  });
});