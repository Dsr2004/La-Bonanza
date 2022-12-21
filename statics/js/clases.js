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



// Horarios Puntuales
let containerCards = document.getElementsByClassName('containerPuntual')[0]
function cargarSize(){  
    var nth = document.querySelector(".containerPuntual div:nth-child(1)")
    nth.style.gridRow = '1/'+containerCards.childElementCount
    nth.style.overflow = 'auto'
    if (containerCards.childElementCount == 2) {
        containerCards.style.gridTemplateRows = "100%"
    }
    else{
        if (containerCards.childElementCount == 3) {
            containerCards.style.gridTemplateRows = '65%'
        }
        if (containerCards.childElementCount == 4) {
            containerCards.style.gridTemplateRows = '30%'
        }
        if (containerCards.childElementCount > 4) {
            containerCards.style.gridTemplateRows = (100/containerCards.childElementCount)+'%'
        }
    }
}
cargarSize()
function act(toggle){
    let cardsToggle = document.querySelectorAll('.toggleView')
    cardsToggle.forEach(reload => {
        if(reload.childNodes[1].classList.contains('fa-compress')){
            reload.parentElement.lastElementChild.lastElementChild.style.display = 'none'
            reload.childNodes[1].classList.remove('fa-compress')
            reload.childNodes[1].classList.add('fa-expand')
            reload.childNodes[1].style.visibility= 'visible';
            if(reload.parentElement.lastElementChild.firstElementChild.classList.contains('center') == false){
                reload.parentElement.lastElementChild.firstElementChild.classList.toggle('center')
            }
        }
        else{
            if(reload.parentElement.lastElementChild.firstElementChild.classList.contains('center') == false){
                reload.parentElement.lastElementChild.firstElementChild.classList.toggle('center')
            }
        }
    })
    if(toggle.childNodes[1].classList.contains('fa-compress')){
        toggle.childNodes[1].classList.remove('fa-compress')
        toggle.childNodes[1].classList.add('fa-expand')
        toggle.childNodes[1].style.visibility= 'visible';
    }
    else{
        toggle.childNodes[1].classList.add('fa-compress')
        toggle.childNodes[1].style.visibility= 'hidden';
        toggle.childNodes[1].classList.remove('fa-expand')
        toggle.parentElement.lastElementChild.lastElementChild.style.display = 'block'
    }
    if(toggle.parentElement.lastElementChild.firstElementChild.classList.contains('center')){
        toggle.parentElement.lastElementChild.firstElementChild.classList.toggle('center')
    }
    let card = toggle.parentElement.cloneNode(true)
    containerCards.firstElementChild.style.gridRow = ""
    containerCards.removeChild(toggle.parentElement)
    containerCards.insertBefore(card,containerCards.firstChild)
    cargarSize()
}
function eliminarClase(){
    if(containerCards.childElementCount > 1){
        containerCards.removeChild(containerCards.lastElementChild)
        cargarSize()
    }
}
function agregarClase(){
    let clone = containerCards.lastElementChild.cloneNode(true)
    clone.style.gridRow = ""
    clone.style.overflow = ""
    clone.lastElementChild.firstElementChild.innerHTML = "Horario "+(containerCards.childElementCount+1)
    clone.lastElementChild.lastElementChild.childNodes[3].value = ""
    clone.lastElementChild.lastElementChild.childNodes[9].value = ""
    clone.lastElementChild.lastElementChild.style.display = "none"
    clone.firstElementChild.style.visibility="visible"
    clone.lastElementChild.lastElementChild.childNodes[3].setAttribute('idPer', "inicioClase"+(containerCards.childElementCount+1))
    clone.lastElementChild.lastElementChild.childNodes[9].setAttribute('idPer', "horaClase"+(containerCards.childElementCount+1))
    clone.lastElementChild.lastElementChild.childNodes[5].id="inicioClase"+(containerCards.childElementCount+1)
    clone.lastElementChild.lastElementChild.childNodes[11].id="horaClase"+(containerCards.childElementCount+1)
    clone.classList.remove('is-invalid')
    containerCards.appendChild(clone)
    cargarSize()
}
  