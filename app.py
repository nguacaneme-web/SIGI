from flask import Flask

from controllers.incidente_controller import incidente_controller


app = Flask(__name__)

DATABASE = "database.db"


def crear_base_datos():
    import sqlite3

    conexion = sqlite3.connect(DATABASE)

    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS incidentes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            departamento TEXT NOT NULL,
            tipo_incidente TEXT NOT NULL,
            lesionados INTEGER DEFAULT 0,
            fatalidades INTEGER DEFAULT 0,
            causa TEXT,
            nivel_riesgo TEXT
        )
    """)

    conexion.commit()
    conexion.close()


app.register_blueprint(incidente_controller)


if __name__ == "__main__":

    crear_base_datos()

    app.run(debug=True)