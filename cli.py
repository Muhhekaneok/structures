import json


def get_list():
    print("""
1. Add tasks
2. Show tasks
3. Delete task
4. Save data to JSON file
5. Show JSON file
6. Load data from file
7. Delete JSON file
8. Find task by category
9. Add category
10. Show categories
11. Delete category
0. Exit
    """)


class TaskCLI:
    def __init__(self, task_manager):
        self.task_manager = task_manager

    def run(self):
        while True:
            print("==== Smart Tasker =====")
            choice = input("Choose option: ").strip()
            if choice == "help":
                get_list()
            elif choice == "1":
                self.add_task_ui()
            elif choice == "2":
                self.task_manager.print_tasks()
            elif choice == "3":
                self.delete_task_ui()
            elif choice == "4":
                self.task_manager.save_to_file()
            elif choice == "5":
                self.show_json()
            elif choice == "6":
                self.task_manager.load_from_file()
            elif choice == "7":
                self.delete_json_file_ui()
            elif choice == "8":
                self.task_manager.find_task_by_category()
            elif choice == "9":
                self.add_category_ui()
            elif choice == "10":
                self.task_manager.print_categories()
            elif choice == "11":
                self.delete_category_ui()
            elif choice == "0":
                print("Exiting...")
                break
            else:
                print("Invalid option")

    def add_task_ui(self):
        title = input("Enter title: ")
        priority = int(input("Enter priority: "))
        category = input("Enter category: ")
        self.task_manager.add_task(title, priority, category)

    def delete_task_ui(self):
        try:
            task_id = int(input("Enter task id to delete the task: "))
            self.task_manager.delete_task(task_id)
        except ValueError:
            print("Invalid task")

    def show_json(self):
        categories_serialized = {
            name: node.to_dict()
            for name, node in self.task_manager.category_map.items()
        }
        print(json.dumps(categories_serialized, ensure_ascii=False, indent=4))
        print(json.dumps(self.task_manager.tasks, ensure_ascii=False, indent=4))

    def add_category_ui(self):
        category = input("Enter category: ")
        parent = input("Enter parent category (or leave empty): ").strip()
        parent = parent if parent else None
        self.task_manager.add_category(category, parent)

    def delete_category_ui(self):
        category = input("Enter category: ")
        self.task_manager.delete_category(category)

    def delete_json_file_ui(self):
        json_file = input("Enter json file to delete: ")
        self.task_manager.delete_json_file(json_file)