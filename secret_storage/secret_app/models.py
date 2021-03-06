from django.db import models


class Secret(models.Model):
    secret_text = models.BinaryField(
        blank=False,
        null=False,
        verbose_name='Секретный Текст'
    )
    secret_word = models.CharField(
        max_length=32,
        blank=False,
        null=False,
        verbose_name='Кодовая Фраза'
    )
    secret_key = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Секретный Ключ'
    )
    is_read = models.BooleanField(default=False)
    added_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Время создания секрета",
    )
    lifetime = models.DurationField(
        verbose_name="Время жизни секрета",
    )

    def __str__(self):
        return self.secret_key

    class Meta:
        verbose_name = 'Секрет'
        verbose_name_plural = 'Секреты'
