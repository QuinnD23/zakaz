from aiogram.dispatcher.filters.state import StatesGroup, State


class StateMachine(StatesGroup):
    Admin = State()

    Add = State()
    Delete = State()

    NotifyChoice = State()

    NotifyTextWeek = State()
    NotifyDateWeek = State()
    NotifyTimeWeek = State()

    NotifyText = State()
    NotifyDate = State()
    NotifyTime = State()
    NotifyMembers = State()

    EditChoice = State()
    EditMain = State()
    Text = State()
    Date = State()
    Time = State()
