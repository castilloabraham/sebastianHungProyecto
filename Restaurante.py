class Restaurante():

    def __init__(self, nombre, productos):
        self.nombre = nombre
        self.productos = productos

    def show(self):
        return f"""
            nombre: {self.nombre}
            productos: {self.productos}"""        
