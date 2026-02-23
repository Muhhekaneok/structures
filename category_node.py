class CategoryNode:
    def __init__(self, name):
        self.name = name
        self.children = []
        self.parent = None

    def add_child(self, child_node):
        child_node.parent = self
        self.children.append(child_node)

    def get_all_names(self):
        names = [self.name]
        for child in self.children:
            names.extend(child.get_all_names())
        return names

    def to_dict(self):
        return {
            "name": self.name,
            "parent": self.parent.name if self.parent else None,
            "children": [child.name for child in self.children]
        }