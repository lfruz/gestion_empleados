from flask import Flask, abort, render_template, blueprints, request, redirect, url_for, session, flash, send_file
from werkzeug.security import check_password_hash, generate_password_hash
from forms import FormEmpleado, LoginEmpleado, DesempenioEmpleado
from markupsafe import escape
from db import get_db
import functools

SALT = 'Mt1c2022%$Gp443qu1p09'

main = blueprints.Blueprint('main', __name__)


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        # puedes hacer otro tipo de validación
        if 'id_empleado' not in session:
            return redirect(url_for('main.login'))
        return view(**kwargs)
    return wrapped_view


@main.route('/', methods=['GET', 'POST'])
def login():
    form_login = LoginEmpleado()
    if request.method == 'POST':
        usuario = escape(request.form['user'])
        clave = escape(request.form['password'])

        db = get_db()
        #sql = "select * from usuario where usuario = '{0}' and clave= '{1}'".format(usuario, clave)
        user = db.execute(
            'SELECT * FROM tbl_empleados WHERE identificacion = ? ', (usuario,)).fetchone()
        db.commit()
        db.close()

        if user is not None:

            print(user[15])
            clave = SALT + clave + usuario

            sw = check_password_hash(user[15], clave)

            if(sw):
                session['id_empleado'] = user[0]
                session['nombres'] = user[1]
                session['apellidos'] = user[2]
                session['cargo'] = user[11]
                session['rol'] = user[14]
                if session['rol'] == 'Usuario Final':
                    return redirect(url_for('main.ver_desempenio'))
                return redirect(url_for('main.home'))
        flash('Usuario o clave incorrecto.', 'errorLogin')
    return render_template('login.html', form=form_login)


@main.route('/home')
@login_required
def home():
    db = get_db()
    id = session['id_empleado']
    rows = db.execute(
        'select * from tbl_empleados where identificacion != ? and rol!="Super Administrador"', [id]).fetchall()
    db.commit()
    db.close()
    form_empleado = FormEmpleado()
    return render_template('home.html', rows=rows, form=form_empleado)


@main.route('/crear', methods=['GET', 'POST'])
@login_required
def crear():
    form_empleado = FormEmpleado()
    if request.method == 'POST':
        id_empleadoInput = escape(request.form['identificacion'])
        nombresInput = escape(request.form['nombres'])
        apellidosInput = escape(request.form['apellidos'])
        fechaNacimientoInput = escape(request.form['fecha_nacimiento'])
        sexoInput = escape(request.form['sexo'])
        correoInput = escape(request.form['correo'])
        direccionInput = escape(request.form['direccion'])
        telefonoInput = escape(request.form['telefono'])
        fechaIngresoInput = escape(request.form['fecha_ingreso'])
        tipoContratoInput = escape(request.form['tipo_contrato'])
        fechaTerminacionInput = escape(request.form['terminacion_contrato'])
        cargoInput = escape(request.form['cargo'])
        dependenciaInput = escape(request.form['dependencia'])
        salarioInput = escape(request.form['salario'])
        rolInput = escape(request.form['rol'])
        contraseniaInput = escape(request.form['passw'])
        db = get_db()
        contraseniaInput = SALT + contraseniaInput + id_empleadoInput
        contraseniaInput = generate_password_hash(contraseniaInput)
        db.execute("INSERT INTO tbl_empleados (identificacion,nombres, apellidos, fecha_nacimiento, sexo, correo,direccion,telefono,fecha_ingreso,tipo_contrato,fecha_termin_contrato,cargo,dependencia,salario,rol,contrasenia) VALUES( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (id_empleadoInput, nombresInput, apellidosInput, fechaNacimientoInput, sexoInput, correoInput, direccionInput, telefonoInput, fechaIngresoInput, tipoContratoInput, fechaTerminacionInput, cargoInput, dependenciaInput, salarioInput, rolInput, contraseniaInput))
        db.commit()
        db.close()
        flash('Empleado Guardado Exitosamente', 'crearEmpleado')
        return redirect(url_for('main.home'))

    return render_template('crear.html', form=form_empleado)


@main.route('/editar/<id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    db = get_db()
    rows = db.execute(
        'SELECT * FROM tbl_empleados WHERE identificacion = ?', [id]).fetchone()
    db.commit()
    print(rows)
    if request.method == 'POST':
        nombresInput = escape(request.form['nombres'])
        apellidosInput = escape(request.form['apellidos'])
        fechaNacimientoInput = escape(request.form['fecha_nacimiento'])
        sexoInput = escape(request.form['sexo'])
        correoInput = escape(request.form['correo'])
        direccionInput = escape(request.form['direccion'])
        telefonoInput = escape(request.form['telefono'])
        fechaIngresoInput = escape(request.form['fecha_ingreso'])
        tipoContratoInput = escape(request.form['tipo_contrato'])
        fechaTerminacionInput = escape(request.form['terminacion_contrato'])
        cargoInput = escape(request.form['cargo'])
        dependenciaInput = escape(request.form['dependencia'])
        salarioInput = escape(request.form['salario'])
        rolInput = escape(request.form['rol'])
        db.execute("UPDATE tbl_empleados SET nombres = ?, apellidos= ?, fecha_nacimiento= ?, sexo= ?, correo= ?,direccion= ?,telefono= ?,fecha_ingreso= ?,tipo_contrato= ?,fecha_termin_contrato= ?,cargo= ?,dependencia= ?,salario= ?,rol= ? WHERE identificacion = ?",
                   [nombresInput, apellidosInput, fechaNacimientoInput, sexoInput, correoInput, direccionInput, telefonoInput, fechaIngresoInput, tipoContratoInput, fechaTerminacionInput, cargoInput, dependenciaInput, salarioInput, rolInput, id])
        db.commit()
        db.close()
        flash('Empleado Modificado Exitosamente', 'editarEmpleado')
        return redirect(url_for('main.home'))

    form_empleado = FormEmpleado()
    return render_template('editar.html', rows=rows, form=form_empleado)


@main.route('/eliminar/<id>', methods=['GET','POST'])
def eliminar(id):
    db = get_db()
    db.execute('DELETE FROM tbl_empleados WHERE identificacion = ?', [id])
    db.commit()
    db.close()
    flash('Empleado Eliminado Exitosamente', 'editarEmpleado')
    return redirect(url_for('main.home'))


@main.route('/desempenio/<id>', methods=['GET', 'POST'])
@login_required
def desempenio(id):
    db = get_db()
    rows = db.execute(
        'SELECT * FROM tbl_empleados WHERE identificacion = ?', [id]).fetchone()
    db.commit()
    print(rows)
    if request.method == 'POST':
        comentarioInput = escape(request.form['comentario'])
        puntajeInput = escape(request.form['puntaje'])
        idEvaluadorInput = escape(request.form['id_evaluador'])
        db.execute("INSERT INTO tbl_desempenio (id_empleado,comentario,puntaje,id_evaluador) VALUES(?, ?, ?, ?)",
                   ([id, comentarioInput, puntajeInput, idEvaluadorInput]))
        db.commit()
        db.close()
        flash('Desemeo Evaluado Exitosamente', 'evaluarEmpleado')
        return redirect(url_for('main.home'))
    form_desempenio = DesempenioEmpleado()
    return render_template('desempenio.html', rows=rows, form=form_desempenio)


@main.route('/ver_desempenio', methods=['GET', 'POST'])
@login_required
def ver_desempenio():
    db = get_db()
    id = session['id_empleado']
    rows = db.execute(
        'SELECT * FROM tbl_desempenio WHERE id_empleado = ?', [id]).fetchall()
    db.commit()
    db.close()
    print(rows)
    # for row in rows:
    #     id_evaluador = row[4]
    #     getEvaluador = db.execute(
    #         'select nombres,apellidos from tbl_empleados WHERE identificacion = ?', [id_evaluador]).fetchone()
    #     datos = getEvaluador[0]+" "+getEvaluador[1]
    return render_template('ver_desempenio.html', rows=rows)


@main.route('/perfil', methods=['GET', 'POST'])
@login_required
def perfil():
    db = get_db()
    id = session['id_empleado']
    rows = db.execute(
        'SELECT * FROM tbl_empleados WHERE identificacion = ?', [id]).fetchone()
    db.commit()
    db.close()
    print(rows)
    form_empleado = FormEmpleado()
    return render_template('perfil.html', form=form_empleado, rows=rows)


@main.route('/ver_perfil/<id>', methods=['GET', 'POST'])
@login_required
def ver_perfil(id):
    db = get_db()
    rows = db.execute(
        'SELECT * FROM tbl_empleados WHERE identificacion = ?', [id]).fetchone()
    db.commit()
    db.close()
    print(rows)
    form_empleado = FormEmpleado()
    return render_template('perfil.html', form=form_empleado, rows=rows)

@main.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('main.login'))
