from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from unfold.contrib.filters import AdminFilters
from unfold.contrib.forms import UserCreationForm, UserChangeForm
from .models import (
    Service, Technology, Testimonial, Project,
    ContactRequest, ConsultationRequest, CompanyInfo, SiteContent,
    ServiceDetail, ServiceFeature, ServiceProcess,
    ServiceBenefit, ServiceFAQ, ServiceCase
)

class ServiceFeatureInline(admin.TabularInline):
    """Инлайн для особенностей услуги"""
    model = ServiceFeature
    extra = 1
    fields = ['title', 'order', 'is_active', 'icon_preview', 'link']
    readonly_fields = ['icon_preview']
    
    def icon_preview(self, obj):
        if obj.icon:
            return format_html(
                '<img src="{}" style="max-height: 30px;" />', 
                obj.icon.url
            )
        return "—"
    icon_preview.short_description = 'Иконка'


class ServiceProcessInline(admin.TabularInline):
    """Инлайн для этапов работы"""
    model = ServiceProcess
    extra = 1
    fields = ['step_number', 'title', 'icon_preview']
    readonly_fields = ['icon_preview']
    
    def icon_preview(self, obj):
        if obj.icon:
            return format_html(
                '<img src="{}" style="max-height: 30px;" />', 
                obj.icon.url
            )
        return "—"
    icon_preview.short_description = 'Иконка'


class ServiceBenefitInline(admin.TabularInline):
    """Инлайн для преимуществ"""
    model = ServiceBenefit
    extra = 1
    fields = ['title', 'order', 'icon_preview']
    readonly_fields = ['icon_preview']
    
    def icon_preview(self, obj):
        if obj.icon:
            return format_html(
                '<img src="{}" style="max-height: 30px;" />', 
                obj.icon.url
            )
        return "—"
    icon_preview.short_description = 'Иконка'


class ServiceFAQInline(admin.TabularInline):
    """Инлайн для частых вопросов"""
    model = ServiceFAQ
    extra = 1
    fields = ['question', 'order', 'is_active']


class ServiceCaseInline(admin.TabularInline):
    """Инлайн для кейсов"""
    model = ServiceCase
    extra = 1
    fields = ['title', 'order', 'is_active', 'image_preview']
    readonly_fields = ['image_preview']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 50px;" />', 
                obj.image.url
            )
        return "—"
    image_preview.short_description = 'Превью'


@admin.register(ServiceDetail)
class ServiceDetailAdmin(ModelAdmin):
    """Админка для детальной страницы услуги"""
    list_display = [
        'title', 'service_link', 'is_active', 
        'features_count', 'cases_count', 'created_at'
    ]
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']
    prepopulated_fields = {'meta_title': ('title',)}
    readonly_fields = [
        'created_at', 'updated_at', 
        'main_image_preview', 'banner_image_preview'
    ]
    
    fieldsets = (
        ('Связь с основной услугой', {
            'fields': ('service',),
            'description': 'Если выбрать существующую услугу, она будет связана с этой детальной страницей'
        }),
        ('Основная информация', {
            'fields': (
                'title', 'subtitle', 'short_description'
            )
        }),
        ('Полное описание (CKEditor)', {
            'fields': ('description',),
            'classes': ('wide',),
            'description': 'Используйте редактор для форматирования текста'
        }),
        ('Изображения', {
            'fields': (
                ('main_image', 'main_image_preview'),
                ('banner_image', 'banner_image_preview')
            ),
            'description': 'Рекомендуемый размер главного изображения: 1200x630px'
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',),
            'description': 'Настройки для поисковых систем'
        }),
        ('Настройки', {
            'fields': ('is_active', 'created_at', 'updated_at')
        }),
    )
    
    inlines = [
        ServiceFeatureInline,
        ServiceProcessInline,
        ServiceBenefitInline,
        ServiceFAQInline,
        ServiceCaseInline
    ]
    
    def service_link(self, obj):
        """Ссылка на связанную услугу"""
        if obj.service:
            return format_html(
                '<a href="/admin/main/service/{}/change/">{}</a>',
                obj.service.id,
                obj.service.title
            )
        return "—"
    service_link.short_description = "Связанная услуга"
    
    def features_count(self, obj):
        """Количество особенностей"""
        count = obj.features.count()
        return format_html('<b style="color: {};">{}</b>', 
                          'green' if count > 0 else 'gray', count)
    features_count.short_description = "📊 Особенности"
    
    def cases_count(self, obj):
        """Количество кейсов"""
        count = obj.cases.count()
        return format_html('<b style="color: {};">{}</b>', 
                          'green' if count > 0 else 'gray', count)
    cases_count.short_description = "📁 Кейсы"
    
    def main_image_preview(self, obj):
        """Превью главного изображения"""
        if obj.main_image:
            return format_html(
                '<img src="{}" style="max-height: 100px; border-radius: 5px;" />',
                obj.main_image.url
            )
        return "Нет изображения"
    main_image_preview.short_description = "Превью"
    
    def banner_image_preview(self, obj):
        """Превью баннера"""
        if obj.banner_image:
            return format_html(
                '<img src="{}" style="max-height: 60px; border-radius: 5px;" />',
                obj.banner_image.url
            )
        return "Нет изображения"
    banner_image_preview.short_description = "Превью баннера"
    
    actions = ['duplicate_service', 'toggle_active']
    
    def duplicate_service(self, request, queryset):
        """Дублирование услуги"""
        for obj in queryset:
            obj.pk = None
            obj.title = f"{obj.title} (копия)"
            obj.is_active = False
            obj.save()
        self.message_user(request, f"Создано {queryset.count()} копий")
    duplicate_service.short_description = "📋 Создать копию"
    
    def toggle_active(self, request, queryset):
        """Переключение активности"""
        for obj in queryset:
            obj.is_active = not obj.is_active
            obj.save()
        self.message_user(request, f"Статус активности изменен для {queryset.count()} записей")
    toggle_active.short_description = "🔄 Переключить активность"


@admin.register(ServiceFeature)
class ServiceFeatureAdmin(admin.ModelAdmin):
    """Админка для особенностей услуги"""
    list_display = [
        'title', 'service_detail', 'order', 
        'is_active', 'icon_preview', 'link'
    ]
    list_editable = ['order', 'is_active']
    list_filter = ['is_active', 'service_detail']
    search_fields = ['title', 'description']
    readonly_fields = ['icon_preview']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('service_detail', 'title', 'description')
        }),
        ('Иконка', {
            'fields': ('icon', 'icon_preview', 'icon_class'),
            'description': 'Загрузите иконку или укажите CSS класс'
        }),
        ('Ссылка', {
            'fields': ('link', 'link_text')
        }),
        ('Настройки', {
            'fields': ('order', 'is_active')
        }),
    )
    
    def icon_preview(self, obj):
        if obj.icon:
            return format_html(
                '<img src="{}" style="max-height: 40px;" />', 
                obj.icon.url
            )
        elif obj.icon_class:
            return format_html(
                '<span style="font-size: 24px;">📎 {}</span>', 
                obj.icon_class
            )
        return "—"
    icon_preview.short_description = "Превью иконки"


@admin.register(ServiceProcess)
class ServiceProcessAdmin(admin.ModelAdmin):
    """Админка для этапов работы"""
    list_display = ['step_number', 'title', 'service_detail', 'icon_preview']
    list_filter = ['service_detail']
    search_fields = ['title', 'description']
    readonly_fields = ['icon_preview']
    
    fieldsets = (
        ('Информация', {
            'fields': ('service_detail', 'step_number', 'title', 'description')
        }),
        ('Иконка', {
            'fields': ('icon', 'icon_preview')
        }),
    )
    
    def icon_preview(self, obj):
        if obj.icon:
            return format_html(
                '<img src="{}" style="max-height: 30px;" />', 
                obj.icon.url
            )
        return "—"
    icon_preview.short_description = "Иконка"


@admin.register(ServiceBenefit)
class ServiceBenefitAdmin(admin.ModelAdmin):
    """Админка для преимуществ"""
    list_display = ['title', 'service_detail', 'order', 'icon_preview']
    list_editable = ['order']
    list_filter = ['service_detail']
    search_fields = ['title']
    readonly_fields = ['icon_preview']
    
    def icon_preview(self, obj):
        if obj.icon:
            return format_html(
                '<img src="{}" style="max-height: 30px;" />', 
                obj.icon.url
            )
        return "—"
    icon_preview.short_description = "Иконка"


@admin.register(ServiceFAQ)
class ServiceFAQAdmin(admin.ModelAdmin):
    """Админка для частых вопросов"""
    list_display = ['question', 'service_detail', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active', 'service_detail']
    search_fields = ['question', 'answer']
    
    fieldsets = (
        ('Информация', {
            'fields': ('service_detail', 'question', 'answer')
        }),
        ('Настройки', {
            'fields': ('order', 'is_active')
        }),
    )


@admin.register(ServiceCase)
class ServiceCaseAdmin(admin.ModelAdmin):
    """Админка для кейсов"""
    list_display = [
        'title', 'client', 'service_detail', 
        'order', 'is_active', 'image_preview'
    ]
    list_editable = ['order', 'is_active']
    list_filter = ['is_active', 'service_detail']
    search_fields = ['title', 'client', 'description']
    readonly_fields = ['image_preview']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('service_detail', 'title', 'client', 'description')
        }),
        ('Результат', {
            'fields': ('result', 'link')
        }),
        ('Изображение', {
            'fields': ('image', 'image_preview')
        }),
        ('Настройки', {
            'fields': ('order', 'is_active')
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 100px; border-radius: 5px;" />', 
                obj.image.url
            )
        return "Нет изображения"
    image_preview.short_description = "Превью"

from django.utils.html import format_html
from .models import Vacancy, VacancyApplication

@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'category', 'level', 'employment_type',
        'salary_range_display', 'is_active', 'is_featured', 
        'views_count'
    ]
    list_editable = ['is_active', 'is_featured']
    list_filter = ['category', 'level', 'employment_type', 'is_active', 'is_featured']
    search_fields = ['title', 'description', 'skills']
    readonly_fields = ['views_count', 'updated_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': (
                'title', 'category', 'level', 'employment_type',
                'short_description'
            )
        }),
        ('Описание (CKEditor)', {
            'fields': ('description',),
            'classes': ('wide',)
        }),
        ('Зарплата и локация', {
            'fields': (
                ('salary_min', 'salary_max', 'salary_text'),
                'location', 'is_remote',
                'application_email'
            )
        }),
        ('Навыки', {
            'fields': ('skills',)
        }),
        ('Настройки', {
            'fields': (
                'order', 'is_active', 'is_featured',
                'expires_at'
            )
        }),
        ('Статистика', {
            'fields': ('views_count', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def salary_range_display(self, obj):
        return obj.salary_range
    salary_range_display.short_description = 'Зарплата'
    
    actions = ['duplicate_vacancy', 'toggle_featured']
    
    def duplicate_vacancy(self, request, queryset):
        for obj in queryset:
            obj.pk = None
            obj.title = f"{obj.title} (копия)"
            obj.is_active = False
            obj.save()
        self.message_user(request, f"Создано {queryset.count()} копий")
    duplicate_vacancy.short_description = "📋 Создать копию"
    
    def toggle_featured(self, request, queryset):
        for obj in queryset:
            obj.is_featured = not obj.is_featured
            obj.save()
        self.message_user(request, f"Статус изменен для {queryset.count()} вакансий")
    toggle_featured.short_description = "⭐ Переключить рекламные"


@admin.register(VacancyApplication)
class VacancyApplicationAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'vacancy', 'status', 'created_at']
    list_editable = ['status']
    list_filter = ['status', 'vacancy', 'created_at']
    search_fields = ['name', 'email', 'phone']
    readonly_fields = ['created_at', 'updated_at', 'resume_link']
    date_hierarchy = 'created_at'
    actions = ['mark_as_viewed', 'mark_as_interview']
    
    fieldsets = (
        ('Информация о кандидате', {
            'fields': ('name', 'email', 'phone', 'social_link')
        }),
        ('Документы', {
            'fields': ('resume', 'resume_link', 'cover_letter')
        }),
        ('Вакансия', {
            'fields': ('vacancy',)
        }),
        ('Статус', {
            'fields': ('status', 'notes')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def resume_link(self, obj):
        if obj.resume:
            return format_html(
                '<a href="{}" target="_blank">📄 Скачать резюме</a>',
                obj.resume.url
            )
        return "—"
    resume_link.short_description = "Файл"
    
    def mark_as_viewed(self, request, queryset):
        queryset.update(status='viewed')
    mark_as_viewed.short_description = "👁️ Отметить как просмотренные"
    
    def mark_as_interview(self, request, queryset):
        queryset.update(status='interview')
    mark_as_interview.short_description = "🤝 Назначить собеседование"