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
    $(this).appendTo("body").modal('show');
  });
}


function abrir_registro_nivel_modal(url){
  $("#AbirModal").load(url, function (){ 
    $(this).appendTo("body").modal('show');
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
function modificarDocsEstudiante() { 
  event.preventDefault()
  form = $("#modificarDocsEstudiante")
  let spinner = $("#spinnerLoad")
  form.css("display", "none")
  spinner.removeClass("ocultar")
  form.submit()
 }

function ModificarRegistroEstudiante(){
  let form = $("#ModificarRegistroEstudianteForm")
  let p = document.getElementById('horarios-p')
  let div = document.getElementById('horarios')
  div.style.border = "1px solid #ced4da"
  p.style.display="none"
  try {
    let div = document.getElementById('Calendario'+errors['identificador'])
    document.getElementById('pCalendario').remove()
    div.childNodes[0].classList.remove("is-invalid")
    div.childNodes[1].classList.remove("is-invalid")
  } catch (error) {
    
  }
  calendario = [[],[]]
  for (let i = 0; i < div.childNodes.length; i++) {
    if (i>0) {
      calendario[0].push(div.childNodes[i].firstChild.value)
      calendario[1].push(div.childNodes[i].lastChild.value)
    }
  }
  csrfT=document.getElementById('ModificarRegistroEstudianteForm').childNodes[1]
  inicioClase = document.getElementsByName('inicioClase')[0]
  meses = document.getElementsByName('meseSus')[0]
  profesor = document.getElementsByName('profesor')[0]
  nivel = document.getElementsByName('nivel')[0]
  pago = document.getElementsByName('pagado')[0]
  idEs = document.getElementsByName('estudiante')[0]
  servicio = document.getElementsByName('tipo_servicio')[0]
  // console.log(servicio)
  let ruta = window.location.href.split('/')
  let id = ruta[ruta.length-1]
  if(isNaN(ruta[ruta.length-1])==true){
      id = ruta[ruta.length-1].split('?')[0]
  }
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
      'estudiante':idEs.value,
      "pagado":JSON.stringify(pago.checked),
      "servicio":servicio.value,
      'idEstudiante':id
    },
    type: form.attr("method"),
    success: function (response) {
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
      // location.reload()
    },
    error: function(errores){
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
      console.log(errors)
        let div = document.getElementById('Calendario'+errors['identificador'])
        let pCalendario = document.createElement("p");
        pCalendario.innerHTML = errors['Calendario']
        pCalendario.style.color = "#dc3545"
        pCalendario.id = "pCalendario"
        div.appendChild(pCalendario)
        div.childNodes[0].classList.add("is-invalid")
        div.childNodes[1].classList.add("is-invalid")
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

function ModificarRegistroEstudiantej(){
  let form = $("#ModificarRegistroEstudianteForm")
  let servicio = document.getElementsByName('tipo_servicio')[0]
  let datos = form.serializeArray()
  let dias = []  
  let horas = []
  let profesor = ''
  let nivel = ''
  let pagado = ''
  let estudiante = ''
  let ruta = window.location.href.split('/')
  let id = ruta[ruta.length-1]
  if(isNaN(ruta[ruta.length-1])==true){
      id = ruta[ruta.length-1].split('?')[0]
  }
  for (let i = 0; i < datos.length; i++) {
        if(datos[i].name=='inicioClase'){
          dias.push(datos[i].value)
        }
        if(datos[i].name=='horaClase'){
          console.log(datos[i])
          horas.push(datos[i].value)
        }
        if(datos[i].name=='profesor'){
          profesor = datos[i].value
        }
        if(datos[i].name=='nivel'){
          nivel = datos[i].value
        }
        if(datos[i].name=='pagado'){
          pagado = datos[i].value
        }
        if(datos[i].name=='estudiante'){
          estudiante = datos[i].value
        }
    }
  $.ajax({
    url:form.attr("action"),
    type:form.attr("method"),
    data: {
      'csrfmiddlewaretoken':datos[0].value,
      'diaClase':dias,
      'profesor':profesor,
      'nivel':nivel,
      'horaClase':horas,
      'estudiante':estudiante,
      "pagado":pagado,
      "servicio":servicio.value,
      'idEstudiante':id
    },
    success: function(){
        console.log('hola')
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
      errors = errores.responseJSON["errores"]
      console.log(errors)
      form.find('.text-danger').text('');
      form.find('.is-invalid').removeClass('is-invalid');
      for (let i in errors){
        if (i == 'horarios'){
          Swal.fire({
            title: '<strong>Atención</strong>',
            icon: 'info',
            html:
              'Se han puesto más de 5 clases, recuerde que este registro es del tipo <b>Clase Puntual</b> por lo que agregar más clases no lo convertirá en una mensualidad.',
            showCloseButton: true,
            showCancelButton: false,
            focusConfirm: false,
            confirmButtonText:
              '<i class="fa fa-thumbs-up"></i> Si, entendí',
          })
        }
          else{
          let x=form.find('input[name='+i+']')
          let y=form.find('select[name='+i+']')
          if(x.length == 0 && y.length == 0){
            x = form.find('input[idPer='+i+']')
            console.log(x, i)
            y = form.find('select[idPer='+i+']')
            x[0].parentNode.parentNode.parentNode.classList.add('form-control')
            x[0].parentNode.parentNode.parentNode.classList.add('is-invalid')
          }
          x.addClass("is-invalid")
          y.addClass("is-invalid")
          $("#"+i).text(errors[i])
      }
    }
    },
  })
}
function RegistrarEstudianteSinRegistroClasePuntual(){
  let form = $("#RegistrarEstudianteForm")
  let datos = form.serializeArray()
  let dias = []  
  let horas = []
  let profesor = ''
  let nivel = ''
  let pagado = ''
  let estudiante = ''
  for (let i = 0; i < datos.length; i++) {
        if(datos[i].name=='inicioClase'){
          dias.push(datos[i].value)
        }
        if(datos[i].name=='horaClase'){
          console.log(datos[i])
          horas.push(datos[i].value)
        }
        if(datos[i].name=='profesor'){
          profesor = datos[i].value
        }
        if(datos[i].name=='nivel'){
          nivel = datos[i].value
        }
        if(datos[i].name=='pagado'){
          pagado = datos[i].value
        }
        if(datos[i].name=='estudiante'){
          estudiante = datos[i].value
        }
    }
  $.ajax({
    url: form.attr("action"),
    data: {
      'csrfmiddlewaretoken':datos[0].value,
      'diaClase':dias,
      'horaClase':horas,
      'profesor':profesor,
      'nivel':nivel,
      'pagado':pagado,
      'estudiante':estudiante
    },
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
        if (i == 'horarios'){
          Swal.fire({
            title: '<strong>Atención</strong>',
            icon: 'info',
            html:
              'Se han puesto más de 5 clases, recuerde que este registro es del tipo <b>Clase Puntual</b> por lo que agregar más clases no lo convertirá en una mensualidad.',
            showCloseButton: true,
            showCancelButton: false,
            focusConfirm: false,
            confirmButtonText:
              '<i class="fa fa-thumbs-up"></i> Si, entendí',
          })
        }
          else{
          let x=form.find('input[name='+i+']')
          let y=form.find('select[name='+i+']')
          if(x.length == 0 && y.length == 0){
            x = form.find('input[idPer='+i+']')
            console.log(x)
            y = form.find('select[idPer='+i+']')
            x[0].parentNode.parentNode.parentNode.classList.add('form-control')
            x[0].parentNode.parentNode.parentNode.classList.add('is-invalid')
          }
          x.addClass("is-invalid")
          y.addClass("is-invalid")
          $("#"+i).text(errors[i])
      }
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
  calendario = [[],[]]
  for (let i = 0; i < div.childNodes.length; i++) {
    if (i>0) {
      calendario[0].push(div.childNodes[i].firstChild.value)
      calendario[1].push(div.childNodes[i].lastChild.value)
    }
  }
  csrfT=document.getElementById('RegistrarEstudianteForm').childNodes[1]
  inicioClase = document.getElementsByName('inicioClase')[0]
  meses = document.getElementsByName('meseSus')[0]
  profesor = document.getElementsByName('profesor')[0]
  nivel = document.getElementsByName('nivel')[0]
  pago = document.getElementsByName('pagado')[0]
  idEs = document.getElementsByName('estudiante')[0]
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
      'estudiante':idEs.value,
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

  
function cambiar_estado_usuario(id){
  let ids = id
  let token = $("#EstadoUsuarioForm").find('input[name=csrfmiddlewaretoken]').val()
  const swalWithBootstrapButtons = Swal.mixin({
    customClass: {
      confirmButton: 'btn btn-success',
      cancelButton: 'btn btn-danger'
    },
    buttonsStyling: false
  })

  swalWithBootstrapButtons.fire({
    title: '¿Estas Seguro?',
    text: "¡Se cambiará el estado del usuario por lo que ya no podrá iniciar sesión.!",
    icon: 'warning',
    showCancelButton: true,
    confirmButtonText: '¡Si, Modificar!',
    cancelButtonText: '¡No, Cancelar!',
    confirmButtonClass: "buttonSweetalert",
    reverseButtons: true
  }).then((result) => {
    if (result.isConfirmed) {
      $(document).ready(function() {
        $.ajax({
            data: { "csrfmiddlewaretoken": token, "estado": ids },
            url: $("#EstadoUsuarioForm").attr('action'),
            type: $("#EstadoUsuarioForm").attr('method'),
            success: function(datas) {
                swal.fire("¡OK! Se ha modificado el usuario", {
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

function cambiar_estado_estudiante(url, id){
  let ids = id
  let token = csrftoken
  const swalWithBootstrapButtons = Swal.mixin({
    customClass: {
      confirmButton: 'btn btn-success',
      cancelButton: 'btn btn-danger'
    },
    buttonsStyling: false
  })

  swalWithBootstrapButtons.fire({
    title: '¿Estas Seguro?',
    text: "¡Se cambiará el estado del alumno por lo que ya no aparecera en ninguna otra parte.!",
    icon: 'warning',
    showCancelButton: true,
    confirmButtonText: '¡Si, Modificar!',
    cancelButtonText: '¡No, Cancelar!',
    confirmButtonClass: "buttonSweetalert",
    reverseButtons: true
  }).then((result) => {
    if (result.isConfirmed) {
      $(document).ready(function() {
        $.ajax({
            data: { "csrfmiddlewaretoken": token, "id": ids },
            url: url,
            type: 'POST',
            success: function(datas) {
                swal.fire("¡OK! Se ha modificado el alumno", {
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