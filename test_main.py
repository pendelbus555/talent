import pytest
from main import Task, TaskManager


@pytest.fixture
def setup_manager():
    """Создает экземпляр TaskManager с тестовыми данными."""
    manager = TaskManager("test_tasks.json")
    manager.tasks = []  # Очищаем задачи перед тестами
    return manager


def test_add_task(setup_manager):
    manager = setup_manager
    task = Task("Название", "Описание", "Работа", "2024-11-30", "средний")
    manager.add_task(task)
    assert len(manager.tasks) == 1
    assert manager.tasks[0]["title"] == "Название"


def test_invalid_date():
    with pytest.raises(ValueError, match="Неправильный формат даты"):
        Task("Название", "Описание", "Работа", "30-11-2024", "средний")


def test_delete_task(setup_manager):
    manager = setup_manager
    task = Task("Название", "Описание", "Работа", "2024-11-30", "средний")
    manager.add_task(task)
    manager.delete_task(task.id)
    assert len(manager.tasks) == 0


def test_edit_task(setup_manager):
    manager = setup_manager
    task = Task("Название", "Описание", "Работа", "2024-11-30", "средний")
    manager.add_task(task)
    manager.edit_task(1, title="Новое название")
    assert manager.tasks[0]["title"] == "Новое название"


def test_find_task(setup_manager):
    manager = setup_manager
    task = Task("Название", "Описание", "Работа", "2024-11-30", "средний")
    manager.add_task(task)
    results = manager.find_tasks("Название")
    assert len(results) == 1
    assert results[0]["title"] == "Название"
