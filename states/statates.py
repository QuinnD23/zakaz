from aiogram.dispatcher.filters.state import StatesGroup, State


class StateMachine(StatesGroup):

    # 1 Главный Администратор -----------------------------------
    # Главное меню
    MainAdmin = State()

    # Выбор Команды [Администраторы] : EditAdmins
    EditAdminsCommands = State()
    # Ожидание Ника Администратора
    AddAdmins = State()
    # Ожидание Delete Номера Администратора
    DeleteAdmins = State()

    # Выбор Команды [Сотрудники] : EditWorkersMenu
    EditWorkersCommands = State()
    # Ожидание Ника Сотрудника
    AddWorkers = State()
    # Ожидание Номеров Услуг Сотрудника
    AddWorkersServices = State()
    # Ожидание Delete Номера Сотрудника
    DeleteWorkers = State()
    # Ожидание Delete Номера Сотрудника для Услуг
    WaitWorkerForEditServices = State()
    # Ожидание Delete Номера Сотрудника для Редактирования : EditWorkersServicesMenu
    EditWorkersServicesCommands = State()
    # Ожидание Delete Номера Улсуги Добавление
    EditWorkersServicesAdd = State()
    # Ожидание Delete Номера Улсуги Удаление
    EditWorkersServicesDelete = State()

    # Выбор Команды [Услуги] : EditServicesMenu
    EditServicesCommands = State()
    # Ожидание Названия Усулги
    AddServices = State()
    # Ожидание Delete Номера Услуги
    DeleteServices = State()

    # Выбор Команды [Интерфейс] : EditFaceMenu
    EditFaceCommands = State()
    # Ожидание нового текста Приветствия
    EditHelloText = State()
    # Ожидание нового текста Времени Работы
    EditWorkTimeText = State()
    # Ожидание нового текста Завершения
    EditEndText = State()
    # Выбор Команды [Контакты] : EditContactsMenu
    EditContactsCommands = State()
    # Ожидание Названия Контакта
    AddContacts = State()
    # Ожидание Delete Номера Контакта
    DeleteContacts = State()

    # 1 End -----------------------------------------------------

    # 2 Обычный Администратор -----------------------------------
    # Главное меню
    Admin = State()

    # 2 End -----------------------------------------------------

    # 3 Пользователь --------------------------------------------
    # Главное меню
    User = State()

    # Ввод Контактов
    EnterContacts = State()

    # Выбор Команды [Контакты Пользователя] : EditUsersContacts
    EditUsersContactsCommands = State()
    # Ожидание Delete Номера Контакта Пользователя
    DelNumContactWait = State()
    # Ожидание нового Контакта
    NewContactWait = State()

    # Ожидание Услуги
    ServiceInOrder = State()
    # Ожидание Даты
    DateInOrder = State()
    # Ожидание Времени
    TimeInOrder = State()
    # Ожидание Мастера
    WorkerInOrder = State()

    # 3 End -----------------------------------------------------
