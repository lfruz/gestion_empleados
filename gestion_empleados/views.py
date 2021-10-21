from flask import Flask, render_template, blueprints, request, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from forms import FormEmpleado, LoginEmpleado, DesempenioEmpleado
# from db import get_db


main = blueprints.Blueprint('main', __name__)


@main.route('/',methods=['GET','POST'])
def login():
    """Función que maneja la ruta login. Responde a los métodos GET y POST.

        Parameters:
        Ninguno

        Returns:
        login.html si es invocada con el método GET. 
        Redirecciona a  main.ajax si es invocada con POST y la validación es verdadera.

    """
    form_login = LoginEmpleado()
    return render_template('login.html', form=form_login)
    
@main.route('/home',methods=['GET','POST'])
def home():
    form_empleado = FormEmpleado()
    return render_template('home.html',form=form_empleado)

@main.route('/crear',methods=['POST'])
def crear():
    form_empleado = FormEmpleado()
    return render_template('crear.html', form=form_empleado)

@main.route('/editar',methods=['POST'])
def editar():
    form_empleado = FormEmpleado()
    return render_template('editar.html', form=form_empleado)

@main.route('/',methods=['POST'])
def eliminar():
    form_empleado = FormEmpleado()
    return render_template('home.html', form=form_empleado)

@main.route('/desempenio')
def desempenio():
    form_desempenio = DesempenioEmpleado()
    return render_template('desempenio.html', form=form_desempenio)

@main.route('/ver_desempenio',methods=['POST'])
def ver_desempenio():
    return render_template('ver_desempenio.html')

@main.route('/perfil',methods=['GET'])
def perfil():
    form_empleado = FormEmpleado()
    return render_template('perfil.html', form=form_empleado)

def logout():
    return render_template('login.html')