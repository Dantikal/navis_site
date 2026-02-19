from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.decorators import action
from django.db import models
from django.shortcuts import get_object_or_404
from .models import (
    Service, Technology, Testimonial, Project,
    ContactRequest, ConsultationRequest, CompanyInfo, SiteContent,
    ServiceDetail, ServiceFeature, ServiceProcess,
    ServiceBenefit, ServiceFAQ, ServiceCase,
    Vacancy, VacancyApplication
)
from .serializers import (
    ServiceSerializer, TechnologySerializer, TestimonialSerializer,
    ProjectSerializer, ContactRequestSerializer, ConsultationRequestSerializer,
    CompanyInfoSerializer, SiteContentSerializer,
    VacancyListSerializer, VacancyDetailSerializer, VacancyApplicationSerializer
)
from .telegram_service import TelegramService

# ========== СУЩЕСТВУЮЩИЕ VIEWS ==========

# GET - список услуг
class ServiceListView(generics.ListAPIView):
    """Получение списка услуг/проектов"""
    queryset = Service.objects.filter(is_active=True).order_by('order')
    serializer_class = ServiceSerializer
    permission_classes = [AllowAny]

# POST - создание заявки (подписка)
class ContactCreateView(generics.CreateAPIView):
    """Создание заявки на обратную связь (Sign up to connect with us)"""
    queryset = ContactRequest.objects.all()
    serializer_class = ContactRequestSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            contact_request = serializer.save()
            
            # Отправляем уведомление в Telegram
            telegram_message = TelegramService.format_contact_request(contact_request)
            TelegramService.send_notification(telegram_message)
            
            return Response({
                'success': True,
                'message': 'Заявка успешно отправлена',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


# ========== НОВЫЕ VIEWS (из второго скриншота) ==========

# GET - список технологий
class TechnologyListView(generics.ListAPIView):
    """Получение списка технологий (секция 'Мы используем')"""
    queryset = Technology.objects.filter(is_active=True).order_by('order')
    serializer_class = TechnologySerializer
    permission_classes = [AllowAny]


# GET - список отзывов
class TestimonialListView(generics.ListAPIView):
    """Получение списка отзывов клиентов"""
    queryset = Testimonial.objects.filter(is_active=True).order_by('order')
    serializer_class = TestimonialSerializer
    permission_classes = [AllowAny]


# GET - список проектов (для оглавления)
class ProjectListView(generics.ListAPIView):
    """Получение списка проектов"""
    queryset = Project.objects.filter(is_active=True).order_by('order')
    serializer_class = ProjectSerializer
    permission_classes = [AllowAny]


# POST - создание заявки на консультацию
class ConsultationCreateView(generics.CreateAPIView):
    """Создание заявки на бесплатную консультацию"""
    queryset = ConsultationRequest.objects.all()
    serializer_class = ConsultationRequestSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            consultation = serializer.save()
            
            # Отправляем уведомление в Telegram
            telegram_message = TelegramService.format_consultation(consultation)
            TelegramService.send_notification(telegram_message)
            
            return Response({
                'success': True,
                'message': 'Заявка на консультацию отправлена',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


# GET - информация о компании
class CompanyInfoView(generics.RetrieveAPIView):
    """Получение контактной информации компании"""
    permission_classes = [AllowAny]
    serializer_class = CompanyInfoSerializer
    
    def get_object(self):
        obj = CompanyInfo.objects.first()
        if not obj:
            # Создаем с данными по умолчанию из скриншота
            obj = CompanyInfo.objects.create(
                phone="0502 800 202",
                address="г. Бишкек, ул. Манас 60/1",
                work_hours="с 10:00 до 19:00"
            )
        return obj


# GET - контент страницы
class SiteContentView(generics.RetrieveAPIView):
    """Получение контента главной страницы"""
    permission_classes = [AllowAny]
    serializer_class = SiteContentSerializer
    
    def get_object(self):
        obj = SiteContent.objects.filter(is_active=True).first()
        if not obj:
            obj = SiteContent.objects.create()
        return obj


# ========== КОМБИНИРОВАННЫЕ VIEWS ==========

# GET - все данные для главной страницы
class FullHomePageDataView(generics.GenericAPIView):
    """Получение всех данных для главной страницы"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        # Получаем все активные записи
        services = Service.objects.filter(is_active=True).order_by('order')[:6]
        technologies = Technology.objects.filter(is_active=True).order_by('order')
        testimonials = Testimonial.objects.filter(is_active=True).order_by('order')
        projects = Project.objects.filter(is_active=True).order_by('order')
        company_info = CompanyInfo.objects.first()
        site_content = SiteContent.objects.filter(is_active=True).first()
        
        # Сериализуем данные
        data = {
            'services': ServiceSerializer(services, many=True).data,
            'technologies': TechnologySerializer(technologies, many=True).data,
            'testimonials': TestimonialSerializer(testimonials, many=True).data,
            'projects': ProjectSerializer(projects, many=True).data,
            'company_info': CompanyInfoSerializer(company_info).data if company_info else None,
            'site_content': SiteContentSerializer(site_content).data if site_content else None,
        }
        
        return Response({
            'success': True,
            'data': data
        }
        )


# ========== НОВЫЕ VIEWS ДЛЯ ДЕТАЛЬНЫХ СТРАНИЦ УСЛУГ ==========

# GET - детальная информация об услуге по ID ServiceDetail
class ServiceDetailView(generics.RetrieveAPIView):
    """Получение детальной информации об услуге"""
    queryset = ServiceDetail.objects.filter(is_active=True)
    permission_classes = [AllowAny]
    
    def get_serializer_class(self):
        from .serializers import ServiceDetailSerializer
        return ServiceDetailSerializer


# GET - детальная информация об услуге по связанному service_id
class ServiceDetailByServiceView(generics.RetrieveAPIView):
    """Получение детальной информации об услуге по ID основной услуги"""
    permission_classes = [AllowAny]
    
    def get_object(self):
        service_id = self.kwargs['service_id']
        return ServiceDetail.objects.filter(service_id=service_id, is_active=True).first()
    
    def get_serializer_class(self):
        from .serializers import ServiceDetailSerializer
        return ServiceDetailSerializer


# GET - список всех детальных страниц услуг
class ServiceDetailListView(generics.ListAPIView):
    """Получение списка всех детальных страниц услуг"""
    queryset = ServiceDetail.objects.filter(is_active=True).order_by('-created_at')
    permission_classes = [AllowAny]
    
    def get_serializer_class(self):
        from .serializers import ServiceDetailSerializer
        return ServiceDetailSerializer


# GET - особенности конкретной услуги
class ServiceFeatureListView(generics.ListAPIView):
    """Получение особенностей конкретной услуги"""
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        service_detail_id = self.kwargs['service_detail_id']
        return ServiceFeature.objects.filter(service_detail_id=service_detail_id, is_active=True).order_by('order')
    
    def get_serializer_class(self):
        from .serializers import ServiceFeatureSerializer
        return ServiceFeatureSerializer


# GET - этапы работы конкретной услуги
class ServiceProcessListView(generics.ListAPIView):
    """Получение этапов работы конкретной услуги"""
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        service_detail_id = self.kwargs['service_detail_id']
        return ServiceProcess.objects.filter(service_detail_id=service_detail_id).order_by('step_number')
    
    def get_serializer_class(self):
        from .serializers import ServiceProcessSerializer
        return ServiceProcessSerializer


# GET - преимущества конкретной услуги
class ServiceBenefitListView(generics.ListAPIView):
    """Получение преимуществ конкретной услуги"""
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        service_detail_id = self.kwargs['service_detail_id']
        return ServiceBenefit.objects.filter(service_detail_id=service_detail_id).order_by('order')
    
    def get_serializer_class(self):
        from .serializers import ServiceBenefitSerializer
        return ServiceBenefitSerializer


# GET - FAQ конкретной услуги
class ServiceFAQListView(generics.ListAPIView):
    """Получение FAQ конкретной услуги"""
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        service_detail_id = self.kwargs['service_detail_id']
        return ServiceFAQ.objects.filter(service_detail_id=service_detail_id, is_active=True).order_by('order')
    
    def get_serializer_class(self):
        from .serializers import ServiceFAQSerializer
        return ServiceFAQSerializer


# GET - кейсы конкретной услуги
class ServiceCaseListView(generics.ListAPIView):
    """Получение кейсов конкретной услуги"""
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        service_detail_id = self.kwargs['service_detail_id']
        return ServiceCase.objects.filter(service_detail_id=service_detail_id, is_active=True).order_by('order')
    
    def get_serializer_class(self):
        from .serializers import ServiceCaseSerializer
        return ServiceCaseSerializer


# ========== VIEWSETS ДЛЯ АДМИНКИ ==========

class ServiceViewSet(viewsets.ModelViewSet):
    """ViewSet для полного управления услугами (админка)"""
    queryset = Service.objects.all()
    permission_classes = [IsAdminUser]
    
    def get_serializer_class(self):
        from .serializers import ServiceSerializer, ServiceAdminDetailSerializer
        if self.action == 'list':
            return ServiceSerializer
        return ServiceAdminDetailSerializer
    
    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        """Активировать/деактивировать услугу"""
        service = self.get_object()
        service.is_active = not service.is_active
        service.save()
        return Response({'status': 'success', 'is_active': service.is_active})


class TestimonialViewSet(viewsets.ModelViewSet):
    """ViewSet для полного управления отзывами (админка)"""
    queryset = Testimonial.objects.all()
    permission_classes = [IsAdminUser]
    
    def get_serializer_class(self):
        from .serializers import TestimonialSerializer, TestimonialDetailSerializer
        if self.action == 'list':
            return TestimonialSerializer
        return TestimonialDetailSerializer
    
    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        """Активировать/деактивировать отзыв"""
        testimonial = self.get_object()
        testimonial.is_active = not testimonial.is_active
        testimonial.save()
        return Response({'status': 'success', 'is_active': testimonial.is_active})


class ConsultationRequestViewSet(viewsets.ModelViewSet):
    """ViewSet для управления заявками на консультацию (админка)"""
    queryset = ConsultationRequest.objects.all()
    permission_classes = [IsAdminUser]
    
    def get_serializer_class(self):
        from .serializers import ConsultationRequestSerializer, ConsultationRequestDetailSerializer
        if self.action == 'list':
            return ConsultationRequestSerializer
        return ConsultationRequestDetailSerializer
    
    @action(detail=True, methods=['post'])
    def mark_processed(self, request, pk=None):
        """Отметить заявку как обработанную"""
        consultation = self.get_object()
        consultation.is_processed = True
        consultation.save()
        return Response({'status': 'success', 'is_processed': True})
    
    @action(detail=True, methods=['post'])
    def mark_unprocessed(self, request, pk=None):
        """Отметить заявку как необработанную"""
        consultation = self.get_object()
        consultation.is_processed = False
        consultation.save()
        return Response({'status': 'success', 'is_processed': False})


class ServiceDetailViewSet(viewsets.ModelViewSet):
    """ViewSet для полного управления детальными страницами услуг (админка)"""
    queryset = ServiceDetail.objects.all()
    permission_classes = [IsAdminUser]
    
    def get_serializer_class(self):
        from .serializers import ServiceDetailSerializer
        return ServiceDetailSerializer
    
    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        """Активировать/деактивировать детальную страницу"""
        service_detail = self.get_object()
        service_detail.is_active = not service_detail.is_active
        service_detail.save()
        return Response({'status': 'success', 'is_active': service_detail.is_active})

class VacancyListView(generics.ListAPIView):
    """Список всех активных вакансий"""
    queryset = Vacancy.objects.filter(is_active=True)
    serializer_class = VacancyListSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Фильтрация по категории
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        # Фильтрация по уровню
        level = self.request.query_params.get('level')
        if level:
            queryset = queryset.filter(level=level)
        
        # Фильтрация по типу занятости
        employment = self.request.query_params.get('employment_type')
        if employment:
            queryset = queryset.filter(employment_type=employment)
        
        return queryset

class VacancyDetailView(generics.RetrieveAPIView):
    """Детальная страница вакансии"""
    queryset = Vacancy.objects.filter(is_active=True)
    serializer_class = VacancyDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = 'pk'
    
    def retrieve(self, request, *args, **kwargs):
        # Увеличиваем счетчик просмотров
        instance = self.get_object()
        instance.increment_views()
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class VacancyApplicationCreateView(generics.CreateAPIView):
    """Создание отклика на вакансию"""
    serializer_class = VacancyApplicationSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        vacancy_id = kwargs.get('vacancy_id')
        vacancy = get_object_or_404(Vacancy, id=vacancy_id, is_active=True)
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            application = serializer.save(vacancy=vacancy)
            
            # Отправка уведомления на email (опционально)
            # send_application_notification(application)
            
            return Response({
                'success': True,
                'message': 'Отклик успешно отправлен',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)