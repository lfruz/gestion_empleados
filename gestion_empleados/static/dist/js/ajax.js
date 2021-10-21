console.log('Hola');

function cargarMensaje()
{
    var objXMLHTTP = new XMLHttpRequest();

    objXMLHTTP.open('GET', 'http://127.0.0.1:5000/miApi/mensaje/');

    objXMLHTTP.addEventListener('load', completado);
    objXMLHTTP.addEventListener('error', manejarError);
    objXMLHTTP.addEventListener('progress', progreso);
    objXMLHTTP.addEventListener('abort', abortado);

    objXMLHTTP.send();
}


function manejarError(evt)
{
    console.log('ocurrio un error.');
}

function progreso(evt)
{
    var procentaje = evt.loaded / evt.total * 100;
    console.log(procentaje);
}


function abortado(evt)
{
    console.log('cancelado');
}




function completado(evt)
{

    var data =  JSON.parse(this.response);

    console.log(data);

    var info="";

    for(var i =0; i < data.length; i++)
    {
        var mensaje = data[i];
        info += "<div class= 'mensaje'><p class='asunto'>" +mensaje.asunto + "</p>"
        info += "<p class='contenidoMensaje'>" +mensaje.mensaje + "</p>"
        info += "<p class='usuario'>" +mensaje.usuario + "</p></div>"
        
    }

   

    

    document.getElementById('respuesta').innerHTML= info;

}


/*---------------------------------------------*/ 

function crearMensaje()
{

    var userNameInput = document.formularioMensajeAjax.username;
    var asunto = document.formularioMensajeAjax.asunto;
    var mensaje = document.formularioMensajeAjax.mensaje;

    if(userNameInput.value.length > 0 && asunto.value.length >0  && mensaje.value.length > 0)
    {

    var objXMLHTTP = new XMLHttpRequest();

    objXMLHTTP.open('POST', 'http://127.0.0.1:5000/miApi/crearmensaje/');

    objXMLHTTP.addEventListener('load', crearMensajeCompleto);

    objXMLHTTP.setRequestHeader("Content-Type", "application/json");

    objXMLHTTP.send(JSON.stringify({'usuario':userNameInput.value, 'asunto':asunto.value, 'mensaje': mensaje.value})

    );}
    else
    {
        alert('Por favor escriba todos los campos.');
    }
}

function crearMensajeCompleto(evt)
{
    var data = JSON.parse(this.response)
    console.log(data);
    cargarMensaje();
}

/*---------------------------------------------*/ 

function actualizarMensaje()
{

    var idInput = document.formularioActualizarAjax.message_id;
    var asunto = document.formularioActualizarAjax.asunto;
  
    if(idInput.value.length > 0 && asunto.value.length > 0)
    {
        var objXMLHTTP = new XMLHttpRequest();

        objXMLHTTP.open('PUT', 'http://127.0.0.1:5000/miApi/actualizarmensaje/');
    
        objXMLHTTP.addEventListener('load', actualizarMensajeCompleto);
    
        objXMLHTTP.setRequestHeader("Content-Type", "application/json");
    
        objXMLHTTP.send(JSON.stringify({'id':idInput.value, 'asunto':asunto.value})
    
        );
    }
    else{
        alert("Escriba todos los datos.");
    }
   
}

function actualizarMensajeCompleto(evt)
{
    var data = JSON.parse(this.response)
    console.log(data);
    cargarMensaje();
}