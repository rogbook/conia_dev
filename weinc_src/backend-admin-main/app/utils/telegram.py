import telegram
from app.database.schema import SettingValue

async def telegram_send(body):
    try:
        token_data = SettingValue.get(type='telegram_alert_api_token')
        room_data = SettingValue.get(type='telegram_product_notify_room')

        bot = telegram.Bot(token=token_data.value)
        await bot.sendMessage(room_data.value, text=body)
    except:
        pass