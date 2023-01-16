from dataclasses import dataclass, asdict
from typing import Dict, List


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    message: str = ('Тип тренировки: {training_type}; '
                    'Длительность: {duration:.3f} ч; '
                    'Дистанция: {distance:.3f} км; '
                    'Ср. скорость: {speed:.3f} км/ч; '
                    'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.message.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


@dataclass
class Running(Training):
    """Тренировка: бег."""
    CALORIES_COEFF_1 = 18
    CALORIES_COEFF_2 = 20

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        min_duration = self.duration * 60
        calories = ((self.CALORIES_COEFF_1
                    * self.get_mean_speed()
                    - self.CALORIES_COEFF_2)
                    * self.weight
                    / self.M_IN_KM
                    * min_duration)
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_COEFF_WALK_1: float = 0.035
    CALORIES_COEFF_WALK_2: float = 0.029

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        duration_min = self.duration * 60
        return ((self.CALORIES_COEFF_WALK_1
                * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * self.CALORIES_COEFF_WALK_2
                * self.weight)
                * duration_min)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    CALORIES_COEFF_SWIM_1 = 1.1
    CALORIES_COEFF_SWIM_2 = 2

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.action = action
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Переопределили метод, средняя скорость."""
        return (self.length_pool
                * self.count_pool
                / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        """Переопределили метод, колории."""
        return ((self.get_mean_speed()
                + self.CALORIES_COEFF_SWIM_1)
                * self.CALORIES_COEFF_SWIM_2
                * self.weight)


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    package: Dict[str, type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type not in package:
        raise ValueError('Данный тип тренировки отсутствует в словаре')
    return package[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    information = training.show_training_info()
    print(information.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
