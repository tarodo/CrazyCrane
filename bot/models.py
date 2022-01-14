from django.db import models


class Producer(models.Model):
    name = models.CharField("Производитель", max_length=200)
    code = models.CharField("Код производителя", blank=True, max_length=20)

    def __str__(self):
        return f'{self.name} : {self.code}'

    class Meta:
        verbose_name = "Производитель"
        verbose_name_plural = "Производители"


class CraneModel(models.Model):
    code = models.CharField("Код крана", max_length=200)
    producer = models.ForeignKey(Producer, on_delete=models.CASCADE, verbose_name="Производитель",)

    def __str__(self):
        return f'{self.code}'

    class Meta:
        verbose_name = "Кран"
        verbose_name_plural = "Краны"
