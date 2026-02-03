class CategoryNode:
    def __init__(self, name):
        self.name = name
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)

    def get_all_names(self):
        names = [self.name]
        for child in self.children:
            names.extend(child.get_all_names())
        return names