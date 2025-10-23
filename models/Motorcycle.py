from models.Transport import Transport


class Motorcycle(Transport):
    """Класс мотоцикла - наследует от Transport"""

    def __init__(self, brand, model, year, img, price_per_hour,
                 bike_type, engine_volume, has_helmet=True):
        # Вызываем конструктор родительского класса
        super().__init__(brand, model, year, img, price_per_hour)

        # Специфические характеристики мотоцикла
        self.bike_type = bike_type  # Тип мотоцикла: "sport" (спортивный), "cruiser" (круизер), "touring" (туристический)
        self.engine_volume = engine_volume  # Объем двигателя в кубических сантиметрах (например: 600, 1000, 1200)
        self.has_helmet = has_helmet  # Включен ли шлем в аренду (True/False)