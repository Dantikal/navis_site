from email.policy import default
from unicodedata import category
from django.db import models
from django.core.validators import EmailValidator, RegexValidator
from ckeditor.fields import RichTextField
from django.core.validators import FileExtensionValidator

class Service(models.Model):
    """Модель услуг"""
    title = models.CharField('Название', max_length=200)
    name = models.CharField('Имя', max_length=200, blank=True, null=True)
    description = models.TextField('Описание', blank=True, null=True)
    image = models.ImageField('Изображение', upload_to='services/', blank=True, null=True)
    url = models.URLField('Ссылка', max_length=200, blank=True, null=True, help_text='Куда ведет кнопка "Продолжить"')
    order = models.PositiveSmallIntegerField("Порядок", default=0, help_text="Чем меньше число, тем выше позиция")
    is_active = models.BooleanField('Активно', default=True, help_text="Отображать на сайте?")
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True) 
    
    class Meta:
        ordering = ['order', 'title']  
        verbose_name = "Услуга/Проект"
        verbose_name_plural = "Услуги/Проекты"  
    
    def __str__(self):
        return self.title
    
    def short_description(self):
        if self.description and len(self.description) > 50:  
            return f"{self.description[:50]}..."
        return self.description or ""
    short_description.short_description = "Описание (кратко)"


class Technology(models.Model):
    """Модель для технологий (секция 'Мы используем')"""
    name = models.CharField('Название', max_length=200)
    logo = models.ImageField("Логотип", upload_to='technologies/', blank=True, null=True, help_text="SVG или PNG логотип")
    url = models.URLField('Ссылка на сайт', max_length=200, blank=True, null=True, help_text='Например: https://www.python.org/')
    order = models.PositiveSmallIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Активно", default=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Технология" 
        verbose_name_plural = "Технологии"  

    def __str__(self):
        return self.name


class Testimonial(models.Model):
    """Модель для отзывов клиентов (секция 'Благодарности наших клиентов')"""
    client_name = models.CharField(
        'Имя клиента', 
        max_length=200,
        help_text='Например: Эмиля Тимматова'
    )
    client_position = models.CharField(
        'Должность', 
        max_length=200,
        help_text='Например: Директор компании "Айскейс"'
    )
    client_company = models.CharField(
        'Компания',
        max_length=200,
        blank=True,
        null=True
    )
    client_photo = models.ImageField(
        'Фото клиента',
        upload_to='testimonials/',
        blank=True,
        null=True,
        help_text='Фотография клиента (рекомендуемый размер: 100x100)'
    )
    text = models.TextField(
        'Текст отзыва',
        max_length=1000,
        help_text='Текст благодарности от клиента'
    )
    rating = models.PositiveSmallIntegerField(
        'Рейтинг',
        default=5,
        choices=[(i, i) for i in range(1, 6)],
        help_text='Оценка от 1 до 5'
    )
    project_link = models.URLField(
        'Ссылка на проект',
        max_length=200,
        blank=True,
        null=True,
        help_text='Ссылка на выполненный проект'
    )
    order = models.PositiveSmallIntegerField(
        "Порядок", 
        default=0,
        help_text="Чем меньше число, тем выше позиция"
    )
    is_active = models.BooleanField(
        'Активно', 
        default=True,
        help_text="Отображать на сайте?"
    )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    
    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Отзыв клиента"
        verbose_name_plural = "Отзывы клиентов"
    
    def __str__(self):
        return f"{self.client_name} - {self.client_position}"
    
    @property
    def client_full_info(self):
        """Полная информация о клиенте"""
        return f"{self.client_name}, {self.client_position}"


class Project(models.Model):
    """Модель для проектов в оглавлении"""
    title = models.CharField(
        'Название проекта',
        max_length=200,
        help_text='Например: Сайт для поиска и покупки авиабилетов'
    )
    project_type = models.CharField(
        'Тип проекта',
        max_length=100,
        choices=[
            ('website', 'Сайт'),
            ('mobile', 'Мобильное приложение'),
            ('telegram', 'Telegram бот'),
            ('other', 'Другое')
        ],
        default='website'
    )
    description = models.TextField(
        'Описание проекта',
        blank=True,
        null=True
    )
    image = models.ImageField(
        'Превью проекта',
        upload_to='projects/',
        blank=True,
        null=True
    )
    url = models.URLField(
        'Ссылка на проект',
        max_length=200,
        blank=True,
        null=True
    )
    order = models.PositiveSmallIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Активно", default=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'title']
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"
    
    def __str__(self):
        return self.title


class ConsultationRequest(models.Model):
    """Модель для заявок на консультацию"""
    INTEREST_CHOICES = [
        ('website', 'Разработка сайта'),
        ('mobile', 'Мобильное приложение'),
        ('crypto', 'Криптовалюта/Блокчейн'),
        ('design', 'Дизайн'),
        ('marketing', 'Маркетинг'),
        ('other', 'Другое'),
    ]
    
    name = models.CharField(
        'Имя',
        max_length=200
    )
    phone = models.CharField(
        'Номер телефона',
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message='Введите корректный номер телефона'
            )
        ]
    )
    interest = models.CharField(
        'Что вас интересует?',
        max_length=50,
        choices=INTEREST_CHOICES,
        default='other'
    )
    interest_other = models.CharField(
        'Другое (укажите)',
        max_length=200,
        blank=True,
        null=True,
        help_text='Если выбрали "Другое", уточните'
    )
    is_processed = models.BooleanField('Обработано', default=False)
    notes = models.TextField('Заметки', blank=True, null=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    
    class Meta:
        ordering = ['-created_at', '-is_processed']
        verbose_name = "Заявка на консультацию"
        verbose_name_plural = "Заявки на консультацию"
    
    def __str__(self):
        return f"{self.name} - {self.phone}"
    
    @property
    def interest_display(self):
        """Отображение интереса с учетом поля 'Другое'"""
        if self.interest == 'other' and self.interest_other:
            return self.interest_other
        return dict(self.INTEREST_CHOICES).get(self.interest, self.interest)


class CompanyInfo(models.Model):
    """Модель для информации о компании (контакты, адрес, режим работы)"""
    phone = models.CharField(
        'Телефон',
        max_length=20,
        help_text='Например: 0502 800 202'
    )
    phone_additional = models.CharField(
        'Дополнительный телефон',
        max_length=20,
        blank=True,
        null=True
    )
    address = models.CharField(
        'Адрес',
        max_length=300,
        help_text='Например: г. Бишкек, ул. Манас 60/1'
    )
    address_map_link = models.URLField(
        'Ссылка на карту',
        max_length=500,
        blank=True,
        null=True,
        help_text='Ссылка на Google Maps или 2GIS'
    )
    work_hours = models.CharField(
        'Режим работы',
        max_length=200,
        help_text='Например: с 10:00 до 19:00'
    )
    email = models.EmailField(
        'Email',
        max_length=254,
        blank=True,
        null=True
    )
    instagram = models.URLField(
        'Instagram',
        max_length=200,
        blank=True,
        null=True
    )
    facebook = models.URLField(
        'Facebook',
        max_length=200,
        blank=True,
        null=True
    )
    telegram = models.CharField(
        'Telegram',
        max_length=100,
        blank=True,
        null=True,
        help_text='Username в Telegram (например: @company)'
    )
    whatsapp = models.CharField(
        'WhatsApp',
        max_length=20,
        blank=True,
        null=True,
        help_text='Номер для WhatsApp'
    )
    
    class Meta:
        verbose_name = "Информация о компании"
        verbose_name_plural = "Информация о компании"
    
    def save(self, *args, **kwargs):
        # Разрешаем только одну запись
        if not self.pk and CompanyInfo.objects.exists():
            existing = CompanyInfo.objects.first()
            self.pk = existing.pk
        super().save(*args, **kwargs)
    
    def __str__(self):
        return "Контакты компании"


class SiteContent(models.Model):
    """Модель для контента страницы"""
    # Заголовки секций
    hero_title = models.CharField(
        'Главный заголовок',
        max_length=200,
        default='Мы разрабатываем лучшие цифровые продукты для вашего бизнеса'
    )
    technologies_title = models.CharField(
        'Заголовок секции технологий',
        max_length=100,
        default='Мы используем'
    )
    projects_title = models.CharField(
        'Заголовок секции проектов',
        max_length=100,
        default='Наши проекты'
    )
    testimonials_title = models.CharField(
        'Заголовок секции отзывов',
        max_length=100,
        default='Благодарности наших клиентов'
    )
    consultation_title = models.CharField(
        'Заголовок секции консультации',
        max_length=100,
        default='Получить бесплатную консультацию'
    )
    
    # Тексты
    subscription_text = models.CharField(
        'Текст под подпиской',
        max_length=200,
        default='Мы свяжемся с вами на почте.'
    )
    button_text = models.CharField(
        'Текст кнопки',
        max_length=50,
        default='Продолжить'
    )
    all_projects_text = models.CharField(
        'Текст кнопки "Все проекты"',
        max_length=50,
        default='Все проекты'
    )
    send_button_text = models.CharField(
        'Текст кнопки "Отправить"',
        max_length=50,
        default='Отправить'
    )
    
    # Изображения
    logo = models.ImageField(
        'Логотип компании',
        upload_to='site/logo/',
        blank=True,
        null=True
    )
    favicon = models.ImageField(
        'Favicon',
        upload_to='site/favicon/',
        blank=True,
        null=True
    )
    hero_image = models.ImageField(
        'Изображение в hero секции',
        upload_to='site/hero/',
        blank=True,
        null=True
    )
    
    # Мета данные
    meta_title = models.CharField(
        'Meta Title',
        max_length=200,
        blank=True,
        null=True
    )
    meta_description = models.TextField(
        'Meta Description',
        max_length=500,
        blank=True,
        null=True
    )
    
    is_active = models.BooleanField('Активно', default=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    
    class Meta:
        verbose_name = 'Контент страницы'
        verbose_name_plural = 'Контент страницы'
    
    def save(self, *args, **kwargs):
        if self.is_active:
            SiteContent.objects.filter(is_active=True).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'Настройки главной страницы (ID: {self.id})'


# Добавьте в конец файла main/models.py
class ContactRequest(models.Model):
    """Модель для контактных заявок"""
    email = models.EmailField('Email')
    phone = models.CharField('Телефон', max_length=20, blank=True, null=True)
    is_processed = models.BooleanField('Обработано', default=False)
    notes = models.TextField('Заметки', blank=True, null=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    
    class Meta:
        ordering = ['-created_at', '-is_processed']
        verbose_name = "Контактная заявка"
        verbose_name_plural = "Контактные заявки"
    
    def __str__(self):
        return self.email or self.phone or f"Заявка #{self.id}"


class ServiceDetail(models.Model):
    """Модель для детальной страницы услуги"""
    # Связь с существующей моделью Service
    service = models.OneToOneField(
        Service,
        on_delete=models.CASCADE,
        related_name='detail',
        verbose_name='Услуга',
        null=True,
        blank=True,
        help_text='Связь с основной услугой'
    )
    
    # Основная информация
    title = models.CharField(
        'Заголовок',
        max_length=200,
        help_text='Например: UX/UI дизайн'
    )
    subtitle = models.CharField(
        'Подзаголовок',
        max_length=200,
        blank=True,
        null=True,
        help_text='Например: Интерфейс / Вариации'
    )
    
    # Основное описание с CKEditor
    description = RichTextField(
        'Описание',
        help_text='Полное описание услуги с форматированием',
        config_name='default'
    )
    
    # Краткое описание
    short_description = models.TextField(
        'Краткое описание',
        max_length=500,
        help_text='Краткое описание для превью',
        blank=True,
        null=True
    )
    
    # Изображения
    main_image = models.ImageField(
        'Главное изображение',
        upload_to='service_details/',
        blank=True,
        null=True
    )
    banner_image = models.ImageField(
        'Изображение для баннера',
        upload_to='service_details/banners/',
        blank=True,
        null=True
    )
    
    # Мета данные
    meta_title = models.CharField(
        'Meta Title',
        max_length=200,
        blank=True,
        null=True
    )
    meta_description = models.TextField(
        'Meta Description',
        max_length=500,
        blank=True,
        null=True
    )
    
    # Настройки
    is_active = models.BooleanField('Активно', default=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    
    class Meta:
        verbose_name = 'Детальная страница услуги'
        verbose_name_plural = 'Детальные страницы услуг'
    
    def __str__(self):
        return self.title


class ServiceFeature(models.Model):
    """Модель для блоков особенностей услуги (Анализ конкурентов, CRM, Blockchain и т.д.)"""
    service_detail = models.ForeignKey(
        ServiceDetail,
        on_delete=models.CASCADE,
        related_name='features',
        verbose_name='Услуга'
    )
    
    title = models.CharField(
        'Заголовок',
        max_length=200,
        help_text='Например: Анализ конкурентов'
    )
    description = RichTextField(
        'Описание',
        help_text='Описание особенности',
        blank=True,
        null=True
    )
    
    # Иконка (можно загрузить или использовать CSS класс)
    icon = models.ImageField(
        'Иконка',
        upload_to='service_features/',
        blank=True,
        null=True,
        help_text='Загрузите иконку'
    )
    icon_class = models.CharField(
        'CSS класс иконки',
        max_length=100,
        blank=True,
        null=True,
        help_text='Или укажите CSS класс (например: bi bi-phone)'
    )
    
    # Ссылка
    link = models.URLField(
        'Ссылка',
        max_length=200,
        blank=True,
        null=True,
        help_text='Ссылка на подробнее'
    )
    link_text = models.CharField(
        'Текст ссылки',
        max_length=50,
        default='Подробнее',
        blank=True,
        null=True
    )
    
    order = models.PositiveSmallIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активно', default=True)
    
    class Meta:
        ordering = ['order']
        verbose_name = 'Особенность услуги'
        verbose_name_plural = 'Особенности услуги'
    
    def __str__(self):
        return f"{self.title} - {self.service_detail.title}"


class ServiceProcess(models.Model):
    """Модель для этапов работы"""
    service_detail = models.ForeignKey(
        ServiceDetail,
        on_delete=models.CASCADE,
        related_name='processes',
        verbose_name='Услуга'
    )
    
    step_number = models.PositiveSmallIntegerField(
        'Номер этапа',
        help_text='1, 2, 3...'
    )
    title = models.CharField(
        'Название этапа',
        max_length=200
    )
    description = models.TextField(
        'Описание этапа',
        max_length=500,
        blank=True,
        null=True
    )
    
    icon = models.ImageField(
        'Иконка',
        upload_to='service_processes/',
        blank=True,
        null=True
    )
    
    class Meta:
        ordering = ['step_number']
        unique_together = ['service_detail', 'step_number']
        verbose_name = 'Этап работы'
        verbose_name_plural = 'Этапы работы'
    
    def __str__(self):
        return f"Этап {self.step_number}: {self.title}"


class ServiceBenefit(models.Model):
    """Модель для преимуществ"""
    service_detail = models.ForeignKey(
        ServiceDetail,
        on_delete=models.CASCADE,
        related_name='benefits',
        verbose_name='Услуга'
    )
    
    title = models.CharField(
        'Преимущество',
        max_length=200
    )
    description = models.TextField(
        'Описание',
        max_length=400,
        blank=True,
        null=True
    )
    
    icon = models.ImageField(
        'Иконка',
        upload_to='service_benefits/',
        blank=True,
        null=True
    )
    
    order = models.PositiveSmallIntegerField('Порядок', default=0)
    
    class Meta:
        ordering = ['order']
        verbose_name = 'Преимущество'
        verbose_name_plural = 'Преимущества'
    
    def __str__(self):
        return self.title


class ServiceFAQ(models.Model):
    """Модель для частых вопросов"""
    service_detail = models.ForeignKey(
        ServiceDetail,
        on_delete=models.CASCADE,
        related_name='faqs',
        verbose_name='Услуга'
    )
    
    question = models.CharField(
        'Вопрос',
        max_length=300
    )
    answer = RichTextField(
        'Ответ',
        help_text='Ответ на вопрос с форматированием'
    )
    
    order = models.PositiveSmallIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активно', default=True)
    
    class Meta:
        ordering = ['order']
        verbose_name = 'Часто задаваемый вопрос'
        verbose_name_plural = 'Часто задаваемые вопросы'
    
    def __str__(self):
        return self.question


class ServiceCase(models.Model):
    """Модель для кейсов/примеров работ"""
    service_detail = models.ForeignKey(
        ServiceDetail,
        on_delete=models.CASCADE,
        related_name='cases',
        verbose_name='Услуга'
    )
    
    title = models.CharField(
        'Название кейса',
        max_length=200
    )
    client = models.CharField(
        'Клиент',
        max_length=200,
        blank=True,
        null=True
    )
    description = models.TextField(
        'Описание кейса',
        max_length=1000
    )
    
    image = models.ImageField(
        'Изображение',
        upload_to='service_cases/',
        blank=True,
        null=True
    )
    
    result = models.CharField(
        'Результат',
        max_length=200,
        help_text='Например: +150% к конверсии',
        blank=True,
        null=True
    )
    
    link = models.URLField(
        'Ссылка на проект',
        max_length=200,
        blank=True,
        null=True
    )
    
    order = models.PositiveSmallIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активно', default=True)
    
    class Meta:
        ordering = ['order']
        verbose_name = 'Кейс'
        verbose_name_plural = 'Кейсы'
    
    def __str__(self):
        return self.title

class Vacancy(models.Model):
    """Модель для вакансий"""
    EMPLOYMENT_TYPE_CHOICES = (
        ('Full-time', 'Полный рабочий день'),
        ('Part-time', 'Частичная занятость'),
        ('remote', 'Удаленная работа'),
        ('hybird', 'Гибридная работа'),
        ('internship', 'Стажировка'),
    )

    #уровни квалификации
    LEVEL_CHOICES = (
        ('junior', 'junior'),
        ('middle', 'middle'),
        ('senior', 'senior'),
    )

    # Категории
    CATEGORY_CHOICES = (
        ('Frontend', 'Frontend'),
        ('Backend', 'Backend'),
        ('Fullstack', 'Fullstack'),
    )
    #основная инфромация
    title = models.CharField(
        "названия вакансии", 
        max_length=200,
        help_text = CATEGORY_CHOICES,
        default='backend',
    )
    category = models.CharField(
        "Категория",
        max_length=200, 
        choices=CATEGORY_CHOICES, default='backend')
    level = models.CharField(
        'уровень квалификации',
        max_length=200,
        choices=LEVEL_CHOICES,
        default='junior'
    )

    employment_type = models.CharField(
        "Тип занятости",
        max_length=200,
        choices=EMPLOYMENT_TYPE_CHOICES,
        default='Full-time'
    )

    # ===== ТЕКСТОВЫЕ ПОЛЯ С CKEDITOR =====
    
    # Полное описание вакансии (объединенное поле)
    description = RichTextField(
        'Описание вакансии',
        help_text='Полное описание вакансии с форматированием',
        config_name='default'
    )
    
    # ===== ОСТАЛЬНЫЕ ПОЛЯ =====
    
    # Краткое описание для превью
    short_description = models.TextField(
        'Краткое описание',
        max_length=300,
        help_text='Краткое описание для карточки вакансии',
        blank=True,
        null=True
    )
    
    # Зарплатная вилка
    salary_min = models.PositiveIntegerField(
        'Зарплата от',
        blank=True,
        null=True,
        help_text='Минимальная зарплата в $'
    )
    salary_max = models.PositiveIntegerField(
        'Зарплата до',
        blank=True,
        null=True,
        help_text='Максимальная зарплата в $'
    )
    salary_text = models.CharField(
        'Текст о зарплате',
        max_length=100,
        blank=True,
        null=True,
        help_text='Например: "по результатам собеседования"'
    )
    
    # Email для откликов (из текста: motionwebteam@gmail.com)
    application_email = models.EmailField(
        'Email для откликов',
        max_length=254,
        help_text='На этот email будут приходить уведомления',
        blank=True,
        null=True
    )
    
    # Локация
    location = models.CharField(
        'Локация',
        max_length=200,
        default='г. Бишкек',
        help_text='Например: г. Бишкек, ул. Манас 60/1'
    )
    is_remote = models.BooleanField(
        'Удаленная работа',
        default=False,
        help_text='Можно работать удаленно?'
    )
    
    # Ключевые навыки (теги)
    skills = models.CharField(
        'Ключевые навыки',
        max_length=500,
        blank=True,
        null=True,
        help_text='Навыки через запятую (например: Python, Django, Docker)'
    )
    
    # Даты
    published_at = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        'Дата обновления',
        auto_now=True
    )
    expires_at = models.DateTimeField(
        'Дата окончания',
        blank=True,
        null=True,
        help_text='Дата, после которой вакансия не активна'
    )
    
    # Настройки отображения
    order = models.PositiveSmallIntegerField(
        'Порядок',
        default=0,
        help_text='Чем меньше число, тем выше позиция'
    )
    is_active = models.BooleanField(
        'Активно',
        default=True,
        help_text='Отображать вакансию на сайте?'
    )
    is_featured = models.BooleanField(
        'Рекламная',
        default=False,
        help_text='Выделять вакансию?'
    )
    views_count = models.PositiveIntegerField(
        'Просмотры',
        default=0,
        editable=False
    )
    
    class Meta:
        ordering = ['order', '-is_featured', '-published_at']
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
        indexes = [
            models.Index(fields=['category', 'level', 'employment_type']),
            models.Index(fields=['is_active', 'published_at']),
        ]
    
    def __str__(self):
        return f"{self.title} ({self.get_level_display()})"
    
    def increment_views(self):
        """Увеличить счетчик просмотров"""
        self.views_count += 1
        self.save(update_fields=['views_count'])
    
    @property
    def salary_range(self):
        """Форматирование зарплатной вилки"""
        if self.salary_min and self.salary_max:
            return f"{self.salary_min} - {self.salary_max}$"
        elif self.salary_min:
            return f"от {self.salary_min}$"
        elif self.salary_max:
            return f"до {self.salary_max}$"
        elif self.salary_text:
            return self.salary_text
        return "з/п не указана"


class VacancyApplication(models.Model):
    """Модель для откликов на вакансию (форма внизу)"""
    
    vacancy = models.ForeignKey(
        Vacancy,
        on_delete=models.CASCADE,
        related_name='applications',
        verbose_name='Вакансия'
    )
    
    # Поля из формы
    name = models.CharField(
        'Имя',
        max_length=200
    )
    phone = models.CharField(
        'Номер телефона',
        max_length=20
    )
    email = models.EmailField(
        'Электронная почта'
    )
    social_link = models.URLField(
        'Ссылка на соцсеть (LinkedIn)',
        max_length=500,
        blank=True,
        null=True,
        help_text='Ссылка на LinkedIn или другую соцсеть'
    )
    
    # Файл резюме
    resume = models.FileField(
        'Резюме',
        upload_to='vacancies/resumes/',
        validators=[
            FileExtensionValidator(
                allowed_extensions=['pdf', 'doc', 'docx', 'txt']
            )
        ],
        help_text='PDF, DOC, DOCX или TXT'
    )
    
    # Сопроводительное письмо (опционально)
    cover_letter = models.TextField(
        'Сопроводительное письмо',
        blank=True,
        null=True,
        help_text='Краткое сопроводительное письмо'
    )
    
    # Статус обработки
    status = models.CharField(
        'Статус',
        max_length=20,
        choices=[
            ('new', 'Новый'),
            ('viewed', 'Просмотрено'),
            ('interview', 'Собеседование'),
            ('test_task', 'Тестовое задание'),
            ('accepted', 'Принят'),
            ('rejected', 'Отказ'),
        ],
        default='new'
    )
    notes = models.TextField(
        'Заметки',
        blank=True,
        null=True,
        help_text='Внутренние заметки'
    )
    
    # Даты
    created_at = models.DateTimeField('Дата отклика', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Отклик на вакансию'
        verbose_name_plural = 'Отклики на вакансии'
    
    def __str__(self):
        return f"{self.name} - {self.vacancy.title}"



