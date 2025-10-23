from abc import ABC, abstractmethod


class Transport(ABC):
    """Абстрактный класс Transport - базовый класс для всех видов транспорта"""

    def __init__(self, brand, model, year, img):
        self.brand = brand
        self.model = model
        self.year = year
        self.is_available = True
        self.img = img



