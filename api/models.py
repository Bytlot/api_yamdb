from django.db import models


class Review(models.Model):
    SCORE_CHOICES = (
        (1, 'Ужасно'),
        (2, 'Очень плохо'),
        (3, 'Плохо'),
        (4, 'Ниже среднего'),
        (5, 'Средне'),
        (6, 'Выше среднего'),
        (7, 'Выше превыше среднего'),
        (8, 'Хорошо'),
        (9, 'Очень хорошо'),
        (10, 'Прекрасно')
    )

    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='reviews')
    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                               related_name='reviews')
    text = models.TextField()
    pub_date = models.DateTimeField('Дата отзыва',
                                    auto_now_add=True)   
    score = models.PositiveSmallIntegerField(choices=SCORE_CHOICES)

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='comments')
    title = models.ForeignKey(Review, on_delete=models.CASCADE,
                             related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField('Дата добавления',
                                   auto_now_add=True,
                                   db_index=True)

    def __str__(self):
        return self.text
