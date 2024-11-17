from django.shortcuts import render
from .models import *
from datetime import datetime


def main_page(request):
    """Renders the main page. Data on the services provided and
    the specifics of the company's work are extracted from the database."""
    title_h1 = 'УЮТНЫЙ ДОМ'
    services_offered = ServicesOffered.objects.all()
    info_main = InfoGlavnoe.objects.all()
    context = {
        'title_h1': title_h1,
        'services_offered': services_offered,
        'info_main': info_main,
    }
    return render(request, 'main_page.html', context)


def foundation(request):
    """Displays a page with the types of foundations. Data on the types of foundations and
    links to photos of the corresponding foundation are extracted from the database."""
    title_h1 = 'Фундаменты'
    foundations = Foundations.objects.all()
    context = {
        'title_h1': title_h1,
        'foundations': foundations,
    }
    return render(request, 'foundation.html', context)


def katalog_proektov_domov(request):
    """Renders a page with a catalog of house projects."""
    title_h1 = 'Каталог проектов домов'
    context = {
        'title_h1': title_h1,
    }
    return render(request, 'katalog_proektov_domov.html', context)


def septic_tanks(request):
    """Renders a page with septic tanks varieties."""
    title_h1 = 'Септики'
    context = {
        'title_h1': title_h1,
    }
    return render(request, 'septic_tanks.html', context)


def o_kompanii(request):
    """Renders a page with information about the company."""
    title_h1 = 'О компании'
    context = {
        'title_h1': title_h1,
    }
    return render(request, 'o_kompanii.html', context)


def contact_form(request):
    """Renders the contact collection form and the logic of processing the received data."""
    if request.method == 'POST':
        # Получаем данные
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        check = request.POST.get('check') == 'on'

        # Проверим выводом в консоли, что данные от пользователя обработаны и получены сервером (для себя)
        print(f'Name: {name}. Phone: {phone}. Email: {email}. Check: {check}.')
        Contact.objects.create(name=name, phone=phone, email=email)
        return render(request, 'answer_after_contact_form.html')
    return render(request, 'contact_form.html')


def form_of_record(request):
    """Renders a form for recording a user for an office meeting and the logic of processing the received data."""
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        date_of_meeting = datetime.strptime(request.POST.get('date_of_meeting'), '%Y-%m-%d').strftime('%d.%m.%Y')
        meeting_time = request.POST.get('meeting_time')
        check = request.POST.get('check') == 'on'
        context = {
            'date_of_meeting': date_of_meeting,
            'meeting_time': meeting_time,
            'first_name': first_name,
        }

        if not MeetingAtOffice.objects.filter(first_name=first_name, last_name=last_name, phone=phone).exists():
            # Проверим выводом в консоли, что данные от пользователя обработаны и получены сервером (для себя)
            print(f'Запись создана - имя и фамилия: {first_name} {last_name}. Тел.: {phone}. '
                  f'Дата и время встречи: {date_of_meeting} {meeting_time}. Check: {check}.')
            MeetingAtOffice.objects.create(first_name=first_name,  last_name=last_name, phone=phone,
                                           date_of_meeting=date_of_meeting, meeting_time=meeting_time)
            return render(request, 'answer_after_form_of_record.html', context)
        else:
            queryset = MeetingAtOffice.objects.filter(
                first_name=first_name, last_name=last_name, phone=phone).values_list('date_of_meeting', 'meeting_time')
            previous_date_of_meeting = queryset[0][0]
            previous_meeting_time = queryset[0][1]
            print(f'Клиент {first_name} найден, встреча {previous_date_of_meeting} в {previous_meeting_time}')
            context.update({'previous_date_of_meeting': previous_date_of_meeting,
                            'previous_meeting_time': previous_meeting_time})
            # Сохранение данных в сессию
            request.session['first_name'] = first_name
            request.session['last_name'] = last_name
            request.session['phone'] = phone
            request.session['date_of_meeting'] = date_of_meeting
            request.session['meeting_time'] = meeting_time
            return render(request, 'recording_error.html', context)
    return render(request, 'form_of_record.html')


def update_previous_appointment(request):
    """Updates the date and time of the meeting specified by the user in the database table,
    and also displays the response about the scheduled meeting to the user"""
    first_name = request.session.get('first_name')
    last_name = request.session.get('last_name')
    phone = request.session.get('phone')
    date_of_meeting = request.session.get('date_of_meeting')
    meeting_time = request.session.get('meeting_time')

    print(f'Клиент {first_name} {last_name} перезаписался на {date_of_meeting} в {meeting_time}')
    MeetingAtOffice.objects.filter(
        first_name=first_name, last_name=last_name, phone=phone).update(
        date_of_meeting=date_of_meeting, meeting_time=meeting_time)
    context = {'date_of_meeting': date_of_meeting, 'meeting_time': meeting_time, 'first_name': first_name}
    return render(request, 'answer_after_form_of_record.html', context)


def no_changes_previous_appointment(request):
    """Displays the response to the user about saving the previously scheduled date and time of the meeting"""
    first_name = request.session.get('first_name')
    last_name = request.session.get('last_name')
    phone = request.session.get('phone')
    queryset = MeetingAtOffice.objects.filter(
        first_name=first_name, last_name=last_name, phone=phone).values_list('date_of_meeting', 'meeting_time')
    previous_date_of_meeting = queryset[0][0]
    previous_meeting_time = queryset[0][1]

    print(f'Клиент {first_name} оставил прежнюю запись: {previous_date_of_meeting} в {previous_meeting_time}')
    context = {
        'previous_date_of_meeting': previous_date_of_meeting,
        'previous_meeting_time': previous_meeting_time,
        'first_name': first_name,
    }
    return render(request, 'answer_about_saving_previous_record.html', context)
