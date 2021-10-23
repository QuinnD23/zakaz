from aiogram.dispatcher.filters.state import StatesGroup, State


class StateMachine(StatesGroup):
    StartName = State()
    StartNumber = State()
    StartAuto = State()
    StartVin = State()
    StartYear = State()
    StartPlace = State()
    Start = State()

    AutoChoice = State()
    AddAuto = State()
    AddVin = State()
    AddYear = State()

    PhotoTre = State()
    PhotoMar = State()

    DimeTre = State()
    SrokTre = State()

    PlaceChoice = State()
    AddPlace = State()

    Bonus = State()

    Admin = State()
    Answer = State()
    AnswerText = State()
    AcceptText = State()
