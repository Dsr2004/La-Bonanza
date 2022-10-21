function abrir_modal_crear_picadero(url){
    $("#crearPicaderoModal").load(url, function (){ 
        $(this).appendTo("body").modal('show');
      });
}

function CrearPicadero(){
    form = $("#crearPicaderoForm")
    
    $.ajax({
        url: form.attr("action"),
        type: form.attr("method"),
        data: form.serialize(),
        success: function (response) {
           location.reload() 
        },
        error: function(data){
            form.find('.error_text').text('');
            form.find('.is-invalid').removeClass('is-invalid');
            errores = data.responseJSON["errores"]

            for (let i in errores){
                let x=form.find('input[name='+i+']')
                let y=form.find('select[name='+i+']')
                x.addClass("is-invalid")
                y.addClass("is-invalid")
                $("#"+i).text(errores[i])
            }
        }
    });
}