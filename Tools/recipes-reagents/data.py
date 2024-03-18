import yaml
import os

from pathlib import Path
from any_yaml import Loader

from project_dirs import *
from rw_func import *

if __name__ == "__main__":
    print("[ERR] Run the RUN.py")
    exit()
else:
    print("[INFO] Loading data:")

effects = {
    "SatiateThirst": {
        # TODO: fill the missing properties

        # How much thirst is satiated each metabolism tick.
        # Not currently tied to rate or anything
        "factor": 3.0,
        "NAMES": {
            "MAIN": "Утоление жажды",
            "factor": "Значение"
        }
    },

    "SatiateHunger": {
        # How much hunger is satiated when 1u of the reagent is metabolized
        "factor": 3.0,
        "NAMES": {
            "MAIN": "Утоление голода",
            "factor": "Значение"
        }
    },

    "MovespeedModifier": {
        # How much the entities' walk speed is multiplied by
        "walkSpeedModifier": 1,
        # How much the entities' run speed is multiplied by
        "sprintSpeedModifier": 1,
        # How long the modifier applies (in seconds) when metabolized
        "statusLifetime": 2.0,
        "NAMES": {
            "MAIN": "Изменение скорости",
            "walkSpeedModifier": "Модификатор ходьбы",
            "sprintSpeedModifier": "Модификатор бега",
            "statusLifetime": "Длительность эффекта"
        }
    },

    "ResetNarcolepsy": {
        # The # of seconds the effect resets the narcolepsy timer to
        "TimerReset": 600,
        "NAMES": {
            "MAIN": "Ослабление нарколепсии",
            "TimerReset": "Время (сек.)"
        }
    },

    "Polymorph": {
        # What polymorph prototype is used on effect
        "prototype": None,
        "NAMES": {
            "MAIN": "Полиморфизм",
            "prototype": "Прототип"
        }
    },

    "Paralyze": {
        # --
        "paralyzeTime": 2,
        # true - refresh paralyze time,  false - accumulate paralyze time
        "refresh": True,
        "NAMES": {
            "MAIN": "Парализация",
            "paralyzeTime": "Время (сек.)",
            "refresh": "Сброс времени"
        }
    },

    "ModifyBloodLevel": {
        # --
        "scaled": False,
        # --
        "amount": 1.0,
        "NAMES": {
            "MAIN": "Изменение уровня крови в организме",
            "scaled": "Увеличиваемый",
            "amount": "Количество"
        }
    },

    "ModifyBleedAmount": {
        # --
        "scaled": False,
        # --
        "amount": -1.0,
        "NAMES": {
            "MAIN": "Изменение кровотечения",
            "scaled": "Увеличиваемый",
            "amount": "Количество"
        }
    },

    "MakeSentient": {
        "NAMES": {
            "MAIN": "Наделение разумом"
        }
    },

    "HealthChange": {
        # Damage to apply every metabolism cycle. Damage Ignores resistances
        "damage": None,
        # Should this effect scale the damage by the amount of chemical in the solution?
        # Useful for touch reactions, like styptic powder or acid.
        "scaleByQuantity": None,
        # --
        "ignoreResistances": True,
        "NAMES": {
            "MAIN": "Изменение здоровья",
            "damage": "Урон",
            "scaleByQuantity": "Зависимость от количества",
            "ignoreResistances": "Игнорируется ли защита"
        }
    },

    "FlammableReaction": {
        # --
        "multiplier": 0.05,
        "NAMES": {
            "MAIN": "Воспламенение реагента",
            "multiplier": "Множитель"
        }
    },

    "ActivateArtifact": {
        "NAMES": {
            "MAIN": "Активация артефакта"
        }
    },

    "Drunk": {
        # BoozePower is how long each metabolism cycle will make the drunk effect last for
        "boozePower": 3.0,
        # Whether speech should be slurred
        "slurSpeech": True,
        "NAMES": {
            "MAIN": "Опьянение",
            "boozePower": "Длительность (сек.) на каждый цикл метаболизма",
            "slurSpeech": "Изменяет речь"
        }
    },

    "CauseZombieInfection": {
        "NAMES": {
            "MAIN": "Заражение зомби-вирусом"
        }
    },

    "CureZombieInfection": {
        # --
        "innoculate": None,
        "NAMES": {
            "MAIN": "Исцеление от зомби-вируса",
            "innoculate": "Прививаемый"
        }
    },

    "Electrocute": {
        # --
        "electrocuteTime": 2,
        # --
        "electrocuteDamageScale": 5,
        # true - refresh electrocute time,  false - accumulate electrocute time
        "refresh": True,
        "NAMES": {
            "MAIN": "Элекрический шок",
            "electrocuteTime": "Длительность (сек.)",
            "electrocuteDamageScale": "Множитель урона",
            "refresh": "Сброс времени"

        }

    },

    "CreateGas": {
        # --
        "gas": None,
        # For each unit consumed, how many moles of gas should be created?
        "multiplier": 3.0,
        "NAMES": {
            "MAIN": "Создание газа",
            "gas": "Газ",
            "multiplier": "Количество (моль) на еденицу вещества"
        }
    },

    "ChemVomit": {
        # How many units of thirst to add each time we vomit
        "thirstAmount": -40.0,
        # How many units of hunger to add each time we vomit
        "hungerAmount": -40.0,
        "NAMES": {
            "MAIN": "Рвота",
            "thirstAmount": "Количество добавляемых едениц утоления жажды",
            "hungerAmount": "Количество добавляемых едениц насыщения"
        }
    },

    "AdjustReagent": {
        # The reagent ID to remove
        "reagent": None,
        # The metabolism group to remove, if the reagent satisfies any
        "group": None,
        # --
        "amount": None,
        "NAMES": {
            "MAIN": "Изменение реагентов",
            "reagent": "Реагент",
            "group": "Группа метаболизма",
            "amount": "Количество"
        }
    },

    "AdjustTemperature": {
        # --
        "amount": None,
        "NAMES": {
            "MAIN": "Изменение температуры",
            "amount": "Количество"
        }
    },

    "Emote": {
        # --
        "emote": None,
        # --
        "showInChat": None,
        "NAMES": {
            "MAIN": "Эмоция",
            "emote": "Эмоция",
            "showInChat": "Показывать в чате"
        }
    },

    "Ignite": {
        "NAMES": {
            "MAIN": "Поджог"
        }
    },

    "ExtinguishReaction": {
        "NAMES": {
            "MAIN": "Тушение"
        }
    },

    "ChemHealEyeDamage": {
        # How much eye damage to add
        "amount": -1,
        "NAMES": {
            "MAIN": "Исцеление глаз",
            "amount": "Количество добавляемого урона"
        }
    },

    "WashCreamPieReaction": {
        "NAMES": {
            "MAIN": "Смытие пирога с лица"
        }
    },

    "PopupMessage": {
        # --
        "messages": None,
        # --
        "type": "PopupRecipients.Local",
        # --
        "visualType": "PopupType.Small",
        "NAMES": {
            "MAIN": "Всплывающее сообщение",
            "messages": "Сообщение",
            "type": "Тип",
            "visualType": "Тип отображения"
        }
    },

    "ChemCleanBloodstream": {
        #Quantity of reagent units that will be deleted in one metabolism tick.
        "cleanseRate": -3,
        "NAMES": {
            "MAIN": "Очищение кровотока",
            "cleanseRate": "Количество единиц"
        }
    },

    "GenericStatusEffect": {
        # basically just adds a component to an entity for a given time.
        "key": None,
        "component": None,
        "time": 2,
        # true - refresh status effect time,  false - accumulate status effect time
        "refresh": True,
        "type": None,
        "NAMES": {
            "MAIN": "Изменение эффектов",
            "key": "Эффект",
            "component": "Компонент",
            "time": "Длительность (сек.)",
            "refresh": "Возобновляемость",
            "type": "Тип"
        }
    },

    "Oxygenate": {
        # Literally makes gas breathable.
        "factor": 1,
        "NAMES": {
            "MAIN": "Поглощение газа",
            "factor": "Коэфицент"
        }
    },

    "ModifyLungGas": {
        # Used to breathe out gas. 
        "ratios": None,
        "NAMES": {
            "MAIN": "Выделение газа",
            "ratios": "Соотношение"
        }
    },

    "Jitter": {
        # Shakes the character.
        "amplitude": 10,
        "frequency": 4,
        "time": 2,
        "refresh": True,
        "NAMES": {
            "MAIN": "Тряска",
            "amplitude": "Амплитуда",
            "frequency": "Частота",
            "time": "Длительность",
            "refresh": "Возобновляемость"
        }
    },

    "AdjustAlert": {
        # Causes an icon to the right of the screen.
        "alertType": None,
        "clear": None,
        "cooldown": None,
        "time": None,
        "NAMES": {
            "MAIN": "Предупреждение",
            "alertType": "Тип предупреждения",
            "clear": "Очищает",
            "cooldown": "Кулдаун",
            "time": "Время (сек.)"
        }
    },

    "Embalm": {
        #Makes entity unable to rot but also cannot be revived by defibrillator.
        "NAMES": {
            "MAIN": "Бальзамирование"
        }
    },

    "LingEggs": {
        #Quote: "Gives the entity a component that turns it into a f#cking changeling"
        "NAMES": {
            # Я честно без понятия, как это описать иначе.
            "MAIN": "Откладывает личинки генокрада"
        }
    },

    "RobustHarvest": {
        "PotencyLimit": 50,
        "PotencyIncrease": 3,
        "PotencySeedlessThreshold": 30,
        "NAMES": {
            "MAIN": "Повышение потенции растения",
            "PotencyLimit": "Лимит потенции",
            "PotencyIncrease": "Повышение потенции",
            # Seedless.
            "PotencySeedlessThreshold": "Лимит потенции до обессеменивания растения", 
        }
    },

    "PlantPhalanximine": {
        # Makes plant holders genetics viable. I guess.        
        "NAMES": {
            "MAIN": ""
        }
    },

    "PlantDiethylamine": {
        #Don't really know why is it another .cs file.
        #Basically, it just increases lifespan of a plant and it's endurance with some chance.
        "NAMES": {
            "MAIN": "Увеличение долговечности растения"
        }
    },

    "PlantCryoxadone": {
        #Deviates stages of a plant.
        "NAMES": {
            "MAIN": "Отмена стадии роста растения"
        }
    },

    "PlantAffectGrowth": {
        #Honestly I can't understand what's this, needs testing in game.
        "NAMES": {
            "MAIN": "Влияние на рост растения"
        }
    },

    "PlantAdjustWeeds": {
        "Amount": 1,
        "Prob": 1, # " = (80)" - was written in a "PlantAdjustAttribute". Idk.
        "NAMES": {
            "MAIN": "Изменение количества сорняков в растении",
            "Amount": "Количество",
            "Prob": "Шанс"
        }
    },

    "PlantAdjustWater": {
        "Amount": 1,
        "Prob": 1,        
        "NAMES": {
            "MAIN": "Изменение количества воды в растении",
            "Amount": "Количество",
            "Prob": "Шанс"            
        }
    },

    "PlantAdjustToxins": {
        "Amount": 1,
        "Prob": 1,        
        "NAMES": {
            "MAIN": "Изменение количества токсинов в растении",
            "Amount": "Количество",
            "Prob": "Шанс"            
        }
    },

    "PlantAdjustPests": {
        "Amount": 1,
        "Prob": 1,        
        "NAMES": {
            "MAIN": "Изменение количества пестицидов в растении",
            "Amount": "Количество",
            "Prob": "Шанс"
        }
    },

    "PlantAdjustNutrition": {
        "Amount": 1,
        "Prob": 1,        
        "NAMES": {
            "MAIN": "Изменение насыщения растения", #?
            "Amount": "Количество",
            "Prob": "Шанс"
        }
    },

    "PlantAdjustMutationMod": {
        "Amount": 1,
        "Prob": 1,        
        "NAMES": {
            "MAIN": "Изменение модификатора мутации растения",  #?
            "Amount": "Количество",
            "Prob": "Шанс"
        }
    },
    
    "PlantAdjustMutationLevel": {
        "Amount": 1,
        "Prob": 1,        
        "NAMES": {
            "MAIN": "Изменение уровня мутации растения",
            "Amount": "Количество",
            "Prob": "Шанс" 
        }
    },
        
    "PlantAdjustHealth": {
        "Amount": 1,
        "Prob": 1,        
        "NAMES": {
            "MAIN": "Изменение уровня здоровья растения",
            "Amount": "Количество",
            "Prob": "Шанс"
        }
    },

    #"PlantAdjustAttribute" is a parent to any "PlantAdjust...", that does all the checks needed for plants.
}

# takes "dict_generator" as string with itareble "data"
def get_data(path: str | os.PathLike, dict_generator: str) -> dict:
    print(f"[INFO] - {path.name}")
    dct = {}
    files = sorted(Path(path).glob("**/*.yml"))

    for file in files:
        check_and_reencode_utf_sig(file)

        with open(file) as file:
            data = yaml.load(file, Loader=Loader)

        for i in range(len(data)):
            dct.update(eval(dict_generator))

    return dct


reag_dict_gen = '{reagent["id"]: {key: value for key, value in reagent.items() if key != "id"} for reagent in data}'
reagents = get_data(REAG_DIR, reag_dict_gen)
# transform to string, replace brackets and "!type" and convert back to dict
reagents = eval(str(reagents).replace('[', "{").replace(']', "}").replace('!type:', ""))

reag_groups = {reagent["group"] for reagent in reagents.values() if "group" in reagent}
reag_groups.add("reagent")

recp_dict_gen = '{recipes["id"]: {key: value["amount"] for key, value in recipes["reactants"].items()} for recipes in data if "reactants" in recipes}'
recipes = get_data(RECP_DIR, recp_dict_gen)


print("[INFO] Finished")
