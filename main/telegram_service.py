import os
import json
import urllib.request
import urllib.parse
from django.conf import settings


class TelegramService:
    """Сервис для отправки уведомлений в Telegram"""
    
    @staticmethod
    def send_notification(message):
        """Отправка сообщения в Telegram группу"""
        try:
            bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
            chat_id = os.environ.get('TELEGRAM_CHAT_ID')
            
            if not bot_token or not chat_id:
                print("Telegram credentials not configured")
                return False
            
            # Формируем URL для API Telegram
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            
            # Подготавливаем данные
            data = {
                'chat_id': chat_id,
                'text': message
            }
            
            # Кодируем данные и отправляем запрос
            encoded_data = urllib.parse.urlencode(data).encode('utf-8')
            req = urllib.request.Request(
                url,
                data=encoded_data,
                headers={'Content-Type': 'application/x-www-form-urlencoded'}
            )
            
            # Отправляем запрос
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
                
            if result.get('ok'):
                print("Telegram notification sent successfully")
                return True
            else:
                print(f"Telegram error: {result}")
                return False
                
        except Exception as e:
            print(f"Error sending Telegram notification: {e}")
            return False
    
    @staticmethod
    def format_contact_request(contact_request):
        """Форматирует данные заявки для отправки в Telegram"""
        message = f"""
🆕 <b>Новая заявка!</b>

📞 <b>Телефон:</b> {contact_request.phone}
📧 <b>Email:</b> {contact_request.email}
🕐 <b>Дата:</b> {contact_request.created_at.strftime('%d.%m.%Y %H:%M')}

<i>Заявка создана через сайт</i>
        """.strip()
        
        return message
