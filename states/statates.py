from aiogram.dispatcher.filters.state import StatesGroup, State


class StateMachine(StatesGroup):
    Admin = State()

    Add = State()
    Delete = State()

    NotifyText = State()
    NotifyDate = State()
    NotifyTime = State()

    EditChoice = State()
    EditMain = State()
    Text = State()
    Date = State()
    Time = State()