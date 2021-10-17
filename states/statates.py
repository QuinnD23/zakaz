from aiogram.dispatcher.filters.state import StatesGroup, State


class StateMachine(StatesGroup):
    StartName = State()
    StartNumber = State()
    StartAuto = State()
    StartVin = State()
    StartPlace = State()
    Start = State()

    AutoChoice = State()
    AddAuto = State()
    AddVin = State()

    PhotoTre = State()
    PhotoMar = State()

    DimeTre = State()
    SrokTre = State()

    PlaceChoice = State()
    AddPlace = State()

    Bonus = State()

    Admin = State()
