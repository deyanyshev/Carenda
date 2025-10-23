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