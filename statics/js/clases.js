function abrir_modal_reponer_clase(url){
    $("#reponerClasesModal").load(url, function (){ 
        $(this).appendTo("body").modal('show');
      });
}
function reponerClases(ulr) {}