from app.models.links import Link
from app.models.news import News
from app.models.instructions import Instruction
from app.models.types import TypeLinks, TypeNews
from app.models.calendar import Calendar
from app.models.phones import Phones


def all_models():
    ArModels = []
    # независимые таблицы
    ArModels.append(TypeLinks)
    ArModels.append(TypeNews)
    ArModels.append(Calendar)
    ArModels.append(Phones)

    # зависимые таблицы
    ArModels.append(Link)
    ArModels.append(News)
    ArModels.append(Instruction)

    return ArModels


def one_model(name):
    ArModels = all_models()
    for mod in ArModels:
        if name == mod.__name__:
            return mod
    return None
