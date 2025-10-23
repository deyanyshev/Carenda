from models.Transport import Transport


class Car(Transport):
    """Класс автомобиля - наследует от Transport"""

    def __init__(self, brand, model, year, img, price_per_hour, seats, transmission):
        # Вызываем конструктор родительского класса
        super().__init__(brand, model, year, img, price_per_hour)

        # Специфические характеристики автомобиля
        self.seats = seats  # Количество мест в автомобиле (целое число)
        self.transmission = transmission  # Тип коробки передач: "automatic" (автомат), "manual" (механика)