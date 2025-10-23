from abc import ABC, abstractmethod


class Transport(ABC):
    """Абстрактный класс Transport - базовый класс для всех видов транспорта"""

    def __init__(self, brand, model, year, img, price_per_hour, transport_id=None):
        self.brand = brand  # Марка транспорта (например: "Toyota", "BMW")
        self.model = model  # Модель транспорта (например: "Camry", "R1200")
        self.year = year  # Год выпуска транспорта (например: 2022)
        self.img = img  # Ссылка на изображение транспорта


        # Уникальный идентификатор транспорта
        # Если не указан, генерируется автоматически из марки, модели и года
        self.transport_id = transport_id



