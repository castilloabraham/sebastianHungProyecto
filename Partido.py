class Partido():
    def __init__(self, id, numero, home, away, fecha, grupo, estadio):
        self.id = id
        self.numero = numero
        self.home = home
        self.away = away
        self.fecha = fecha
        self.grupo = grupo
        self.estadio = estadio
        self.tickets_vip = []
        self.tickets_general = []
        self.attendance = 0

    def show(self):
        return f"""
            id: {self.id}
            numero: {self.numero}
            home: {self.home.nombre}
            away: {self.away.nombre}
            fecha: {self.fecha}
            grupo: {self.grupo}
            estadio: {self.estadio.nombre}"""
        