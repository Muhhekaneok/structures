import json


class TaskCLI:
    def __init__(self, task_manager):
        self.task_manager = task_manager

    def run(self):
        while True:
            print("==== Smart Tasker =====")
            print("""
1. Add tasks
2. Show tasks
3. Delete task
4. Show JSON
5. Find task by category
6. Save tasks to file
7. Load tasks from file
0. Exit
            """)

            choice = input("Choose option: ").strip()
            if choice == "1":
                self.add_task_ui()
            elif choice == "2":
                self.task_manager.print_tasks()
            elif choice == "3":
                self.delete_task_ui()
            elif choice == "4":
                self.show_json()
            elif choice == "5":
                self.task_manager.find_task_by_category()
            elif choice == "6":
                self.task_manager.save_to_file()
            elif choice == "7":
                self.task_manager.load_from_file()
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
        print(json.dumps(self.task_manager.tasks, ensure_ascii=False, indent=4))