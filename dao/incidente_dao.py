import sqlite3
from models.incidente import Incidente


class IncidenteDAO:

    def __init__(self, database):
        self.database = database

    def conectar(self):
        return sqlite3.connect(self.database)

    def crear(self, incidente):
        conexion = self.conectar()
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO incidentes (
                fecha,
                departamento,
                tipo_incidente,
                lesionados,
                fatalidades,
                causa,
                nivel_riesgo
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            incidente.fecha,
            incidente.departamento,
            incidente.tipo_incidente,
            incidente.lesionados,
            incidente.fatalidades,
            incidente.causa,
            incidente.nivel_riesgo
        ))

        conexion.commit()
        conexion.close()

    def listar(self):
        conexion = self.conectar()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT
                id,
                fecha,
                departamento,
                tipo_incidente,
                lesionados,
                fatalidades,
                causa,
                nivel_riesgo
            FROM incidentes
            ORDER BY id DESC
        """)

        registros = cursor.fetchall()
        conexion.close()

        incidentes = []

        for registro in registros:
            incidente = Incidente(
                id=registro[0],
                fecha=registro[1],
                departamento=registro[2],
                tipo_incidente=registro[3],
                lesionados=registro[4],
                fatalidades=registro[5],
                causa=registro[6],
                nivel_riesgo=registro[7]
            )

            incidentes.append(incidente)

        return incidentes

    def buscar_por_id(self, id):
        conexion = self.conectar()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT
                id,
                fecha,
                departamento,
                tipo_incidente,
                lesionados,
                fatalidades,
                causa,
                nivel_riesgo
            FROM incidentes
            WHERE id = ?
        """, (id,))

        registro = cursor.fetchone()
        conexion.close()

        if registro is None:
            return None

        return Incidente(
            id=registro[0],
            fecha=registro[1],
            departamento=registro[2],
            tipo_incidente=registro[3],
            lesionados=registro[4],
            fatalidades=registro[5],
            causa=registro[6],
            nivel_riesgo=registro[7]
        )

    def actualizar(self, incidente):
        conexion = self.conectar()
        cursor = conexion.cursor()

        cursor.execute("""
            UPDATE incidentes
            SET
                fecha = ?,
                departamento = ?,
                tipo_incidente = ?,
                lesionados = ?,
                fatalidades = ?,
                causa = ?,
                nivel_riesgo = ?
            WHERE id = ?
        """, (
            incidente.fecha,
            incidente.departamento,
            incidente.tipo_incidente,
            incidente.lesionados,
            incidente.fatalidades,
            incidente.causa,
            incidente.nivel_riesgo,
            incidente.id
        ))

        conexion.commit()
        conexion.close()

    def eliminar(self, id):
        conexion = self.conectar()
        cursor = conexion.cursor()

        cursor.execute("""
            DELETE FROM incidentes
            WHERE id = ?
        """, (id,))

        conexion.commit()
        conexion.close()
    def obtener_estadisticas(self):
        conexion = self.conectar()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT COUNT(*) FROM incidentes
        """)
        total_incidentes = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COALESCE(SUM(lesionados), 0)
            FROM incidentes
        """)
        total_lesionados = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COALESCE(SUM(fatalidades), 0)
            FROM incidentes
        """)
        total_fatalidades = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*)
            FROM incidentes
            WHERE nivel_riesgo = 'Crítico'
        """)
        riesgo_critico = cursor.fetchone()[0]

        conexion.close()

        return {
            "total_incidentes": total_incidentes,
            "total_lesionados": total_lesionados,
            "total_fatalidades": total_fatalidades,
            "riesgo_critico": riesgo_critico
        }

    def incidentes_por_departamento(self):
        conexion = self.conectar()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT departamento, COUNT(*)
            FROM incidentes
            GROUP BY departamento
            ORDER BY COUNT(*) DESC
        """)

        resultados = cursor.fetchall()

        conexion.close()

        return resultados