function abrir_modal_crear_picadero(url){
    $("#crearPicaderoModal").load(url, function (){ 
        $(this).appendTo("body").modal('show');
      });
}

function abrir_modal_modificar_picadero(url){
    $("#modificarPicaderoModal").load(url, function (){ 
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

function ModificarPicadero(){
    
    const swalWithBootstrapButtons = Swal.mixin({
        customClass: {
          confirmButton: 'btn btn-success',
          cancelButton: 'btn btn-danger'
        },
        buttonsStyling: false
      })
    
      swalWithBootstrapButtons.fire({
        title: '¿Estas Seguro?',
        text: "¡Se modificará el estado del estudiante!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: '¡Si, Modificar!',
        cancelButtonText: '¡No, Cancelar!',
        confirmButtonClass: "buttonSweetalert",
        reverseButtons: true
      }).then((result) => {
        if (result.isConfirmed) {
            form = $("#modificarPicaderoForm")
            $.ajax({
                url: form.attr("action"),
                type: form.attr("method"),
                data: form.serialize(),
                success: function(){
                    swalWithBootstrapButtons.fire(
                'Modificado!',
                'El estado del estudiante se ha modificado',
                'success'
                ).then(function(){
                    location.reload()
                })
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
        } else if (
          /* Read more about handling dismissals below */
          result.dismiss === Swal.DismissReason.cancel
        ) {
          swalWithBootstrapButtons.fire(
            'Cancelado',
            'No se han aplicado cambios',
            'error'
          )
        }
      })
}

function Borrar_picadero(url, id){
    const swalWithBootstrapButtons = Swal.mixin({
        customClass: {
          confirmButton: 'btn btn-success',
          cancelButton: 'btn btn-danger'
        },
        buttonsStyling: false
      })
    
      swalWithBootstrapButtons.fire({
        title: '¿Estas Seguro?',
        text: "¡Se borrará el picadero, esta acción no se puede deshacer, y se borrará toda la información de las clases!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: '¡Si, Borrar!',
        cancelButtonText: '¡No, Cancelar!',
        confirmButtonClass: "buttonSweetalert",
        reverseButtons: true
      }).then((result) => {
        if (result.isConfirmed) {
          console.log(csrftoken)
         $.ajax({
          url:url,
          type:"POST",
          data:{"csrfmiddlewaretoken":csrftoken,"id":id},
          success: function(){
             swalWithBootstrapButtons.fire(
            'Borrado!',
            'Se ha borrado toda la información de este Picadero',
            'success'
          ).then(function(){
            location.reload()
          })
          },
          error: function(){
             swalWithBootstrapButtons.fire(
            'ERROR!',
            'ha ocurrido un error.',
            'error'
          )
          },
         })
        } else if (
          /* Read more about handling dismissals below */
          result.dismiss === Swal.DismissReason.cancel
        ) {
          swalWithBootstrapButtons.fire(
            'Cancelado',
            'No se han aplicado cambios',
            'error'
          ).then(function(){
            location.reload()
          })
        }
      })
}