from flask import (
    Flask,
    abort,
    render_template,
    blueprints,
    request,
    redirect,
    url_for,
    session,
    flash,
    send_file,
)
from werkzeug.security import check_password_hash, generate_password_hash
from forms import FormEmpleado, LoginEmpleado, DesempenioEmpleado, CambiarPassEmpleado
from markupsafe import escape
from db import get_db
import functools
import sqlite3

SALT = "Mt1c2022%$Gp443qu1p09"
main = blueprints.Blueprint("main", __name__)
main.register_error_handler(404, "perfil.html")


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        # puedes hacer otro tipo de validación
        if "id_empleado" not in session:
            return redirect(url_for("main.login"))
        return view(**kwargs)

    return wrapped_view


@main.route("/", methods=["GET", "POST"])
def login():
    form_login = LoginEmpleado()
    if request.method == "POST":
        usuario = escape(request.form["user"])
        clave = escape(request.form["password"])

        db = get_db()
        # sql = "select * from usuario where usuario = '{0}' and clave= '{1}'".format(usuario, clave)
        user = db.execute(
            "SELECT * FROM tbl_empleados WHERE identificacion = ? ", (usuario,)
        ).fetchone()
        db.commit()
        db.close()

        if user is not None:

            print(user[15])
            clave = SALT + clave + usuario

            sw = check_password_hash(user[15], clave)

            if sw:
                session["id_empleado"] = user[0]
                session["nombres"] = user[1]
                session["apellidos"] = user[2]
                session["cargo"] = user[11]
                session["rol"] = user[14]
                if session["rol"] == "Usuario Final":
                    return redirect(url_for("main.ver_desempenio"))
                return redirect(url_for("main.home"))
        flash("Usuario o clave incorrecto.", "errorLogin")
    return render_template("login.html", form=form_login)


@main.route("/home")
@login_required
def home():
    if session["rol"] == "Usuario Final":
        return redirect(url_for("main.ver_desempenio"))
    db = get_db()
    id = session["id_empleado"]
    id_rol = "Super Administrador"
    rows = db.execute(
        "select * from tbl_empleados where identificacion != ? and rol!=?",
        [id, id_rol],
    ).fetchall()
    db.commit()
    db.close()
    form_empleado = FormEmpleado()
    return render_template("home.html", rows=rows, form=form_empleado)


@main.route("/crear", methods=["GET", "POST"])
@login_required
def crear():
    if session["rol"] == "Usuario Final":
        return redirect(url_for("main.ver_desempenio"))
    if request.method == "POST":
        try:
            id_empleadoInput = escape(request.form["identificacion"])
            nombresInput = escape(request.form["nombres"])
            apellidosInput = escape(request.form["apellidos"])
            fechaNacimientoInput = escape(request.form["fecha_nacimiento"])
            sexoInput = escape(request.form["sexo"])
            correoInput = escape(request.form["correo"])
            direccionInput = escape(request.form["direccion"])
            telefonoInput = escape(request.form["telefono"])
            fechaIngresoInput = escape(request.form["fecha_ingreso"])
            tipoContratoInput = escape(request.form["tipo_contrato"])
            fechaTerminacionInput = escape(request.form["terminacion_contrato"])
            cargoInput = escape(request.form["cargo"])
            dependenciaInput = escape(request.form["dependencia"])
            salarioInput = escape(request.form["salario"])
            rolInput = escape(request.form["rol"])
            contraseniaInput = escape(request.form["passw"])
            db = get_db()
            contraseniaInput = SALT + contraseniaInput + id_empleadoInput
            contraseniaInput = generate_password_hash(contraseniaInput)
            db.execute(
                "INSERT INTO tbl_empleados (identificacion,nombres, apellidos, fecha_nacimiento, sexo, correo,direccion,telefono,fecha_ingreso,tipo_contrato,fecha_termin_contrato,cargo,dependencia,salario,rol,contrasenia) VALUES( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    id_empleadoInput,
                    nombresInput,
                    apellidosInput,
                    fechaNacimientoInput,
                    sexoInput,
                    correoInput,
                    direccionInput,
                    telefonoInput,
                    fechaIngresoInput,
                    tipoContratoInput,
                    fechaTerminacionInput,
                    cargoInput,
                    dependenciaInput,
                    salarioInput,
                    rolInput,
                    contraseniaInput,
                ),
            )
            db.commit()
            db.close()
            flash("Empleado Guardado Exitosamente", "successEmpleado")
            return redirect(url_for("main.home"))
        except (sqlite3.IntegrityError):
            flash("Error al Guadar los Datos. El empleado ya existe", "errorEmpleado")
    form_empleado = FormEmpleado()
    return render_template("crear.html", form=form_empleado)


@main.route("/editar/<id>", methods=["GET", "POST"])
@login_required
def editar(id):
    if session["rol"] == "Usuario Final":
        return redirect(url_for("main.ver_desempenio"))
    form_empleado = FormEmpleado()
    db = get_db()
    print(id)
    rows = db.execute(
        "SELECT * FROM tbl_empleados WHERE identificacion = ?", [id]
    ).fetchone()
    db.commit()
    print(rows)
    if request.method == "POST":
        nombresInput = escape(request.form["nombres"])
        apellidosInput = escape(request.form["apellidos"])
        fechaNacimientoInput = escape(request.form["fecha_nacimiento"])
        sexoInput = escape(request.form["sexo"])
        correoInput = escape(request.form["correo"])
        direccionInput = escape(request.form["direccion"])
        telefonoInput = escape(request.form["telefono"])
        fechaIngresoInput = escape(request.form["fecha_ingreso"])
        tipoContratoInput = escape(request.form["tipo_contrato"])
        fechaTerminacionInput = escape(request.form["terminacion_contrato"])
        cargoInput = escape(request.form["cargo"])
        dependenciaInput = escape(request.form["dependencia"])
        salarioInput = escape(request.form["salario"])
        rolInput = escape(request.form["rol"])
        db.execute(
            "UPDATE tbl_empleados SET nombres = ?, apellidos= ?, fecha_nacimiento= ?, sexo= ?, correo= ?,direccion= ?,telefono= ?,fecha_ingreso= ?,tipo_contrato= ?,fecha_termin_contrato= ?,cargo= ?,dependencia= ?,salario= ?,rol= ? WHERE identificacion = ?",
            [
                nombresInput,
                apellidosInput,
                fechaNacimientoInput,
                sexoInput,
                correoInput,
                direccionInput,
                telefonoInput,
                fechaIngresoInput,
                tipoContratoInput,
                fechaTerminacionInput,
                cargoInput,
                dependenciaInput,
                salarioInput,
                rolInput,
                id,
            ],
        )
        db.commit()
        db.close()
        flash("Empleado Modificado Exitosamente", "successEmpleado")
        return redirect(url_for("main.home"))
    if rows is None:
        flash("El empleado NO existe", "verificarEmpleado")
    if rows is not None:
        if rows[4] == "M":
            form_empleado.sexo.choices = [(rows[4], "Masculino"), ("F", "Femenino")]
        if rows[4] == "F":
            form_empleado.sexo.choices = [(rows[4], "Femenino"), ("M", "Masculino")]
        if rows[14] == "Super Administrador":
            form_empleado.rol.choices = [
                (rows[14], "Super Administrador"),
                ("Administrador", "Administrador"),
                ("Usuario Final", "Usuario Final"),
            ]
        if rows[14] == "Administrador":
            form_empleado.rol.choices = [
                (rows[14], "Administrador"),
                ("Super Administrador", "Super Administrador"),
                ("Usuario Final", "Usuario Final"),
            ]
        if rows[14] == "Usuario Final":
            form_empleado.rol.choices = [
                (rows[14], "Usuario Final"),
                ("Super Administrador", "Super Administrador"),
                ("Administrador", "Administrador"),
            ]
    return render_template("editar.html", rows=rows, form=form_empleado)


@main.route("/eliminar/<id>", methods=["GET", "POST"])
@login_required
def eliminar(id):
    db = get_db()
    db.execute("DELETE FROM tbl_empleados WHERE identificacion = ?", [id])
    db.commit()
    db.close()
    flash("Empleado Eliminado Exitosamente", "successEmpleado")
    return redirect(url_for("main.home"))


@main.route("/desempenio/<id>", methods=["GET", "POST"])
@login_required
def desempenio(id):
    if session["rol"] == "Administrador":
        return redirect(url_for("main.home"))
    if session["rol"] == "Usuario Final":
        return redirect(url_for("main.ver_desempenio"))
    db = get_db()
    rows = db.execute(
        "SELECT * FROM tbl_empleados WHERE identificacion = ?", [id]
    ).fetchone()
    db.commit()
    print(rows)
    if rows is None:
        flash("El empleado NO existe", "verificarEmpleado")
    if request.method == "POST":
        comentarioInput = escape(request.form["comentario"])
        puntajeInput = escape(request.form["puntaje"])
        idEvaluadorInput = escape(request.form["id_evaluador"])
        db.execute(
            "INSERT INTO tbl_desempenio (id_empleado,comentario,puntaje,id_evaluador) VALUES(?, ?, ?, ?)",
            ([id, comentarioInput, puntajeInput, idEvaluadorInput]),
        )
        db.commit()
        db.close()
        flash("Desempeño Evaluado Exitosamente", "successEmpleado")
        return redirect(url_for("main.home"))
    form_desempenio = DesempenioEmpleado()
    return render_template("desempenio.html", rows=rows, form=form_desempenio)


@main.route("/ver_desempenio", methods=["GET", "POST"])
@login_required
def ver_desempenio():
    if session["rol"] == "Super Administrador" or session["rol"] == "Administrador":
        return redirect(url_for("main.home"))
    db = get_db()
    id = session["id_empleado"]
    rows = db.execute(
        "SELECT * FROM tbl_desempenio WHERE id_empleado = ?", [id]
    ).fetchall()
    db.commit()
    db.close()
    print(rows)
    # for row in rows:
    #     id_evaluador = row[4]
    #     getEvaluador = db.execute(
    #         'select nombres,apellidos from tbl_empleados WHERE identificacion = ?', [id_evaluador]).fetchone()
    #     datos = getEvaluador[0]+" "+getEvaluador[1]
    return render_template("ver_desempenio.html", rows=rows)


@main.route("/perfil", methods=["GET", "POST"])
@login_required
def perfil():
    db = get_db()
    id = session["id_empleado"]
    rows = db.execute(
        "SELECT * FROM tbl_empleados WHERE identificacion = ?", [id]
    ).fetchone()
    db.commit()
    db.close()
    print(rows)
    form_empleado = FormEmpleado()
    if rows[4] == "M":
        form_empleado.sexo.choices = [(rows[4], "Masculino")]
    if rows[4] == "F":
        form_empleado.sexo.choices = [(rows[4], "Femenino")]
    if rows[14] == "Super Administrador":
        form_empleado.rol.choices = [(rows[14], "Super Administrador")]
    if rows[14] == "Administrador":
        form_empleado.rol.choices = [(rows[14], "Administrador")]
    if rows[14] == "Usuario Final":
        form_empleado.rol.choices = [(rows[14], "Usuario Final")]
    return render_template("perfil.html", form=form_empleado, rows=rows)


@main.route("/ver_perfil/<id>", methods=["GET", "POST"])
@login_required
def ver_perfil(id):
    if session["rol"] == "Usuario Final":
        return redirect(url_for("main.ver_desempenio"))
    db = get_db()
    rows = db.execute(
        "SELECT * FROM tbl_empleados WHERE identificacion = ?", [id]
    ).fetchone()
    db.commit()
    db.close()
    print(rows)
    form_empleado = FormEmpleado()
    if rows is None:
        flash("El empleado NO existe", "verificarEmpleado")
    if rows is not None:
        if rows[4] == "M":
            form_empleado.sexo.choices = [(rows[4], "Masculino")]
        if rows[4] == "F":
            form_empleado.sexo.choices = [(rows[4], "Femenino")]
        if rows[14] == "Super Administrador":
            form_empleado.rol.choices = [(rows[14], "Super Administrador")]
        if rows[14] == "Administrador":
            form_empleado.rol.choices = [(rows[14], "Administrador")]
        if rows[14] == "Usuario Final":
            form_empleado.rol.choices = [(rows[14], "Usuario Final")]
    return render_template("perfil.html", form=form_empleado, rows=rows)


@main.route("/cambiar_pass", methods=["GET", "POST"])
@login_required
def cambiar_pass():
    form_cambiarPassEmpleado = CambiarPassEmpleado()
    id_emp = session["id_empleado"]
    db = get_db()
    rows = db.execute(
        "SELECT contrasenia FROM tbl_empleados WHERE identificacion = ?",
        [id_emp],
    ).fetchone()
    db.commit()
    oldPass = rows[0]
    print(oldPass)
    if request.method == "POST":
        idEmpInput = escape(request.form["id_emp"])
        oldPassInput = escape(request.form["oldPass"])
        newPassInput = escape(request.form["newPass"])
        confirmarNewPassInput = escape(request.form["confirmarNewPass"])
        oldPassCheck = SALT + oldPassInput + idEmpInput
        verif_pass = check_password_hash(oldPass, oldPassCheck)
        print(verif_pass)
        if verif_pass == False:
            flash("Verifique su anterior contraseña", "errorEmpleado")
        elif newPassInput != confirmarNewPassInput:
            flash("Las Contraseñas NO coinciden", "errorEmpleado")
        elif oldPassInput == confirmarNewPassInput:
            flash(
                "La nueva contraseña deber ser diferente a la anterior contraseña.",
                "errorEmpleado",
            )
        elif verif_pass:
            encryptNewPassInput = generate_password_hash(
                SALT + newPassInput + idEmpInput
            )
            db.execute(
                "UPDATE tbl_empleados SET contrasenia= ? WHERE identificacion = ?",
                [encryptNewPassInput, id_emp],
            )
            db.commit()
            db.close()
            flash("Contraseña Modificada Exitosamente", "successEmpleado")
            return redirect(url_for("main.logout"))
    return render_template("cambiar_pass.html", form=form_cambiarPassEmpleado)


@main.route("/logout", methods=["GET"])
@login_required
def logout():
    session.clear()
    return redirect(url_for("main.login"))
