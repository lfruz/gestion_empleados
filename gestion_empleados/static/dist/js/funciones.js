//var userNameInput = document.formularioRegistro.username;
//window.status="Hola mundo";
function validar() {
    var id_empleadoInput = document.formCrearEmpleado.identificacion;
    var nombresInput = document.formularioRegistro.userPassword;
    var apellidosInput = document.formularioRegistro.correo;
    var fechaNacimientoInput = document.formularioRegistro.correo;
    var sexoInput = document.formularioRegistro.correo;
    var correoInput = document.formularioRegistro.correo;
    var direccionInput = document.formularioRegistro.correo;
    var telefonoInput = document.formularioRegistro.correo;
    var fechaIngresoInput = document.formularioRegistro.correo;
    var tipoContratoInput = document.formularioRegistro.correo;
    var fechaTerminacionInput = document.formularioRegistro.correo;
    var cargoInput = document.formularioRegistro.correo;
    var dependenciaInput = document.formularioRegistro.correo;
    var salarioInput = document.formularioRegistro.correo;
    var rolInput = document.formularioRegistro.correo;
    var contraseniaInput = document.formularioRegistro.correo;

    var formato_email = /^\w+([\.-]?\w+)@\w+([\.-]?\w+)(\.\w{2,3})+$/;

    var swErrores = false;

    // console.log(userNameInput.value + "-" + passWordInput.value + "-" + correoInput.value);



    if (id_empleadoInput.value.length == 0) {
        alert("El id de usuario debe tener mínimo 8 caracteres.");
        //document.getElementById("errorUsername").innerHTML = "El nombre de usuario debe tener mínimo 8 caracteres.";
        userNameInput.focus();
        //document.getElementById("botonEnviar").disabled=true;
        swErrores = true;
    }

    if (passWordInput.value.length == 0 || passWordInput.value.length < 8) {
        //alert("La clave debe tener mínimo 8 caracteres.");
        document.getElementById("errorPassword").innerHTML = "La clave debe tener mínimo 8 caracteres.";
        passWordInput.focus();
        swErrores = true;
    }

    if (!correoInput.value.match(formato_email)) {
        //alert("Por favor escriba un correo válido.");
        document.getElementById("errorMail").innerHTML = "Por favor escriba un correo válido.";
        correoInput.focus();
        swErrores = true;
    }


    if (swErrores == true) {
        return false;
    }
    else {
        return true;
    }




}


function verClave() {
    console.log('Mostrar clave');

    var passWordInput = document.getElementById('userPassword');
    passWordInput.type = "text";
}

function ocultarClave() {
    console.log('Ocultar clave');
    var passWordInput = document.getElementById('userPassword');
    passWordInput.type = "password";


}

function ocultarVerClave() {
    var passWordInput = document.getElementById('userPassword');
    var tipo = passWordInput.type;

    console.log(tipo);

    if (tipo == "text") {
        passWordInput.type = "password";
    }

    if (tipo == "password") {
        passWordInput.type = "text";
    }
}
