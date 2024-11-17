from django.db import models
from django.core.validators import RegexValidator


class Contact(models.Model):
    """A table for recording and storing contacts of a potential client: his name, phone number and email address."""
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    privacy_policy_consent = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name} {self.phone}'

    class Meta:
        verbose_name_plural = 'Контакты для обзвона'


class MeetingAtOffice(models.Model):
    """A table containing information about the user's self-appointment
    for an office meeting at a convenient date and time."""
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    date_of_meeting = models.CharField(max_length=10, validators=[RegexValidator(regex=r'^\d{2}.\d{2}.\d{4}$')],
                                       verbose_name='Дата встречи')
    meeting_time = models.TimeField(verbose_name='Время встречи')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    privacy_policy_consent = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.date_of_meeting} {self.meeting_time} {self.first_name} {self.last_name} - тел. {self.phone}'

    class Meta:
        verbose_name = 'Клиент записан на дату и время:'
        verbose_name_plural = 'Назначенные встречи'
        ordering = ['date_of_meeting', 'meeting_time']


class ServicesOffered(models.Model):
    """A table for working with information about the services provided by the company."""
    title = models.CharField(max_length=60)
    link_to_photo = models.CharField(max_length=200)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Предлагаемая услуга'
        verbose_name_plural = 'Предлагаемые услуги'


class Foundations(models.Model):
    """A table for working with information about the foundations that the company is building."""
    title = models.CharField(max_length=60)
    link_to_photo = models.CharField(max_length=200)
    description = models.TextField(verbose_name='Описание', null=True, blank=True)
    service_offer = models.ForeignKey(ServicesOffered, on_delete=models.CASCADE, verbose_name='Предлагаемая услуга')

    def __str__(self):
        return f'{self.title} {self.link_to_photo}'

    class Meta:
        verbose_name = 'Фундамент'
        verbose_name_plural = 'Фундаменты'


class InfoGlavnoe(models.Model):
    """A table for working with information about the specifics of the company's work."""
    title = models.CharField(max_length=100)
    description = models.TextField(verbose_name='Содержание')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Информация на Главной странице'
