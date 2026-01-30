import json
import os
import time
from json import JSONDecodeError


class SmartTasker:
    def __init__(self):
        self.tasks = {}
        self.undo_stack = []
        self.counter = 1
        self.filepath = "tasks.json"

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
        print(f"I have {len(self.tasks)} tasks sorted by priority:" if len(self.tasks) > 1
              else "I have 1 task:")

        sorted_tasks = sorted(self.tasks.items(), key=lambda x: x[1]["priority"])
        for tid, data in sorted_tasks:
            print(f"ID {tid} | {data['title']} {data['priority']} | tags: {data['tags']}")
        print("-" * 25)

    def delete_task(self, task_id):
        removed_task = self.tasks.pop(task_id, None)
        if removed_task:
            print(f"Task '{removed_task['title']}' was removed")
        else:
            print(f"Task with ID {task_id} was not found")

    def save_to_file(self):
        clean_tasks = {}
        for tid, data in self.tasks.items():
            clean_tasks[tid] = data.copy()
            clean_tasks[tid]["tags"] = list(data["tags"])

        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(clean_tasks, f, indent=4)
        print("The data has been saved to tasks.json")

    def load_from_file(self):
        if not os.path.exists(self.filepath):
            print("The file doesn't exist")
            return
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                content = f.read()
                if not content:
                    print("File is empty")
                    return
                data = json.loads(content)
            self.tasks = {int(k): v for k, v in data.items()}
            self.counter = max(self.tasks.keys()) + 1

            print(f"File has been loaded. Loaded {len(self.tasks)} tasks")
        except JSONDecodeError:
            print("File is damaged.")


task_manager = SmartTasker()
# task_manager.add_task("Coding", 1, ["algorithms", "frameworks"])
# task_manager.add_task("German", 2, ["Grammatik", "Wörterbuch"])
# task_manager.add_task("English", 1, ["grammar", "vocabulary"])

# task_manager.print_tasks()

# task_manager.delete_task(3)
# task_manager.print_tasks()

# task_manager.save_to_file()

task_manager.load_from_file()