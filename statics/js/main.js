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


function abrir_registro_nivel_modal(url){
  $("#AbirModal").load(url, function (){ 
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
    console.log(datos)
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
        }).then(function(){
          location.reload()
        })
        
      },
      error: function(errores){
        $(".formEstudianteUpdate").find('.error_text').text('');
        $(".formEstudianteUpdate").find('.is-invalid').removeClass('is-invalid');
        $("#icon_danger_ESTUDIANTE").css("display","none")
        $("#icon_danger_ACUDIENTE").css("display","none")
        $("#icon_danger_EMERGENCIA").css("display","none")
        $("#icon_danger_DOCUMENTOS").css("display","none")
        errors = errores.responseJSON["errores"]
        pestañas = {
          "info_estudiante":["nombre_completo","fecha_nacimiento","documento","celular","telefono","email","direccion","barrio","seguro_medico","documento_identidad","ciudad"],
          "info_acudiente":["nombre_completo_acudiente","cedula_acudiente","celular_acudiente","email_acudiente","lugar_expedicion_acudiente"],
          "info_emergencia":["nombre_contactoE","telefono_contactoE","relacion_contactoE"],
          "info_documentos":["documento_A","seguro_A","exoneracion"]
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
        for(campo in pestañas["info_documentos"]){
          if (pestañas["info_emergencia"][campo] in errors){
            $("#icon_danger_DOCUMENTOS").css("display","inline-block")
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
        }).then(function(){
         location.reload()
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
function RegistrarEstudianteSinRegistroClasePuntual(){
  let form = $("#RegistrarEstudianteForm")
  $.ajax({
    url: form.attr("action"),
    data: form.serialize(),
    type: form.attr("method"),
    success: function (response) {
      location.reload()
    },
    error: function(errores){
      errors = errores.responseJSON["errores"]
      console.log(errors)
      form.find('.text-danger').text('');
      form.find('.is-invalid').removeClass('is-invalid');
      for (let i in errors){
        let x=form.find('input[name='+i+']')
        let y=form.find('select[name='+i+']')
        x.addClass("is-invalid")
        y.addClass("is-invalid")
        $("#"+i).text(errors[i])
    }
    }
  });
 }
function RegistrarEstudianteSinRegistro(forj){
  let form = $("#RegistrarEstudianteForm")
  let p = document.getElementById('horarios-p')
  let div = document.getElementById('horarios')
  div.style.border = "1px solid #ced4da"
  p.style.display="none"
  try {
    let div = document.getElementById('Calendario'+errors['identificador'])
    document.getElementById('pCalendario').remove()
    div.childNodes[0].classList.remove("is-invalid")
    div.childNodes[2].classList.remove("is-invalid")
  } catch (error) {
    
  }
  div = forj.parentNode.childNodes[21]
  calendario = [[],[]]
  for (let i = 0; i < div.childNodes.length; i++) {
    if (i>0) {
      calendario[0].push(div.childNodes[i].firstChild.value)
      calendario[1].push(div.childNodes[i].lastChild.value)
    }
  }
  csrfT=forj.parentNode.childNodes[1]
  inicioClase = forj.parentNode.childNodes[13]
  meses = forj.parentNode.childNodes[29]
  profesor = forj.parentNode.childNodes[37]
  nivel =  forj.parentNode.childNodes[45]
  pago = forj.parentNode.childNodes[51].childNodes[3]
  idEs = forj.parentNode.childNodes[57].value
  $.ajax({
    url: form.attr("action"),
    data: {
      'csrfmiddlewaretoken':csrfT.value,
      'inicioClase':inicioClase.value,
      'meseSus':meses.value,
      'profesor':profesor.value,
      'nivel':nivel.value,
      'horaClase':JSON.stringify(calendario[1]),
      'diaClase':JSON.stringify(calendario[0]),
      'estudiante':idEs,
      "pagado":JSON.stringify(pago.checked)
    },
    type: form.attr("method"),
    success: function (response) {
      location.reload()
    },
    error: function(errores){
      form.find('.text-danger').text('');
      form.find('.is-invalid').removeClass('is-invalid');
      errors = errores.responseJSON["errores"]
      console.log(errors)
      try {
        if (errors['identificador']==null){
          let p = document.getElementById('horarios-p')
          let div = document.getElementById('horarios')
          if(errors['Calendario']==undefined){
            p.innerHTML = 'Este campo es obligatorio'
          }else{
            p.innerHTML = errors['Calendario']
          }
          p.style.color = "#dc3545"
          p.style.display = "block"
          div.style.border = "1px solid #dc3545"
        }
        let div = document.getElementById('Calendario'+errors['identificador'])
        let pCalendario = document.createElement("p");
        pCalendario.innerHTML = errors['Calendario']
        pCalendario.style.color = "#dc3545"
        pCalendario.id = "pCalendario"
        div.appendChild(pCalendario)
        div.childNodes[0].classList.add("is-invalid")
        div.childNodes[2].classList.add("is-invalid")
      } catch (error) {
        form.find('.text-danger').text('');
        form.find('.is-invalid').removeClass('is-invalid');
        for (let i in errors){
          let x=form.find('input[name='+i+']')
          let y=form.find('select[name='+i+']')
          x.addClass("is-invalid")
          y.addClass("is-invalid")
          $("#"+i).text(errors[i]) 
      }
    }
    }
  });
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

function ModificarNivel(){
  let form = $("#ModificarNivelForm")
  console.log(form.attr('action'),form.attr('method'),form.serialize())
  $.ajax({
    url: form.attr('action'),
    type: form.attr('method'),
    data: form.serialize(),
    success: function(){
      Swal.fire(
        'HECHO',
        'Nivel modificado',
        'success'
      ).then(function(){
        location.reload()
      })
    },
    error: function(){
      form.find('.error_text').text('');
      form.find('.is-invalid').removeClass('is-invalid');
      for (let i in errors){
        let x=form.find('input[name='+i+']')
        x.addClass("is-invalid")
        $("#"+i).text(errors[i])
    }
    },
  })
}


function CraerNivel(){
  let form = $("#CrearcarNivelForm")
  console.log(form.attr('action'),form.attr('method'),form.serialize())
  $.ajax({
    url: form.attr('action'),
    type: form.attr('method'),
    data: form.serialize(),
    success: function(){
      Swal.fire(
        'HECHO',
        'Nivel Creado',
        'success'
      ).then(function(){
        location.reload()
      })
    },
    error: function(){
      form.find('.error_text').text('');
      form.find('.is-invalid').removeClass('is-invalid');
      for (let i in errors){
        let x=form.find('input[name='+i+']')
        x.addClass("is-invalid")
        $("#"+i).text(errors[i])
    }
    },
  })
}

function abrir_modal_calendario(url){
  $("#ModalInfoEstudianteCalendario").load(url, function (){ 
    $(this).appendTo("body").modal('show');
  });
}


function Borrar_Nivel(url, id){
  const swalWithBootstrapButtons = Swal.mixin({
      customClass: {
        confirmButton: 'btn btn-success',
        cancelButton: 'btn btn-danger'
      },
      buttonsStyling: false
    })
  
    swalWithBootstrapButtons.fire({
      title: '¿Estas Seguro?',
      text: "¡Se borrará el Nivel, esta acción no se puede deshacer, los estudiantes y picaderos que tengan este nivel quedaran sin uno.",
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
          'Se ha borrado Este nivel',
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
        )
      }
    })
}
// let tables = document.querySelectorAll('table')
// for (let i = 0; i < tables.length; i++) {
//   tables[i].classList.add('display')
//   tables[i].classList.add('nowrap')
//   tables[i].cellspacing="0"
//   tables[i].width = "100%"
//   console.log(tables[i])
// }