from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import OperationalError, ProgrammingError
from django.shortcuts import render, redirect

from .models import Request, Review

SERVICES = [
    {
        'title': 'Техническое обслуживание',
        'description': 'Замена масла, фильтров, технических жидкостей и комплексная проверка автомобиля.',
        'price': 'от 2 500 ₽',
        'icon': 'fas fa-oil-can',
    },
    {
        'title': 'Диагностика автомобиля',
        'description': 'Компьютерная диагностика, проверка ошибок, осмотр ходовой и основных систем.',
        'price': 'от 0 ₽',
        'icon': 'fas fa-laptop-medical',
    },
    {
        'title': 'Ремонт ходовой части',
        'description': 'Замена амортизаторов, рычагов, сайлентблоков, шаровых опор и других элементов подвески.',
        'price': 'от 1 900 ₽',
        'icon': 'fas fa-car-side',
    },
    {
        'title': 'Тормозная система',
        'description': 'Замена колодок, дисков, тормозной жидкости, обслуживание суппортов.',
        'price': 'от 1 500 ₽',
        'icon': 'fas fa-circle-notch',
    },
    {
        'title': 'Шиномонтаж',
        'description': 'Сезонная смена шин, балансировка, ремонт проколов и проверка давления.',
        'price': 'от 1 800 ₽',
        'icon': 'fas fa-compact-disc',
    },
    {
        'title': 'Электрика и электроника',
        'description': 'Поиск неисправностей, ремонт проводки, датчиков, освещения и электронных блоков.',
        'price': 'от 1 200 ₽',
        'icon': 'fas fa-bolt',
    },
]

STATIC_REVIEWS = [
    {
        'name': 'Алексей',
        'car': 'Toyota Camry',
        'rating': 5,
        'stars': range(5),
        'text': 'Быстро нашли причину стука в подвеске, заранее согласовали цену и сделали в тот же день.',
    },
    {
        'name': 'Марина',
        'car': 'Kia Rio',
        'rating': 5,
        'stars': range(5),
        'text': 'Приезжала на ТО. Всё объяснили простыми словами, лишних работ не навязывали.',
    },
    {
        'name': 'Дмитрий',
        'car': 'Volkswagen Polo',
        'rating': 4,
        'stars': range(4),
        'text': 'Удобная запись через сайт, нормальная зона ожидания и понятная смета до ремонта.',
    },
]

def save_request_from_post(request):
    name = request.POST.get('name', '').strip()
    phone = request.POST.get('phone', '').strip()
    car = request.POST.get('car', '').strip()
    service = request.POST.get('service', '').strip()

    if not name or not phone:
        return False, 'Введите имя и телефон, чтобы администратор смог с вами связаться.'

    try:
        Request.objects.create(
            name=name,
            phone=phone,
            car=car,
            service=service or 'Консультация',
        )
    except (OperationalError, ProgrammingError):
        return False, 'Заявку не удалось сохранить. Выполните миграции: python manage.py migrate.'

    return True, ''

def index(request):
    if request.method == 'POST' and request.POST.get('name') is not None:
        success, error = save_request_from_post(request)
        if success:
            messages.success(request, 'Заявка отправлена! Администратор свяжется с вами в ближайшее время.')
            return redirect('/#contacts')
        messages.error(request, error)
    return render(request, 'index.html')

def services(request):
    return render(request, 'services.html', {'services': SERVICES})

def contacts(request):
    success = request.GET.get('sent') == '1'
    if request.method == 'POST':
        success, error = save_request_from_post(request)
        if success:
            messages.success(request, 'Заявка отправлена! Администратор свяжется с вами в ближайшее время.')
            return redirect('/contacts/?sent=1')
        if error:
            messages.error(request, error)
    return render(request, 'contacts.html', {
        'success': success,
        'selected_service': request.GET.get('service', ''),
    })

def reviews(request):
    success = False
    if request.method == 'POST':
        try:
            Review.objects.create(
                name=request.POST.get('name', '').strip(),
                car=request.POST.get('car', '').strip(),
                rating=int(request.POST.get('rating', 5)),
                text=request.POST.get('text', '').strip(),
            )
            success = True
        except (ValueError, OperationalError, ProgrammingError):
            success = False

    user_reviews = []
    try:
        for review in Review.objects.all()[:12]:
            user_reviews.append({
                'name': review.name,
                'car': review.car,
                'rating': review.rating,
                'stars': range(max(1, min(review.rating, 5))),
                'text': review.text,
            })
    except (OperationalError, ProgrammingError):
        user_reviews = []

    return render(request, 'reviews.html', {
        'success': success,
        'reviews': user_reviews + STATIC_REVIEWS,
    })

def cabinet(request):
    user_requests = []
    if request.user.is_authenticated:
        try:
            user_requests = list(Request.objects.filter(phone=request.user.username)[:10])
        except (OperationalError, ProgrammingError):
            user_requests = []
    return render(request, 'cabinet.html', {
        'requests': user_requests,
        'requests_count': len(user_requests),
    })

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('login_phone', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Вы успешно вошли в личный кабинет.')
            return redirect('/cabinet/')
        messages.error(request, 'Неверный телефон или пароль.')
    return redirect('/cabinet/')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('login_phone', '').strip()
        password = request.POST.get('password', '')
        if username and password:
            user, created = User.objects.get_or_create(username=username)
            if created:
                user.set_password(password)
                user.save()
                messages.success(request, 'Аккаунт создан. Вы вошли в личный кабинет.')
            else:
                messages.error(request, 'Аккаунт с таким телефоном уже существует. Выполните вход.')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('/cabinet/')
        else:
            messages.error(request, 'Введите телефон и пароль.')
    return redirect('/cabinet/')

def logout_view(request):
    logout(request)
    messages.success(request, 'Вы вышли из личного кабинета.')
    return redirect('/cabinet/')
