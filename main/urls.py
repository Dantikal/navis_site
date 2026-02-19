"""
API URL Configuration for Navis Site

Доступные эндпоинты:

Документация API:
- /api/schema/ - OpenAPI схема
- /api/docs/ - Swagger UI
- /api/redoc/ - ReDoc документация

Публичные эндпоинты:
GET /api/services/ - Получить все услуги
GET /api/technologies/ - Получить все технологии
GET /api/testimonials/ - Получить все отзывы
GET /api/projects/ - Получить все проекты
GET /api/company-info/ - Получить контакты компании
GET /api/site-content/ - Получить контент страницы
GET /api/full-homepage/ - Получить ВСЕ данные сразу
POST /api/contact/ - Отправить заявку (подписка)
POST /api/consultation/ - Отправить заявку на консультацию

Детальные страницы услуг:
GET /api/service-details/ - Получить все детальные страницы услуг
GET /api/service-details/<int:pk>/ - Получить детальную информацию об услуге по ID
GET /api/service-details/by-service/<int:service_id>/ - Получить детальную информацию по service_id
GET /api/service-details/<int:service_detail_id>/features/ - Получить особенности услуги
GET /api/service-details/<int:service_detail_id>/processes/ - Получить этапы работы
GET /api/service-details/<int:service_detail_id>/benefits/ - Получить преимущества
GET /api/service-details/<int:service_detail_id>/faqs/ - Получить FAQ
GET /api/service-details/<int:service_detail_id>/cases/ - Получить кейсы

Вакансии:
GET /api/vacancies/ - Получить список вакансий (с фильтрацией)
GET /api/vacancies/<int:pk>/ - Получить детальную информацию о вакансии
POST /api/vacancies/<int:vacancy_id>/apply/ - Создать отклик на вакансию

Административные эндпоинты (требуют аутентификации):
/api/services/admin/ - Управление услугами (CRUD + toggle_active)
/api/testimonials/admin/ - Управление отзывами (CRUD + toggle_active)
/api/consultations/admin/ - Управление заявками (CRUD + mark_processed/unprocessed)
/api/service-details/admin/ - Управление детальными страницами (CRUD + toggle_active)
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Router для ViewSet'ов (админские эндпоинты)
router = DefaultRouter()
router.register(r'services/admin', views.ServiceViewSet, basename='service-admin')
router.register(r'testimonials/admin', views.TestimonialViewSet, basename='testimonial-admin')
router.register(r'consultations/admin', views.ConsultationRequestViewSet, basename='consultation-admin')
router.register(r'service-details/admin', views.ServiceDetailViewSet, basename='servicedetail-admin')

urlpatterns = [
    # ========== ПУБЛИЧНЫЕ ЭНДПОИНТЫ ==========
    
    # Услуги
    path('api/services/', views.ServiceListView.as_view(), name='service-list'),
    
    # ========== НОВЫЕ ЭНДПОИНТЫ ДЛЯ ДЕТАЛЬНЫХ СТРАНИЦ УСЛУГ ==========
    
    # Получить детальную информацию об услуге по ID ServiceDetail
    path('api/service-details/<int:pk>/', views.ServiceDetailView.as_view(), name='service-detail'),
    
    # Получить детальную информацию об услуге по связанному service_id
    path('api/service-details/by-service/<int:service_id>/', 
         views.ServiceDetailByServiceView.as_view(), 
         name='service-detail-by-service'),
    
    # Получить все детальные страницы услуг (с фильтрацией)
    path('api/service-details/', views.ServiceDetailListView.as_view(), name='service-detail-list'),
    
    # Получить особенности конкретной услуги
    path('api/service-details/<int:service_detail_id>/features/', 
         views.ServiceFeatureListView.as_view(), 
         name='service-features'),
    
    # Получить этапы работы конкретной услуги
    path('api/service-details/<int:service_detail_id>/processes/', 
         views.ServiceProcessListView.as_view(), 
         name='service-processes'),
    
    # Получить преимущества конкретной услуги
    path('api/service-details/<int:service_detail_id>/benefits/', 
         views.ServiceBenefitListView.as_view(), 
         name='service-benefits'),
    
    # Получить FAQ конкретной услуги
    path('api/service-details/<int:service_detail_id>/faqs/', 
         views.ServiceFAQListView.as_view(), 
         name='service-faqs'),
    
    # Получить кейсы конкретной услуги
    path('api/service-details/<int:service_detail_id>/cases/', 
         views.ServiceCaseListView.as_view(), 
         name='service-cases'),
    
    # ========== СУЩЕСТВУЮЩИЕ ЭНДПОИНТЫ ==========
    
    # Технологии
    path('api/technologies/', views.TechnologyListView.as_view(), name='technology-list'),
    
    # Отзывы
    path('api/testimonials/', views.TestimonialListView.as_view(), name='testimonial-list'),
    
    # Проекты
    path('api/projects/', views.ProjectListView.as_view(), name='project-list'),
    
    # Контакты и заявки
    path('api/contact/', views.ContactCreateView.as_view(), name='contact-create'),
    path('api/consultation/', views.ConsultationCreateView.as_view(), name='consultation-create'),
    
    # Информация о компании
    path('api/company-info/', views.CompanyInfoView.as_view(), name='company-info'),
    path('api/site-content/', views.SiteContentView.as_view(), name='site-content'),
    
    # Комбинированные эндпоинты
    path('api/full-homepage/', views.FullHomePageDataView.as_view(), name='full-homepage'),

    # ========== ВАКАНСИИ ==========
    path('api/vacancies/', views.VacancyListView.as_view(), name='vacancy-list'),
    path('api/vacancies/<int:pk>/', views.VacancyDetailView.as_view(), name='vacancy-detail'),
    path('api/vacancies/<int:vacancy_id>/apply/', 
         views.VacancyApplicationCreateView.as_view(), 
         name='vacancy-apply'),
    
    # ========== АДМИНСКИЕ ЭНДПОИНТЫ ==========
    path('api/', include(router.urls)),
]




# Если хотите версионирование API, можно добавить:
"""
urlpatterns = [
    path('api/v1/', include([
        path('services/', views.ServiceListView.as_view()),
        path('technologies/', views.TechnologyListView.as_view()),
        path('testimonials/', views.TestimonialListView.as_view()),
        path('projects/', views.ProjectListView.as_view()),
        path('contact/', views.ContactCreateView.as_view()),
        path('consultation/', views.ConsultationCreateView.as_view()),
        path('company-info/', views.CompanyInfoView.as_view()),
        path('site-content/', views.SiteContentView.as_view()),
        path('full-homepage/', views.FullHomePageDataView.as_view()),
        path('', include(router.urls)),
    ])),
]








Метод	URL	Описание
/api/schema/ - OpenAPI схема
/api/docs/ - Swagger UI
/api/redoc/ - ReDoc документация

# GET /api/vacancies/1/  (где 1 - ID вакансии)
# GET /api/vacancies/1/  (где 1 - ID вакансии)
# POST /api/vacancies/1/apply/  (где 1 - ID вакансии)

GET	/api/services/	Получить все услуги
GET	/api/technologies/	Получить все технологии
GET	/api/testimonials/	Получить все отзывы
GET	/api/projects/	Получить все проекты
GET	/api/company-info/	Получить контакты компании
GET	/api/site-content/	Получить контент страницы
GET	/api/full-homepage/	Получить ВСЕ данные сразу
POST	/api/contact/	Отправить заявку (подписка)
POST	/api/consultation/	Отправить заявку на консультацию

# ========== НОВЫЕ ЭНДПОИНТЫ ДЛЯ ДЕТАЛЬНЫХ СТРАНИЦ УСЛУГ ==========
GET	/api/service-details/	Получить все детальные страницы услуг
GET	/api/service-details/<int:pk>/	Получить детальную информацию об услуге по ID
GET	/api/service-details/by-service/<int:service_id>/	Получить детальную информацию по service_id
GET	/api/service-details/<int:service_detail_id>/features/	Получить особенности услуги
GET	/api/service-details/<int:service_detail_id>/processes/	Получить этапы работы
GET	/api/service-details/<int:service_detail_id>/benefits/	Получить преимущества
GET	/api/service-details/<int:service_detail_id>/faqs/	Получить FAQ
GET	/api/service-details/<int:service_detail_id>/cases/	Получить кейсы
"""
