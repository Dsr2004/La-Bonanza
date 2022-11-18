let title="Reglamento general"
reglamento = [
    {'title':'PUNTUALIDAD','datos':'El alumno(a) deberá llegar puntualmente a la clase, solo se permitirán 10 minutos de tolerancia, luego de este tiempo no se dictará la clase y el precio de la misma será descontado del valor de la matricula como si se hubiese dictado. El tiempo perdido por llegar tarde a la clase no será recompensado. De preferencia estar 5 minutos antes de la clase.'},
    {'title':'CANCELACIONES','datos':'La clase deberá ser cancelada por lo menos con 24 horas de anterioridad, de no ser cancelada, la clase será descontada como si se hubiera dictado. Las clases que son canceladas adecuadamente se pueden reemplazar en un periodo de 2 semanas, dependiendo de la disponibilidad del horario del club. Si la clase no se remplaza en un periodo de 4 semanas la clase se dará por dictada. Solamente se podrán cancelar las clases por motivos de salud, de tal forma que solamente se reprogramarán las clases que sean canceladas por atenciones médicas debidamente certificadas por el médico de la EPS. No se repondrán clases por motivos diferentes, ya sea por viajes, por clima, problemas de transporte, vacaciones u otros eventos, pues es responsabilidad del alumno y sus padres programar sus horarios.'},
    {'title':'CAMBIO DE HORARIO','datos':'En caso de que se tenga que cambiar el horario de las clases, el padre o alumno(a) deberá ​notificar a la administración por lo menos con 24 horas de anterioridad, en caso contrario, no se podrá cambiar el horario de las clases.'},
    {'title':'UNIFORME','datos':' El alumno(a) deberá usar siempre el uniforme: zapatos totalmente cerrados, preferiblemente botas, pantalones largos, la camisa o camiseta del club, y para alumnos menores de 12 años el club le proveerá un casco adecuado. En caso de que el alumno(a) participe en cualquier tipo de competencias, el uniforme es responsabilidad del alumno(a) o del padre de familia.'},
    {'title':'​ANTES Y DESPUES DE CLASES','datos':'El club no se hará responsable por cualquier incidente que ocurra antes y después de clase, si los alumnos menores de edad llegan antes o se quedan después de clases, los padres se harán responsable del cuidado de su hijo(a).'},
    {'title':'​SISTEMA DE PAGO','datos':'La matrícula será cobrada anualmente, a partir del día de la inscripción. El pago de ​la mensualidad deberá hacerse durante los primeros 8 días hábiles del periodo de pago, de lo contrario el alumno(a) no podrá asistir a clases hasta que se liquide la mensualidad en su totalidad. El pago se podrá hacer por medio de una transferencia bancaria o en efectivo.     La mensualidad depende de la cantidad de semanas en el mes, hay meses que cuentan con 4 semanas es decir 4 clases, otros meses que cuentan con 5 semanas serian 5 clases, en caso de que una de las clases sea un día festivo dicha clase se deberá de reprogramar para otro día, mas no se deja de pagar.'},
    {'title':'COMPETENCIAS','datos':'Si el alumno(a) decide participar en cualquier tipo de competencia, todos los gastos y riesgos asociados con el evento serán responsabilidad de los padres de familia y/o acudientes del alumno, quienes bajo su propio riesgo y responsabilidad autorizarán la participación en competencias. En caso de que la competencia implique la representación del Club, será éste quien decida si permite o no dicha representación, sin que por ello asuma responsabilidad por los gastos y riesgos, ya que los mismos son asumidos completamente por los padres y/o acudientes del alumno.'},
    {'title':'RESPETO','datos':' Tanto los alumnos como sus padres y/o representantes se comprometen a respetar a todos y cada uno de los integrantes del club, por lo tanto, se abstendrán de realizar actos irrespetuosos o que riñan con la sana convivencia. En caso de que un alumno o alguno de sus representantes incurran en conductas que afecten la convivencia y el buen nombre del club, podrán ser retirados del mismo.'},
    {'title':'ACEPTACIÓN','datos':'Por medio de la suscripción de este documento declaro en forma clara y expresa que he leído y comprendido el presente reglamento, razón por lo acepto en su integridad y me comprometo a cumplirlo en su integridad, así como velar por su cumplimiento por parte de mi hijo y/o representado. La dirección de este club pide el consentimiento a los padres o tutores legales para publicar las imágenes, en las cuales aparezcan individualmente o en grupo los niños(a), en las diferentes secuencias y actividades realizadas en el club y fuera del mismo.'},
]
function verContrato(){
    $("#alertDocumentDownload").hide()
    let div = document.getElementById("fondoContrato");
    div.style.display="block";
    document.getElementById("titleContrato").innerHTML = title;
    let content = document.getElementById("contentContrato")
    for (let i = 0; i < reglamento.length; i++) {
        let subtitle = document.createElement("h3")
        subtitle.innerHTML = reglamento[i].title;
        let contenido = document.createElement("p")
        contenido.innerHTML = "<b>"+subtitle.innerHTML+':</b> ' + reglamento[i].datos
        let divC = document.createElement("div")
        divC.appendChild(contenido)
        content.appendChild(divC)
        document.getElementById("CrearEstudianteForm").style.display = "none"
    }
}
function hideContrato(){
    $("#alertDocumentDownload").show()
    let div = document.getElementById("fondoContrato");
    div.style.display="none";
    document.getElementById("CrearEstudianteForm").style.display = "block"
}
function guardarContrato(){
    let checkbox = document.getElementById("AceptacionContrato")
    let input = checkbox.cloneNode(true);
    input.id = "aceptaContratoInput"
    input.style.display="none"
    if (checkbox.checked) {
        input.name = "aceptaContrato"
        if(document.getElementById("aceptaContratoInput")==null){
            document.getElementById("CrearEstudianteForm").appendChild(input)
        }else{
            let repl = document.getElementById("aceptaContratoInput")
            document.getElementById("CrearEstudianteForm").replaceChild(input, repl)
        }
        let div = document.getElementById("fondoContrato");
        div.style.display="none";
        let button = document.getElementById("verContratob")
        if (button.classList.contains("btn-xs")){
            button.classList.remove("btn-xs")
            button.classList.add('btn-success')
        }
        else{
            button.classList.remove("btn-danger")
            button.classList.add('btn-success')
        }
        button.style.color = "#fff"
        button.nextSibling.style.display = "none"
    }
    else{
        if(document.getElementById("aceptaContratoInput")==null){
            document.getElementById("CrearEstudianteForm").appendChild(input)
        }else{
            let repl = document.getElementById("aceptaContratoInput")
            document.getElementById("CrearEstudianteForm").replaceChild(input, repl)
        }
        let div = document.getElementById("fondoContrato");
        div.style.display="none";
        let button = document.getElementById("verContratob")
        if (button.classList.contains("btn-xs")){
            button.classList.remove("btn-xs")
            button.classList.add('btn-danger')
        }
        else{
            button.classList.remove("btn-success")
            button.classList.add('btn-danger')
        }
        button.style.color = "#fff"
        button.nextSibling.innerHTML = "<sub>No podrá realizar el registro</sub>"
        button.nextSibling.style.display = "block"
        button.nextSibling.style.color = "red"
        button.nextSibling.style.marginLeft = "10px"
    }
    document.getElementById("CrearEstudianteForm").style.display = "block"
    
    console.log(document.getElementById("aceptaContrato").checked)
    $("#alertDocumentDownload").show()
}