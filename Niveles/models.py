from django.db import models

class Nivel(models.Model):
    nivel = models.CharField(max_length = 150, unique=True, null=False, blank=False)
    color_fondo = models.CharField("color de fondo", null=False, blank=False,max_length = 30)
    color_letra = models.CharField("color de texto", default="rgb(0,0,0)", null=False, blank=False,max_length = 30)

    class Meta:
        db_table = "niveles"
        verbose_name_plural = "niveles"
        

    def __str__(self):
        return self.nivel
