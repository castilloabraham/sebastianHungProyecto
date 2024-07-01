class Equipo():
    def __init__(self, id, codigo, nombre, grupo):
        self.id = id
        self.codigo = codigo
        self.nombre = nombre
        self.grupo = grupo

    def show(self):
        return f"""
            id: {self.id}
            codigo: {self.codigo}
            nombre: {self.nombre}
            grupo: {self.grupo}"""
