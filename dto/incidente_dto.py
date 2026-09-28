class IncidenteDTO:

    def __init__(
        self,
        id=None,
        fecha="",
        departamento="",
        tipo_incidente="",
        lesionados=0,
        fatalidades=0,
        causa="",
        nivel_riesgo=""
    ):
        self.id = id
        self.fecha = fecha
        self.departamento = departamento
        self.tipo_incidente = tipo_incidente
        self.lesionados = lesionados
        self.fatalidades = fatalidades
        self.causa = causa
        self.nivel_riesgo = nivel_riesgo