ROLE_CHOICES = (
    ('customer', 'customer'),
    ('executor', 'executor'),
)

GENDER_CHOICES = (
    ("Женский", "Женский"),
    ("Мужской", "Мужской"),
    ("Не указано", "Не указано"),
)

EDUCATION_CHOICES = (
    ("Среднее", "Среднее"),
    ("Высшее", "Высшее"),
)

RATING_CHOICES = ((i, i * '*') for i in range(1, 6))
