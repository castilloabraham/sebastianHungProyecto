class Estadio():
    def __init__(self, id, nombre, ciudad, capacidad, restaurantes):
        self.id = id
        self.nombre = nombre
        self.ciudad = ciudad
        self.capacidad = capacidad
        self.restaurantes = restaurantes

    def show(self):
        return f"""
        id: {self.id}
        nombre: {self.nombre}
        ciudad: {self.ciudad}
        capacidad: {self.capacidad}
        restaurantes: {self.restaurantes}"""
    

