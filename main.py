import json
from datetime import datetime


class Task:
    """Класс для представления задачи."""

    def __init__(self, title, description, category, due_date, priority, status="Не выполнена"):
        if not title.strip():
            raise ValueError("Название задачи не может быть пустым.")
        if not description.strip():
            raise ValueError("Описание задачи не может быть пустым.")
        if not category.strip():
            raise ValueError("Категория задачи не может быть пустой.")
        try:
            self.due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Неправильный формат даты. Используйте YYYY-MM-DD.")
        if priority not in ["низкий", "средний", "высокий"]:
            raise ValueError("Приоритет задачи должен быть: низкий, средний или высокий.")

        self.title = title
        self.description = description
        self.category = category
        self.priority = priority
        self.status = status
        self.id = None

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "due_date": self.due_date.strftime("%Y-%m-%d"),
            "priority": self.priority,
            "status": self.status,
        }


class TaskManager:
    """Класс для управления задачами."""

    def __init__(self, file_name="tasks.json"):
        self.file_name = file_name
        self.tasks = self.load_tasks()

    def load_tasks(self):
        try:
            with open(self.file_name, "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_tasks(self):
        with open(self.file_name, "w", encoding="utf-8") as file:
            json.dump(self.tasks, file, ensure_ascii=False, indent=4)

    def add_task(self, task):
        if not isinstance(task, Task):
            raise TypeError("Задача должна быть объектом класса Task.")
        task.id = len(self.tasks) + 1
        self.tasks.append(task.to_dict())
        self.save_tasks()

    def delete_task(self, task_id):
        try:
            task_id = int(task_id)
        except ValueError:
            raise ValueError("ID задачи должен быть числом.")
        self.tasks = [task for task in self.tasks if task["id"] != task_id]
        self.save_tasks()

    def edit_task(self, task_id, **updates):
        for task in self.tasks:
            if task["id"] == task_id:
                for key, value in updates.items():
                    if key in task and value:
                        task[key] = value
                self.save_tasks()
                return
        raise ValueError("Задача с указанным ID не найдена.")

    def find_tasks(self, keyword):
        return [task for task in self.tasks if keyword.lower() in task["title"].lower()]

    def list_tasks(self, category=None):
        if category:
            return [task for task in self.tasks if task["category"] == category]
        return self.tasks


def main():
    manager = TaskManager()

    while True:
        print("\nМеню:")
        print("1. Просмотр задач")
        print("2. Добавление задачи")
        print("3. Редактирование задачи")
        print("4. Удаление задачи")
        print("5. Поиск задачи")
        print("6. Выход")

        choice = input("Выберите действие: ")

        match choice:
            case "1":
                category = input("Введите категорию (или нажмите Enter для всех задач): ")
                tasks = manager.list_tasks(category if category.strip() else None)
                if tasks:
                    for task in tasks:
                        print(task)
                else:
                    print("Задачи не найдены.")

            case "2":
                try:
                    title = input("Введите название задачи: ")
                    description = input("Введите описание задачи: ")
                    category = input("Введите категорию задачи: ")
                    due_date = input("Введите срок выполнения (YYYY-MM-DD): ")
                    priority = input("Введите приоритет (низкий, средний, высокий): ")
                    task = Task(title, description, category, due_date, priority)
                    manager.add_task(task)
                    print("Задача добавлена.")
                except ValueError as e:
                    print(f"Ошибка: {e}")

            case "3":
                try:
                    task_id = int(input("Введите ID задачи для редактирования: "))
                    updates = {
                        "title": input("Новое название (или Enter для пропуска): "),
                        "description": input("Новое описание (или Enter для пропуска): "),
                        "category": input("Новая категория (или Enter для пропуска): "),
                        "due_date": input("Новая дата (YYYY-MM-DD, или Enter для пропуска): "),
                        "priority": input("Новый приоритет (низкий, средний, высокий): "),
                        "status": input("Новый статус (Выполнена/Не выполнена): "),
                    }
                    manager.edit_task(task_id, **{k: v for k, v in updates.items() if v.strip()})
                    print("Задача обновлена.")
                except ValueError as e:
                    print(f"Ошибка: {e}")

            case "4":
                try:
                    task_id = input("Введите ID задачи для удаления: ")
                    manager.delete_task(task_id)
                    print("Задача удалена.")
                except ValueError as e:
                    print(f"Ошибка: {e}")

            case "5":
                keyword = input("Введите ключевое слово для поиска: ")
                results = manager.find_tasks(keyword)
                if results:
                    for task in results:
                        print(task)
                else:
                    print("Задачи не найдены.")

            case "6":
                print("Выход из программы.")
                break

            case _:
                print("Некорректный выбор, попробуйте снова.")


if __name__ == "__main__":
    main()
