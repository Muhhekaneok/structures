import json
import os
import time
from json import JSONDecodeError

from category_node import CategoryNode


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
            "tags": set(tags),
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
            json.dump(clean_tasks, f, ensure_ascii=False, indent=4)
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
            for k, v in data.items():
                v["tags"] = set(v["tags"])
                self.tasks[int(k)] = v

            self.counter = max(self.tasks.keys()) + 1 if self.tasks else 1

            print(f"File has been loaded. Loaded {len(self.tasks)} tasks")
        except JSONDecodeError:
            print("File is damaged.")

    def find_by_tag(self, tag, category_map=None):
        print(f"Fetching tasks with tag '{tag}':")
        if category_map and tag in category_map:
            fetching_tags = set(category_map[tag].get_all_names())
        else:
            fetching_tags = {tag}
        print(f"Looking for matches with '{', '.join(fetching_tags)}'")
        found = False
        for tid, task in self.tasks.items():
            if not task["tags"].isdisjoint(fetching_tags):
                print(f" - ID: {tid} | {task['title']}")
                found = True
        if not found:
            print(f"No tasks with tag '{tag}' found")


if __name__ == "__main__":
    task_manager = SmartTasker()

    python_work = CategoryNode("Work and practice in Python")
    programming_python = CategoryNode("Coding in Python")
    python = CategoryNode("Python language")
    algo_python = CategoryNode("Algorithms in Python")

    java_work = CategoryNode("Practice and work in Java")
    programming_java = CategoryNode("Coding in Java")
    java = CategoryNode("Java language")
    algo_java = CategoryNode("Algorithms in Java")

    python_work.add_child(programming_python)
    programming_python.add_child(python)
    programming_python.add_child(algo_python)

    java_work.add_child(programming_java)
    programming_java.add_child(java)
    programming_java.add_child(algo_java)

    category_map = {
        "Work in Python": python_work,
        "Coding in Python": programming_python,
        "Python": python,
        "Algorithms in Python": algo_python,

        "Work in Java": java_work,
        "Coding in Java": programming_java,
        "Java": java,
        "Algorithms in Java": algo_java
    }

    if not task_manager.tasks:
        task_manager.add_task("Coding", 1, ["Algorithms", "Frameworks"])
        task_manager.add_task("Deutsche", 2, ["Grammatik", "Wörterbuch"])
        task_manager.add_task("English", 1, ["Grammar", "Vocabulary"])
        task_manager.add_task("アンジェラ・アキ", 3, ["どこか懐かしい", "しました"])
        task_manager.save_to_file()

    task_manager.print_tasks()
    # task_manager.find_by_tag("Algorithms", category_map)
    task_manager.find_by_tag("Work in Python", category_map)