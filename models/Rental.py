from datetime import datetime



class Rental:
    def __init__(self, transport, start_date=None):
        self.transport = transport
        self.transport_type = "Машина" if type(transport).__name__ == "Car" else "Мотоцикл"
        self.start_date = start_date or datetime.now()
        self.end_date = None