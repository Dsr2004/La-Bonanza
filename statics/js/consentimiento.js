titleC="CONSENTIMIENTO PARA ASUMIR RIESGO Y EXONERACION DE RESPONSABILIDAD"
consentimiento = [
    'De la Actividad de apoyo terapéutico, enseñanza deportiva y recreativa de chalanería y actividades ecuestres. Yo reconozco que hay ciertos riesgos, posibles daños y peligros, incluyendo el riesgo de daño físico, o muerte y riesgo de discapacidad o daño a mi propiedad personal, como resultado de permitirme o permitir que mi hijo(a) según sea el caso participe en esta Actividad. Los riesgos incluyen, pero no están limitados a accidentes, peligros relacionados, enfermedades contagiosas, la posibilidad de resbalarse y caerse lo que podría resultar en rasguños, contusiones, esguinces, heridas en la piel, fracturas, conmociones cerebrales, o inclusive peligros severos de debilitamiento o pérdida de la vida. Entiendo que las lesiones o pérdidas podrían resultar de riegos inesperados y por el uso de equipo, materiales, o instalaciones recomendadas por la <b>CLUB DE CHALANERIA Y EQUINOTERAPIA LA BONANZA S.A.S.</b>; condiciones ambientales; de los actos u omisiones de otros; o falta de cuidados médicos inmediatos o cuidados médicos de emergencia adecuados. Entiendo que <b>CLUB DE CHALANERIA Y EQUINOTERAPIA LA BONANZA S.A.S</b>S. no garantiza la salud o seguridad personal de los participantes, ni los protege contra riesgos de pérdidas personales.',
    'Certifico que con conocimiento, he proveído mi información de salud y médica pertinente o mi hijo(a) según sea el caso en el formulario de matrícula, el cual he llenado y firmado. Si yo o mi hijo(a) según sea el caso se lastima o se enferma y/o causa daño a la propiedad de otra persona o personas cuando esté participando en esta Actividad, aceptaré la responsabilidad de todas las pérdidas y cualquier gasto médico, incluyendo co-pagos y deducibles y no pediré reembolso por parte del <b>CLUB DE CHALANERIA Y EQUINOTERAPIA LA BONANZA S.A.S.</b>',
    'Entiendo que el <b>CLUB DE CHALANERIA Y EQUINOTERAPIA LA BONANZA S.A.S.</b> no asume la responsabilidad por eventos que no sean parte de la Actividad descrita anteriormente, o que estén fuera del control del <b>CLUB DE CHALANERIA Y EQUINOTERAPIA LA BONANZA S.A.S.</b>, sus empleados, agentes o voluntarios, o por cualquier otra situación que pueda surgir debido a que él/la participante no provea la información pertinente.',
    'Mi hijo(a) y yo entendemos y aceptamos adherirnos a las Normas de Comportamiento de los estudiandiantes proporcionadas por el <b>CLUB DE CHALANERIA Y EQUINOTERAPIA LA BONANZA S.A.S.</b> Entiendo que el <b>CLUB DE CHALANERIA Y EQUINOTERAPIA LA BONANZA S.A.S.</b> .tiene el derecho de pedirme a mi hijo(a) según sea el caso que abandone esta Actividad, si alguno de los instructores de <b>CLUB DE CHALANERIA Y EQUINOTERAPIA LA BONANZA S.A.S.</b> considera que el comportamiento o acciones representan una amenaza para otros estudiantes de <b>CLUB DE CHALANERIA Y EQUINOTERAPIA LA BONANZA S.A.S.</b>',
    'Afirmo que he revisado y entendido las reglas pertinentes de seguridad suministradas al momento de realizar la inscripción de mi hijo(a) en el <b>CLUB DE CHALANERIA Y EQUINOTERAPIA LA BONANZA S.A.S.</b> En consideración a la participación en la Actividad, exonero de toda responsabilidad al <b>CLUB DE CHALANERIA Y EQUINOTERAPIA LA BONANZA S.A.S.</b>, sus oficiales, empleados, agentes y voluntarios, y renuncio a cualquier demanda que mi hijo(a) o yo podamos presentar, como resultado o que esté relacionada a la Actividad y participación) en la Actividad. Esta exoneración y renuncia también aplican a mis herederos, delegados y representantes.'
]
function verConsentimiento(){
    $("#alertDocumentDownload").hide()
    let div = document.getElementById("fondoConsentimiento");
    div.style.display="block";
    document.getElementById("titleConsentimiento").innerHTML = titleC;
    let content = document.getElementById("contentConsentimiento")
    content.innerHTML = ''
    for (let i = 0; i < consentimiento.length; i++) {
        let contenido = document.createElement("p")
        contenido.innerHTML = consentimiento[i]
        let divC = document.createElement("div")
        divC.appendChild(contenido)
        content.appendChild(divC)
        document.getElementById("CrearEstudianteForm").style.display = "none"
    }
    let contenido = document.createElement("p")
    contenido.innerHTML = "<b>He leído y acepto este consentimiento en su totalidad</b>"
    content.appendChild(contenido)

}
function hideConsentimiento(){
    $("#alertDocumentDownload").show()
    let div = document.getElementById("fondoConsentimiento");
    div.style.display="none";
    document.getElementById("CrearEstudianteForm").style.display = "block"
}
function guardarConsentimiento(){
    let autoriza = document.getElementById("aceptaConsentimiento")
    let auth = autoriza.cloneNode(true);
    auth.id = "aceptaConsentimientoInput"
    auth.style.display="none"
    if (auth.checked) {
        auth.name = 'exoneracion'
        document.getElementById('exoneracion').innerHTML = ''
        document.getElementById('verConsentimientob').classList.remove('btn-warning')
        document.getElementById('verConsentimientob').classList.remove('btn-danger')
        document.getElementById('verConsentimientob').classList.add('btn-success')
        if(document.getElementById("aceptaConsentimientoInput")==null){
            document.getElementById("CrearEstudianteForm").appendChild(auth)
        }else{
            let repl = document.getElementById("aceptaConsentimientoInput")
            document.getElementById("CrearEstudianteForm").replaceChild(auth, repl)
        }
    }
    else{
        document.getElementById('exoneracion').innerHTML = 'Es necesario que leas y aceptes el consentimiento para continuar el proceso.'
        document.getElementById('verConsentimientob').classList.remove('btn-success')
        document.getElementById('verConsentimientob').classList.add('btn-danger')
    }
    document.getElementById("CrearEstudianteForm").style.display = "block"
    let div = document.getElementById("fondoConsentimiento");
    div.style.display="none";
    $("#alertDocumentDownload").show()
}