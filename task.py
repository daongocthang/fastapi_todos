class Task:
    def __init__(self, index, title, description, due_date, completed, important, point):
        self.id = index
        self.title = title
        self.description = description
        self.due_date = due_date
        self.completed = completed
        self.important = important
        self.point = point

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'due_date': self.due_date,
            'completed': self.completed,
            'important': self.important,
            'point': self.point
        }

    @staticmethod
    def from_dict(d):
        return Task(
            d['id'],
            d['title'],
            d['description'],
            d['due_date'],
            d['completed'],
            d['important'],
            d['point']
        )
