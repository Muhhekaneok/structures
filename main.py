import time


class SmartTasker:
    def __init__(self):
        self.tasks = {}
        self.undo_stack = []
        self.counter = 1

    def add_task(self, title, priority, tags):
        task_id = self.counter
        self.tasks[task_id] = {
            "title": title,
            "priority": priority,
            "tags": tags,
            "time": time.strftime("%H:%M:%S")
        }
        self.undo_stack.append(task_id)
        self.counter += 1
        print(f"Task {title} added (ID: {task_id})")

    def print_tasks(self):
        if not self.tasks:
            print("There are no tasks to print")
            return
        print("---My tasks---")
        print(f"I have {len(self.tasks)} tasks:" if len(self.tasks) > 1 else "I have 1 task:")
        print(f"Tasks: {self.tasks}")


task_manager = SmartTasker()
task_manager.add_task("Coding", 1, ["algorithms", "frameworks"])
task_manager.add_task("German", 2, ["Grammatik", "Wörterbuch"])
task_manager.add_task("English", 1, ["grammar", "vocabulary"])
task_manager.print_tasks()