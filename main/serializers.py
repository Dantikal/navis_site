from rest_framework import serializers
from .models import (
    Service, Technology, Testimonial, Project,
    ContactRequest, ConsultationRequest, CompanyInfo, SiteContent,
    ServiceDetail, ServiceFeature, ServiceProcess,
    ServiceBenefit, ServiceFAQ, ServiceCase,
    Vacancy, VacancyApplication
)

# ========== СУЩЕСТВУЮЩИЕ СЕРИАЛИЗАТОРЫ ==========

class ServiceSerializer(serializers.ModelSerializer):
    """Сериализатор для услуг"""
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Service
        fields = ['id', 'title', 'description', 'name', 'image', 'image_url', 'url', 'order']
        read_only_fields = ['id']
    
    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url
        return None


class ContactRequestSerializer(serializers.ModelSerializer):
    """Сериализатор для заявок (подписка)"""
    class Meta:
        model = ContactRequest
        fields = ['id', 'phone', 'email', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def validate(self, data):
        """Проверяем, что указан хотя бы один способ связи"""
        if not data.get('email') and not data.get('phone'):
            raise serializers.ValidationError("Укажите хотя бы email или телефон")
        return data


# ========== НОВЫЕ СЕРИАЛИЗАТОРЫ ==========

class TechnologySerializer(serializers.ModelSerializer):
    """Сериализатор для технологий"""
    logo_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Technology
        fields = ['id', 'name', 'logo', 'logo_url', 'url', 'order']
        read_only_fields = ['id']
    
    def get_logo_url(self, obj):
        if obj.logo:
            return obj.logo.url
        return None


class TestimonialSerializer(serializers.ModelSerializer):
    """Сериализатор для отзывов клиентов"""
    client_photo_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Testimonial
        fields = [
            'id', 'client_name', 'client_position', 'client_company',
            'client_photo', 'client_photo_url', 'text', 'rating', 
            'project_link', 'order'
        ]
        read_only_fields = ['id']
    
    def get_client_photo_url(self, obj):
        if obj.client_photo:
            return obj.client_photo.url
        return None


class ProjectSerializer(serializers.ModelSerializer):
    """Сериализатор для проектов (оглавление)"""
    image_url = serializers.SerializerMethodField()
    project_type_display = serializers.CharField(
        source='get_project_type_display', 
        read_only=True
    )
    
    class Meta:
        model = Project
        fields = [
            'id', 'title', 'project_type', 'project_type_display',
            'description', 'image', 'image_url', 'url', 'order'
        ]
        read_only_fields = ['id']
    
    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url
        return None


class ConsultationRequestSerializer(serializers.ModelSerializer):
    """Сериализатор для заявок на консультацию"""
    interest_display = serializers.SerializerMethodField()
    
    class Meta:
        model = ConsultationRequest
        fields = [
            'id', 'name', 'phone', 'interest', 'interest_other',
            'interest_display', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'interest_display']
    
    def validate(self, data):
        """Валидация: если выбран 'Другое', нужно заполнить interest_other"""
        if data.get('interest') == 'other' and not data.get('interest_other'):
            raise serializers.ValidationError({
                'interest_other': 'Укажите, что вас интересует'
            })
        
        # Валидация телефона (можно добавить)
        phone = data.get('phone')
        if phone and len(phone) < 10:
            raise serializers.ValidationError({
                'phone': 'Номер телефона слишком короткий'
            })
        
        return data
    
    def get_interest_display(self, obj):
        """Возвращает текстовое представление интереса"""
        return obj.interest_display


class CompanyInfoSerializer(serializers.ModelSerializer):
    """Сериализатор для информации о компании"""
    
    class Meta:
        model = CompanyInfo
        fields = [
            'phone', 'phone_additional', 'address', 'address_map_link',
            'work_hours', 'email', 'instagram', 'facebook', 'telegram', 'whatsapp'
        ]


class SiteContentSerializer(serializers.ModelSerializer):
    """Сериализатор для контента страницы"""
    logo_url = serializers.SerializerMethodField()
    favicon_url = serializers.SerializerMethodField()
    hero_image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = SiteContent
        fields = [
            # Заголовки секций
            'hero_title', 'technologies_title', 'projects_title',
            'testimonials_title', 'consultation_title',
            
            # Тексты и кнопки
            'subscription_text', 'button_text', 'all_projects_text', 
            'send_button_text',
            
            # Изображения
            'logo_url', 'favicon_url', 'hero_image_url',
            
            # Мета данные
            'meta_title', 'meta_description'
        ]
    
    def get_logo_url(self, obj):
        return obj.logo.url if obj.logo else None
    
    def get_favicon_url(self, obj):
        return obj.favicon.url if obj.favicon else None
    
    def get_hero_image_url(self, obj):
        return obj.hero_image.url if obj.hero_image else None


# ========== КОМБИНИРОВАННЫЕ СЕРИАЛИЗАТОРЫ ==========

class HomePageDataSerializer(serializers.Serializer):
    """Сериализатор для всех данных главной страницы"""
    services = ServiceSerializer(many=True, read_only=True)
    technologies = TechnologySerializer(many=True, read_only=True)
    testimonials = TestimonialSerializer(many=True, read_only=True)
    projects = ProjectSerializer(many=True, read_only=True)
    company_info = CompanyInfoSerializer(read_only=True)
    site_content = SiteContentSerializer(read_only=True)


# ========== ДЕТАЛЬНЫЕ СЕРИАЛИЗАТОРЫ ДЛЯ АДМИНКИ ==========

class ServiceAdminDetailSerializer(serializers.ModelSerializer):
    """Детальный сериализатор для услуг (с дополнительными полями)"""
    image_url = serializers.SerializerMethodField()
    created_at_formatted = serializers.DateTimeField(
        source='created_at', 
        format='%d.%m.%Y %H:%M',
        read_only=True
    )
    updated_at_formatted = serializers.DateTimeField(
        source='updated_at', 
        format='%d.%m.%Y %H:%M',
        read_only=True
    )
    
    class Meta:
        model = Service
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
    
    def get_image_url(self, obj):
        return obj.image.url if obj.image else None


class TestimonialDetailSerializer(serializers.ModelSerializer):
    """Детальный сериализатор для отзывов"""
    client_photo_url = serializers.SerializerMethodField()
    created_at_formatted = serializers.DateTimeField(
        source='created_at', 
        format='%d.%m.%Y %H:%M',
        read_only=True
    )
    
    class Meta:
        model = Testimonial
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
    
    def get_client_photo_url(self, obj):
        return obj.client_photo.url if obj.client_photo else None


class ConsultationRequestDetailSerializer(serializers.ModelSerializer):
    """Детальный сериализатор для заявок на консультацию"""
    interest_display = serializers.SerializerMethodField()
    created_at_formatted = serializers.DateTimeField(
        source='created_at', 
        format='%d.%m.%Y %H:%M',
        read_only=True
    )
    
    class Meta:
        model = ConsultationRequest
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
    
    def get_interest_display(self, obj):
        return obj.interest_display


# ========== СЕРИАЛИЗАТОРЫ ДЛЯ ДЕТАЛЬНЫХ СТРАНИЦ УСЛУГ ==========

class ServiceDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для детальных страниц услуг"""
    main_image_url = serializers.SerializerMethodField()
    banner_image_url = serializers.SerializerMethodField()
    service_title = serializers.CharField(source='service.title', read_only=True)
    
    class Meta:
        model = ServiceDetail
        fields = [
            'id', 'title', 'subtitle', 'short_description', 'description',
            'main_image', 'main_image_url', 'banner_image', 'banner_image_url',
            'meta_title', 'meta_description', 'is_active', 'created_at', 'updated_at',
            'service', 'service_title'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_main_image_url(self, obj):
        return obj.main_image.url if obj.main_image else None
    
    def get_banner_image_url(self, obj):
        return obj.banner_image.url if obj.banner_image else None


class ServiceFeatureSerializer(serializers.ModelSerializer):
    """Сериализатор для особенностей услуги"""
    icon_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ServiceFeature
        fields = [
            'id', 'title', 'description', 'icon', 'icon_url', 
            'icon_class', 'link', 'link_text', 'order', 'is_active'
        ]
    
    def get_icon_url(self, obj):
        return obj.icon.url if obj.icon else None


class ServiceProcessSerializer(serializers.ModelSerializer):
    """Сериализатор для этапов работы"""
    icon_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ServiceProcess
        fields = [
            'id', 'step_number', 'title', 'description', 
            'icon', 'icon_url'
        ]
    
    def get_icon_url(self, obj):
        return obj.icon.url if obj.icon else None


class ServiceBenefitSerializer(serializers.ModelSerializer):
    """Сериализатор для преимуществ"""
    icon_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ServiceBenefit
        fields = [
            'id', 'title', 'description', 'icon', 'icon_url', 'order'
        ]
    
    def get_icon_url(self, obj):
        return obj.icon.url if obj.icon else None


class ServiceFAQSerializer(serializers.ModelSerializer):
    """Сериализатор для FAQ"""
    
    class Meta:
        model = ServiceFAQ
        fields = [
            'id', 'question', 'answer', 'order', 'is_active'
        ]


class ServiceCaseSerializer(serializers.ModelSerializer):
    """Сериализатор для кейсов"""
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ServiceCase
        fields = [
            'id', 'title', 'client', 'description', 'image', 'image_url',
            'result', 'link', 'order', 'is_active'
        ]
    
    def get_image_url(self, obj):
        return obj.image.url if obj.image else None


# ========== СЕРИАЛИЗАТОРЫ ДЛЯ ВАКАНСИЙ ==========

class VacancyListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка вакансий"""
    salary_range = serializers.ReadOnlyField()
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    level_display = serializers.CharField(source='get_level_display', read_only=True)
    employment_type_display = serializers.CharField(source='get_employment_type_display', read_only=True)
    
    class Meta:
        model = Vacancy
        fields = [
            'id', 'title', 'category', 'category_display', 'level', 'level_display',
            'employment_type', 'employment_type_display', 'salary_range', 'location',
            'is_remote', 'is_featured', 'views_count', 'published_at', 'short_description'
        ]


class VacancyDetailSerializer(serializers.ModelSerializer):
    """Детальный сериализатор для вакансии"""
    salary_range = serializers.ReadOnlyField()
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    level_display = serializers.CharField(source='get_level_display', read_only=True)
    employment_type_display = serializers.CharField(source='get_employment_type_display', read_only=True)
    skills_list = serializers.SerializerMethodField()
    
    class Meta:
        model = Vacancy
        fields = '__all__'
    
    def get_skills_list(self, obj):
        """Преобразует строку навыков в список"""
        if obj.skills:
            return [skill.strip() for skill in obj.skills.split(',')]
        return []


class VacancyApplicationSerializer(serializers.ModelSerializer):
    """Сериализатор для откликов на вакансии"""
    resume_url = serializers.SerializerMethodField()
    vacancy_title = serializers.CharField(source='vacancy.title', read_only=True)
    
    class Meta:
        model = VacancyApplication
        fields = [
            'id', 'name', 'email', 'phone', 'social_link', 'resume', 
            'resume_url', 'cover_letter', 'status', 'vacancy', 'vacancy_title',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'resume_url', 'vacancy_title']
    
    def get_resume_url(self, obj):
        return obj.resume.url if obj.resume else None
    
    def validate(self, data):
        """Валидация: хотя бы один из email или телефон должен быть указан"""
        if not data.get('email') and not data.get('phone'):
            raise serializers.ValidationError("Укажите хотя бы email или телефон")
        return data
