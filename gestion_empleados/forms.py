from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, DateField, SelectField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length


class FormEmpleado(FlaskForm):
    identificacion = IntegerField('Identificacion:', validators=[DataRequired(message='No dejar vacío, completar'), Length(max=10)])
    nombres = StringField('Nombres: ', validators=[DataRequired()])
    apellidos = StringField('Apellidos: ', validators=[DataRequired()])
    fecha_nacimiento = DateField('Fecha Nacimiento: ', validators=[DataRequired()])
    sexo = SelectField('Sexo: ', choices=[('F', "Femenino"), ('M', "Masculino")],validators=[DataRequired()])
    correo = StringField('Correo Electronico: ', validators=[DataRequired()])
    direccion = StringField('Direccion: ', validators=[DataRequired()])
    telefono = StringField('Telefono: ', validators=[DataRequired()])
    fecha_ingreso = DateField('Fecha de Ingreso: ', validators=[DataRequired()])
    tipo_contrato = StringField('Tipo de Contrato: ', validators=[DataRequired()])
    terminacion_contrato = DateField('Terminacion de Contrato: ', validators=[DataRequired()])
    cargo  = StringField('Cargo: ', validators=[DataRequired()])
    dependencia = StringField('Dependencia: ', validators=[DataRequired()])
    salario = StringField('Salario: ', validators=[DataRequired()])
    rol = SelectField('Rol: ', choices=[('Super Administrador', "Super Administrador"), ('Administrador', "Administrador"),('Usuario Final', "Usuario Final")],  validators=[DataRequired()])
    passw = StringField('Contraseña: ', validators=[DataRequired()])
    guardar = SubmitField('Guardar')
    editar = SubmitField('Editar')
    eliminar = SubmitField('Eliminar')


class DesempenioEmpleado(FlaskForm):
    id_empleado = IntegerField('Identificacion:', validators=[
                                 DataRequired(), Length(max=10)])
    comentario = TextAreaField('Comentario: ', validators=[DataRequired()])
    puntaje = IntegerField('Puntaje:', validators=[
                                 DataRequired(), Length(max=2)])
    calificar_desempenio = SubmitField('Calificar')

class LoginEmpleado(FlaskForm):
    user = StringField('Identificacion: ', validators=[
                       DataRequired(), Length(max=10)])
    password = PasswordField('Contraseña: ', validators=[DataRequired()])
    entrar = SubmitField('Entrar')
