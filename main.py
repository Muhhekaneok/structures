import json
import os
import time
from json import JSONDecodeError

from category_node import CategoryNode
from cli import TaskCLI


class SmartTasker:
    def __init__(self, category_map=None):
        self.tasks = {}
        self.counter = 1
        self.filepath = "tasks.json"
        self.category_map = category_map or {}

    def add_task(self, title, priority, category_name):
        if category_name not in self.category_map:
            print(f"Category '{category_name}' does not exist!")
            return

        task_id = self.counter
        self.tasks[task_id] = {
            "title": title,
            "priority": priority,
            "category": category_name,
            "time": time.strftime("%H:%M:%S")
        }
        self.counter += 1
        print(f"Task '{title}' added (ID: {task_id})")

    def print_tasks(self):
        if not self.tasks:
            print("There are no tasks to print")
            return

        print("\n---My tasks---")
        sorted_tasks = sorted(self.tasks.items(), key=lambda x: x[1]["priority"])
        print(f"I have {len(self.tasks)} tasks sorted by priority:" if len(self.tasks) > 1
              else "I have 1 task:")
        id_width = max(len(str(tid)) for tid in self.tasks) + 3
        title_width = max(len(data["title"]) for _, data in sorted_tasks) + 3
        priority_width = len("priority") + 3
        category_width = max(len(data["category"]) for _, data in sorted_tasks) + 3
        print(
            f"{'ID':<{id_width}}"
            f"{'TITLE':<{title_width}}"
            f"{'PRIORITY':<{priority_width}}"
            f"{'CATEGORY':<{category_width}}"
        )
        print("-" * (id_width + title_width + priority_width + category_width))
        for tid, data in sorted_tasks:
            print(
                f"{tid:<{id_width}}"
                f"{data['title']:<{title_width}}"
                f"{data['priority']:<{priority_width}}"
                f"{data['category']:<{category_width}}"
            )
        print("-" * (id_width + title_width + priority_width + category_width))

    def delete_task(self, task_id):
        removed_task = self.tasks.pop(task_id, None)
        if removed_task:
            print(f"Task '{removed_task['title']}' was removed")
        else:
            print(f"Task with ID {task_id} was not found")

    def add_category(self, name, parent_name=None):
        if name in self.category_map:
            print(f"Category '{name}' already exists")
            return
        new_category = CategoryNode(name)
        self.category_map[name] = new_category
        if parent_name:
            parent = self.category_map.get(parent_name)
            if not parent:
                print(f"Parent category '{parent_name}' not found")
                return
            parent.children.append(new_category)
        print(f"Category '{name}' was successfully added")

    def print_categories(self):
        if not self.tasks:
            print("There are no categories to print")
            return
        sorted_categories = sorted(self.category_map.keys())
        print(f"There are {len(sorted_categories)} categories:")
        for category in sorted_categories:
            print("\t-", category)

    def save_to_file(self):
        clean_tasks = {}
        for tid, data in self.tasks.items():
            clean_tasks[tid] = data.copy()
            clean_tasks[tid]["category"] = data["category"]
        filename = input("Name the file: ")
        self.filepath = filename
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
                self.tasks[int(k)] = v

            self.counter = max(self.tasks.keys()) + 1 if self.tasks else 1

            print(f"File has been loaded. Loaded {len(self.tasks)} tasks")
        except JSONDecodeError:
            print("File is damaged.")

    def _find_by_category(self, category_name):
        if category_name not in self.category_map:
            print(f"Category '{category_name}' not found!")
            return

        category_node = self.category_map[category_name]
        valid_categories = category_node.get_all_names()

        print(f"Searching task(s) in categories {valid_categories}:")

        found = False
        for tid, task in self.tasks.items():
            if task["category"] in valid_categories:
                print(f"[ID {tid}] {task['title']} ({task['category']})")
                found = True
        if not found:
            print("No task found")

    def find_task_by_category(self):
        # while True:
        #     category = input("Enter a category. Or enter 'Q' for exiting: ").strip()
        #     if category.lower() == "q":
        #         break
        #     if category not in self.category_map:
        #         answer = input("Invalid category. Try again? (Y/N): ").strip().lower()
        #         if answer == "y":
        #             continue
        #         else:
        #             break
        #     self._find_by_category(category_name=category)
        category_name = input("Enter the category name: ")
        self._find_by_category(category_name=category_name)


if __name__ == "__main__":
    programming_languages = CategoryNode("Programming language")

    python = CategoryNode("Python")
    python_purpose = CategoryNode("Big Data")
    python_frameworks = CategoryNode("Python Framework")
    fast_api = CategoryNode("FastAPI")
    django = CategoryNode("Django")
    flask = CategoryNode("Flask")
    algo_python = CategoryNode("Merge sort")

    java = CategoryNode("Java")
    java_purpose = CategoryNode("Fintech")
    java_frameworks = CategoryNode("Java Framework")
    spring = CategoryNode("Spring")
    algo_java = CategoryNode("Quick sort")

    cpp = CategoryNode("C++")
    cpp_purpose = CategoryNode("Operation Systems")  # todo how to [Operation Systems, Games]?
    cpp_frameworks = CategoryNode("C++ Framework")
    opengl = CategoryNode("OpenGL")
    boost_asio = CategoryNode("Boost.Asio")
    unreal_engine = CategoryNode("Unreal Engine")
    algo_cpp = CategoryNode("Introsort")

    language_study = CategoryNode("Language")
    english = CategoryNode("English")
    german = CategoryNode("German")

    books = CategoryNode("Books")
    linux_book = CategoryNode("Linux book")
    python_book = CategoryNode("Python book")
    java_book = CategoryNode("Java book")
    cpp_book = CategoryNode("C++ book")
    sql_book = CategoryNode("SQL book")
    postman_book = CategoryNode("Postman source")
    docker_book = CategoryNode("Docker source")
    kubernetes_book = CategoryNode("Kubernetes source")

    programming_languages.add_child(python)
    python.add_child(python_purpose)
    python_purpose.add_child(python_frameworks)
    python_purpose.add_child(algo_python)
    python_frameworks.add_child(fast_api)
    python_frameworks.add_child(django)
    python_frameworks.add_child(flask)

    programming_languages.add_child(java)
    java.add_child(java_purpose)
    java_purpose.add_child(java_frameworks)
    java_purpose.add_child(algo_java)
    java_frameworks.add_child(spring)

    programming_languages.add_child(cpp)
    cpp.add_child(cpp_purpose)
    cpp_purpose.add_child(cpp_frameworks)
    cpp_purpose.add_child(algo_cpp)
    cpp_frameworks.add_child(opengl)
    cpp_frameworks.add_child(boost_asio)
    cpp_frameworks.add_child(unreal_engine)

    language_study.add_child(english)
    language_study.add_child(german)

    books.add_child(linux_book)
    books.add_child(python_book)
    books.add_child(java_book)
    books.add_child(cpp_book)
    books.add_child(sql_book)
    books.add_child(postman_book)
    books.add_child(docker_book)
    books.add_child(kubernetes_book)

    my_categories = {
        programming_languages.name: programming_languages,

        python.name: python,
        python_purpose.name: python_purpose,
        python_frameworks.name: python_frameworks,
        fast_api.name: fast_api,
        django.name: django,
        flask.name: flask,
        algo_python.name: algo_python,

        java.name: java,
        java_purpose.name: java_purpose,
        java_frameworks.name: java_frameworks,
        spring.name: spring,
        algo_java.name: algo_java,

        cpp.name: cpp,
        cpp_purpose.name: cpp_purpose,
        cpp_frameworks.name: cpp_frameworks,
        opengl.name: opengl,
        boost_asio.name: boost_asio,
        unreal_engine.name: unreal_engine,
        algo_cpp.name: algo_cpp,

        language_study.name: language_study,
        english.name: english,
        german.name: german,

        books.name: books,
        linux_book.name: linux_book,
        python_book.name: python_book,
        java_book.name: java_book,
        sql_book.name: sql_book,
        postman_book.name: postman_book,
        docker_book.name: docker_book,
        kubernetes_book.name: kubernetes_book
    }

    task_manager = SmartTasker(category_map=my_categories)

    if not task_manager.tasks:
        task_manager.add_task("Learning English", 2, "Language")
        task_manager.add_task("Deutsch lernen", 4, "Language")
        task_manager.add_task("Practice Dolinguo daily ", 2, "English")
        task_manager.add_task("Read 'Harry Potter' to the kids", 3, "English")
        task_manager.add_task("Deutsch für Kinder", 4, "German")
        task_manager.add_task("'How Linux Works' by Brian Ward", 1, "Linux book")
        task_manager.add_task("Find out in PyCharm IDE", 1, "Python")
        task_manager.add_task("Find out in Intellij IDEA IDE", 1, "Java")
        task_manager.add_task("Make project with FastAPI", 1, "Python Framework")
        task_manager.add_task("Read about Django", 2, "Python Framework")
        task_manager.add_task("Read about Flask", 2, "Python Framework")
        task_manager.add_task("Remember Java Spring", 3, "Java Framework")
        task_manager.add_task("Practice in merge sort via Python", 1, "Merge sort")
        task_manager.add_task("Make project with Postman", 1, "Postman source")
        task_manager.add_task("Find out how Docker works", 1, "Docker source")
        task_manager.add_task("Read about Kubernetes", 3, "Kubernetes source")
        task_manager.add_task("Programming: Principles and Practice Using C++", 3, "C++")

    app = TaskCLI(task_manager)
    app.run()
