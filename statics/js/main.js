function changePass(url){
    $("#CambiarContrasena").load(url, function (){ 
      $(this).appendTo("body").modal('show');
    });
}

function EstudianteSinRegistro(url){
  $("#CambiarContrasena").load(url, function (){ 
    $(this).appendTo("body").modal('show');
  });
}