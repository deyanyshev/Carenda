class User:
    """Класс пользователя системы каршеринга"""

    def __init__(self, user_id, name, email, phone, driver_license):
        # Основная информация о пользователе
        self.user_id = user_id  # Уникальный идентификатор пользователя
        self.name = name  # Полное имя пользователя
        self.email = email  # Электронная почта пользователя
        self.phone = phone  # Номер телефона пользователя
        self.driver_license = driver_license  # Номер водительского удостоверения

        # Статус и финансы пользователя
        self.is_verified = False  # Прошел ли пользователь верификацию (True/False)
        self.balance = 0.0  # Баланс пользователя (в рублях)

        # История и текущая аренда
        self.rental_history = []  # Список предыдущих аренд (история поездок)
        self.current_rental = None  # Текущая активная аренда (None если нет активной аренды)