from flask import Blueprint, render_template, request, redirect, url_for

from dao.incidente_dao import IncidenteDAO
from models.incidente import Incidente
from dto.incidente_dto import IncidenteDTO


incidente_controller = Blueprint(
    "incidente_controller",
    __name__
)


dao = IncidenteDAO("database.db")
@incidente_controller.route("/dashboard")
def dashboard():

    estadisticas = dao.obtener_estadisticas()

    departamentos = dao.incidentes_por_departamento()

    return render_template(
        "dashboard.html",
        estadisticas=estadisticas,
        departamentos=departamentos
    )

@incidente_controller.route("/")
def listar():
    incidentes = dao.listar()

    return render_template(
        "index.html",
        incidentes=incidentes
    )


@incidente_controller.route("/crear", methods=["GET", "POST"])
def crear():

    if request.method == "POST":

        dto = IncidenteDTO(
            fecha=request.form["fecha"],
            departamento=request.form["departamento"],
            tipo_incidente=request.form["tipo_incidente"],
            lesionados=int(request.form["lesionados"]),
            fatalidades=int(request.form["fatalidades"]),
            causa=request.form["causa"],
            nivel_riesgo=request.form["nivel_riesgo"]
        )

        incidente = Incidente(
            fecha=dto.fecha,
            departamento=dto.departamento,
            tipo_incidente=dto.tipo_incidente,
            lesionados=dto.lesionados,
            fatalidades=dto.fatalidades,
            causa=dto.causa,
            nivel_riesgo=dto.nivel_riesgo
        )

        dao.crear(incidente)

        return redirect(url_for("incidente_controller.listar"))

    return render_template("crear.html")


@incidente_controller.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):

    incidente = dao.buscar_por_id(id)

    if incidente is None:
        return "Incidente no encontrado", 404

    if request.method == "POST":

        dto = IncidenteDTO(
            id=id,
            fecha=request.form["fecha"],
            departamento=request.form["departamento"],
            tipo_incidente=request.form["tipo_incidente"],
            lesionados=int(request.form["lesionados"]),
            fatalidades=int(request.form["fatalidades"]),
            causa=request.form["causa"],
            nivel_riesgo=request.form["nivel_riesgo"]
        )

        incidente.fecha = dto.fecha
        incidente.departamento = dto.departamento
        incidente.tipo_incidente = dto.tipo_incidente
        incidente.lesionados = dto.lesionados
        incidente.fatalidades = dto.fatalidades
        incidente.causa = dto.causa
        incidente.nivel_riesgo = dto.nivel_riesgo

        dao.actualizar(incidente)

        return redirect(url_for("incidente_controller.listar"))

    return render_template(
        "editar.html",
        incidente=incidente
    )


@incidente_controller.route("/eliminar/<int:id>")
def eliminar(id):

    dao.eliminar(id)

    return redirect(url_for("incidente_controller.listar"))