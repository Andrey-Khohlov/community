import datetime
import enum
from typing import Annotated

from sqlalchemy import text, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase, mapped_column


# Создание базового класса для всех моделей
# Model = declarative_base()
intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', NOW())"))]
updated_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', NOW())"), onupdate=datetime.datetime.utcnow)]
str_256 = Annotated[str, mapped_column(String(256))]

class Model(DeclarativeBase):
    type_annotation_map = {
        "intpk": intpk,
        "created_at": created_at,
        "updated_at": updated_at,
        "str_256": str_256
    }

class RoastingLevel(enum.Enum):
    filter = "фильтр"
    spro = "эспрессо"
    milk = "под молоко"
    omni = "омни"

class BrewMethod(enum.Enum):
    espresso = "эспрессо"
    pourover = "пуровер"
    drip_coffee_maker = "капельная кофеварка"
    cezve = "джезва"
    french_press = "френч-пресс"
    mokka = "гейзерная кофеварка"
    immerse = "иммерсионная воронка"
    in_cup = "в чашке"
    aeropress = "аэропресс"
    capsules = "капсула"
    drip = "дрип-пакет"
    brew_bag = "брю-бэг"

class CoffeeProcessing(enum.Enum):
    washed = "мытая"
    natural = "натуральная"
    honey = "хани"
    aerobic = "аэробная"
    aerobic_washed = "аэробная мытая"
    aerobic_natural = "аэробная натуральная"
    aerobic_honey = "аэробная хани"
    anaerobic = "анаэробная"
    anaerobic_natural = "анаэробная натуральная"
    anaerobic_honey = "анаэробная хани"
    anaerobic_carbonic = "анаэробная углекислотная мацерация"
    anaerobic_lacto = "анаэробная лактоферментация"
    infuse = "инфьюз"
    gilling = "гиллинг - басах"
    wet_halling = "вэт - халл"
    half_dry = "полусухая"
    copi = "копи лювак"
    mixture = "смесь"

class Origin(enum.Enum):
    BR = "Бразилия"
    GT = "Гватемала"
    CO = "Колумбия"
    KE = "Кения"
    ZW = "Зимбабве"
    ET = "Эфиопия"
    PE = "Перу"
    IN = "Индия"
    VN = "Вьетнам"
    ID = "Индонезия"
    ID_ = "Индонезия Ява"
    CR = "Коста-Рика"
    MX = "Мексика"
    SV = "Сальвадор"
    HN = "Гондурас"
    NI = "Никарагуа"
    RW = "Руанда"
    CN = "Китай"