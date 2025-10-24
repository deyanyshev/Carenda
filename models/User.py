from datetime import datetime

from models.Rental import Rental


class User:
    """Класс пользователя системы каршеринга"""

    def __init__(self, id, login, password, phone,):
        # Основная информация о пользователе
        self.id = id  # Уникальный идентификатор пользователя
        self.login = login  # Полное имя пользователя
        self.password = password
        self.phone = phone  # Номер телефона пользователя

        # История и текущая аренда
        self.rental_history = []  # Список предыдущих аренд (история поездок)
        self.current_rental = None  # Текущая активная аренда (None если нет активной аренды)


    def rent_transport(self, transport):
        if self.current_rental:
            return False  # Уже есть активная аренда

        if not transport.is_available:
            return False  # Транспорт недоступен

        transport.is_available = False
        self.current_rental = Rental(transport)
        return True


    def end_rental(self):
        if not self.current_rental:
            return False

        self.current_rental.transport.is_available = True
        self.current_rental.end_date = datetime.now()
        self.rental_history.append(self.current_rental)
        self.current_rental = None
        return True