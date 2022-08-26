function changePass(url){
    $("#CambiarContrasena").load(url, function (){ 
      $(this).appendTo("body").modal('show');
    });
}