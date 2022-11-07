function abrir_modal_reponer_clase(url){
    $("#reponerClasesModal").load(url, function (){ 
        $(this).appendTo("body").modal('show');
      });
}
function reponerClases() {
  let form = $("#reponerClaseForm")
  console.log(form.attr("action"))
  console.log(form.serialize())

  $.ajax({
    url: form.attr("action"),
    type: "POST",
    data: form.serialize(),
    success: function (response) {
      Swal.fire({
        position: 'top-end',
        icon: 'success',
        title: 'La clase ha sido modificadá',
        showConfirmButton: false,
        timer: 2000
      }).then(function(){
       location.reload()
      })
    },
    error: function(errores){
      form.find('.error_text').text('');
      form.find('.is-invalid').removeClass('is-invalid');
      errors = errores.responseJSON["errores"]
      console.log(errors)
      for (let i in errors){
        let x=form.find('input[name='+i+']')
        let y=form.find('select[name='+i+']')
        x.addClass("is-invalid")
        y.addClass("is-invalid")
        $("#error"+i).text(errors[i])
    }
    }
  });
}
