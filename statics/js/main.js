// funcion que devulve el csrf token de django
function getToken(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}
const csrftoken = getToken('csrftoken');

function changePass(url){
    $("#CambiarContrasena").load(url, function (){ 
      $(this).appendTo("body").modal('show');
    });
}

function EstudianteSinRegistro(url){
  $("#EstudianteSinRegistroModal").load(url, function (){ 
    $(this).modal('show');
  });
}


function ModificarEstudiante(url){
  let forms = document.getElementsByClassName('formEstudianteUpdate')
    datos={}
    for (let i = 0; i < forms.length; i++) {
        inputs = forms[i].getElementsByTagName('input')
        selects = forms[i].getElementsByTagName('select')
        for (let i = 0; i < inputs.length; i++) {
            datos[inputs[i].name]=inputs[i].value
        }
        for (let i = 0; i < selects.length; i++) {
            datos[selects[i].name]=selects[i].value
        }
    }
    $.ajax({
      url: url,
      type: "POST",
      data:datos,
      success: function(data){
        $(".formEstudianteUpdate").find('.error_text').text('');
        $(".formEstudianteUpdate").find('.is-invalid').removeClass('is-invalid');
        $("#icon_danger_ESTUDIANTE").css("display","none")
        $("#icon_danger_ACUDIENTE").css("display","none")
        $("#icon_danger_EMERGENCIA").css("display","none")
        Swal.fire({
          position: 'top-end',
          icon: 'success',
          title: 'Estudiante Modificado',
          showConfirmButton: false,
          timer: 2000
        })
      },
      error: function(errores){
        $(".formEstudianteUpdate").find('.error_text').text('');
        $(".formEstudianteUpdate").find('.is-invalid').removeClass('is-invalid');
        $("#icon_danger_ESTUDIANTE").css("display","none")
        $("#icon_danger_ACUDIENTE").css("display","none")
        $("#icon_danger_EMERGENCIA").css("display","none")
        errors = errores.responseJSON["errores"]
        pestañas = {
          "info_estudiante":["nombre_completo","fecha_nacimiento","documento","celular","telefono","email","direccion","barrio","seguro_medico","documento_identidad","ciudad","nivel"],
          "info_acudiente":["nombre_completo_acudiente","cedula_acudiente","celular_acudiente","email_acudiente","lugar_expedicion_acudiente"],
          "info_emergencia":["nombre_contactoE","telefono_contactoE","relacion_contactoE"]
        }

        for(campo in pestañas["info_estudiante"]){
          if (pestañas["info_estudiante"][campo] in errors){
            $("#icon_danger_ESTUDIANTE").css("display","inline-block")
            break
          }
        }
        for(campo in pestañas["info_estudiante"]){
          if (pestañas["info_acudiente"][campo] in errors){
            $("#icon_danger_ACUDIENTE").css("display","inline-block")
            break
          }
        }
        for(campo in pestañas["info_estudiante"]){
          if (pestañas["info_emergencia"][campo] in errors){
            $("#icon_danger_EMERGENCIA").css("display","inline-block")
            break
          }
        }

        for (let i in errors){
          let x=$(".formEstudianteUpdate").find('input[name='+i+']')
          let y=$(".formEstudianteUpdate").find('select[name='+i+']')
          x.addClass("is-invalid")
          y.addClass("is-invalid")
          $("#"+i).text(errors[i])
      }
        
      },
    })
}

function ModificarRegistroEstudiante(){
  let form = $("#ModificarRegistroEstudianteForm")
  $.ajax({
    url:form.attr("action"),
    type:form.attr("method"),
    data:form.serialize(),
    success: function(){
        form.find('.error_text').text('');
        form.find('.is-invalid').removeClass('is-invalid');
        $("#icon_danger_REGISTRO").css("display","none")
        Swal.fire({
          position: 'top-end',
          icon: 'success',
          title: 'Registro del Estudiante Modificado',
          showConfirmButton: false,
          timer: 2000
        })
    },
    error: function(errores){
      form.find('.error_text').text('');
      form.find('.is-invalid').removeClass('is-invalid');
      $("#icon_danger_REGISTRO").css("display","inline-block")
      errors = errores.responseJSON["errores"]
      for (let i in errors){
        let x=form.find('input[name='+i+']')
        let y=form.find('select[name='+i+']')
        x.addClass("is-invalid")
        y.addClass("is-invalid")
        $("#"+i).text(errors[i])
    }
    },
  })
}

function cambiar_estado_estudiante(url,id){
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
      console.log(csrftoken)
     $.ajax({
      url:url,
      type:"POST",
      data:{"csrfmiddlewaretoken":csrftoken,"id":id},
      success: function(){
         swalWithBootstrapButtons.fire(
        'Modificado!',
        'El estado del estudiante se ha modificado',
        'success'
      )
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

function cambiar_estado_usuario(id){
  let ids = id
    let token = $("#EstadoUsuarioForm").find('input[name=csrfmiddlewaretoken]').val()
    swal.fire({
        title: "¿Estás seguro?",
        text: "Se modificara el estado del Usuario",
        icon: "warning",
        buttons: {
            confirm: { text: 'Confirmar', className: 'btn-success' },
            cancel: 'Cancelar'
        },
        dangerMode: true,
    }).then((changeStatus) => {
        if (changeStatus) {
            $(document).ready(function() {
                $.ajax({
                    data: { "csrfmiddlewaretoken": token, "estado": ids },
                    url: $("#EstadoUsuarioForm").attr('action'),
                    type: $("#EstadoUsuarioForm").attr('method'),
                    success: function(datas) {
                        swal.fire("¡OK! Se ha modificado el Usuario", {
                            icon: "success",
                        }).then(function() {
                            location.reload()
                        });
                    },
                    error: function(error) {
                      Error = error['responseJSON']
                      Swal.fire({
                          icon: 'info',
                          title: 'Atención.',
                          text: Error['error'] + '.',
                      })
                    }
                });
            })
        } else {
            swal("¡OK! Ningún dato del usuario ha sido modificado").then(function() {
                location.reload()
            });

        }
    });
}