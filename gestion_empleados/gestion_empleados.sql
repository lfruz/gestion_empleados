BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "tbl_empleados" (
	"identificacion"	INT NOT NULL UNIQUE,
	"nombres"	VARCHAR(100) NOT NULL,
	"apellidos"	VARCHAR(100) NOT NULL,
	"fecha_nacimiento"	DATE NOT NULL,
	"sexo"	VARCHAR(20) NOT NULL,
	"correo"	VARCHAR(100) NOT NULL,
	"direccion"	VARCHAR(100) NOT NULL,
	"telefono"	INT NOT NULL,
	"fecha_ingreso"	DATE NOT NULL,
	"tipo_contrato"	VARCHAR(100) NOT NULL,
	"fecha_termin_contrato"	DATE NOT NULL,
	"cargo"	VARCHAR(100) NOT NULL,
	"dependencia"	VARCHAR(100) NOT NULL,
	"salario"	DOUBLE NOT NULL,
	"rol"	VARCHAR(100) NOT NULL,
	"contrasenia"	VARCHAR(255) NOT NULL,
	PRIMARY KEY("identificacion")
);
CREATE TABLE IF NOT EXISTS "tbl_desempenio" (
	"id_desempenio"	INTEGER NOT NULL,
	"id_empleado"	INT NOT NULL,
	"comentario"	VARCHAR(255) NOT NULL,
	"puntaje"	DOUBLE NOT NULL,
	"id_evaluador"	INT NOT NULL,
	FOREIGN KEY("id_empleado") REFERENCES "tbl_empleados"("identificacion"),
	FOREIGN KEY("id_evaluador") REFERENCES "tbl_empleados"("identificacion"),
	PRIMARY KEY("id_desempenio" AUTOINCREMENT)
);
COMMIT;
