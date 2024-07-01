class Clientee():
    def __init__(self, nombre, edad, cedula):
        self.nombre = nombre
        self.edad = edad
        self.cedula = cedula
        self.balance = 0
        self.type_tickets = None
        self.tickets = []

    def show(self):
        return f"""
            nombre: {self.nombre}
            edad: {self.edad}
            cedula: {self.cedula}
            balance: {self.balance}
            type_tickets: {self.type_tickets}
            tickets: {self.tickets}"""