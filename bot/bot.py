import httpx
from aiogram.filters import CommandStart
from aiogram.types import Message
from config import config
from bot.bot_instance import dp, bot



async def check_imei(imei: str):
    headers = {
        'Authorization': f'Bearer {config.API_TOKEN}',
        'Content-Type': 'application/json',
    }

    # Данные для запроса
    data = {
        'deviceId': imei,  
        'serviceId': config.SERVICE_ID,
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(config.URL_CHECK, json=data, headers=headers)
            response.raise_for_status()

            print(response.json())

            return response.json()
    except httpx.HTTPStatusError as e:
        print(f"HTTP Error: {e.response.status_code} - {e.response.text}")
        return {"error": f"HTTP Error: {e.response.status_code} - {e.response.text}"}
    except httpx.RequestError as e:
        print(f"Request Error: {str(e)}")
        return {"error": f"Request Error: {str(e)}"}
    except Exception as e:
        print(f"Unexpected Error: {str(e)}")
        return {"error": f"Unexpected Error: {str(e)}"}


@dp.message(CommandStart())
async def start(message: Message):
    user_id = str(message.from_user.id)
    if message.from_user.id not in config.WHITE_LIST:
        return await message.answer(f"У вас нет доступа к боту, {user_id}")
    await message.answer("Отправьте IMEI для проверки.")


@dp.message()
async def handle_imei(message: Message):
    if message.from_user.id not in config.WHITE_LIST:
        return await message.answer("У вас нет доступа к боту.")
    
    imei = message.text.strip()
    
    if not imei.isdigit() or len(imei) not in {14, 15}:
        return await message.answer("Некорректный IMEI. Попробуйте снова:")
    
    await message.answer("Проверяю IMEI...")

    response = await check_imei(imei)
    
    if response.get("status") == "successful":
        properties = response.get('properties', {})
        
        device_name = properties.get('deviceName', 'Неизвестное устройство')
        imei = properties.get('imei', 'Неизвестен')
        model_desc = properties.get('modelDesc', 'Неизвестная модель')
        purchase_country = properties.get('purchaseCountry', 'Неизвестная страна')
        sim_lock = "Да" if properties.get('simLock') else "Нет"
        fmi_on = "Да" if properties.get('fmiOn') else "Нет"
        lost_mode = "Да" if properties.get('lostMode') else "Нет"
        image_url = properties.get('image', '')
        
        result_text = f"""
        Результат проверки: {imei}
        Модель: {device_name}
        IMEI: {imei}
        Описание модели: {model_desc}
        Страна: {purchase_country}
        SIM Lock: {sim_lock}
        Find My iPhone: {fmi_on}
        Режим потерянного устройства: {lost_mode}
        
Изображение устройства({image_url})
        """
    else:
        result_text = f"Не удалось проверить IMEI. Причина: {response.get('error', 'Неизвестная ошибка')}"

    await message.answer(result_text)

