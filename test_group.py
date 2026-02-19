import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from main.telegram_service import TelegramService

# Тест отправки в группу
test_message = "🧪 Тест в группу Navis_Ac"

print("Отправка в группу...")
print(f"Chat ID: {os.environ.get('TELEGRAM_CHAT_ID')}")
result = TelegramService.send_notification(test_message)

if result:
    print("✅ Отправлено в группу!")
else:
    print("❌ Ошибка")
