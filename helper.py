import sqlite3
from datetime import datetime

from task import Task


class TaskHelper:

    def __enter__(self):
        self.connector = sqlite3.connect('db.sqlite3')
        print('Opened database successfully')

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connector.close()

    def create_if_not_exists(self):
        self.connector.execute('''
        CREATE TABLE IF NOT EXISTS ToDoList (
        Id INT PRIMARY KEY AUTOINCREMENT,
        Title CHAR(50) NOT NULL,
        Description TEXT,
        DueDate DATE,
        Completed INT,
        Important INT       
        );''')
        print('Table `ToDoList` created successfully')

    def insert_or_update(self, task: Task):
        if self.exist(task.id):
            self.connector.execute('''
            UPDATE ToDoList SET
            Title = :title,
            Description = :description,
            DueDate = :due_date,
            Completed = :completed,
            Important = :important
            WHERE Id = :id
            ''', task.to_dict())
        else:
            self.connector.execute('''
            INSERT INTO ToDoList ('Title','Description','DueDate','Completed','Important')
            VALUES (:title,:description,:due_date,:completed,:important)
            ''', task.to_dict())
        self.connector.commit()

    def remove(self, index):
        self.connector.execute('''
        DELETE FROM ToDoList WHERE Id = ?
        ''', (index,))
        self.connector.commit()

    def exist(self, index):
        return self.connector.execute('SELECT COUNT(*) FROM ToDoList WHERE Id=?', (index,)) > 0

    @staticmethod
    def dict_factory(row):
        d = {
            'id': row[0],
            'title': row[1],
            'description': row[2],
            'due_date': row[3],
            'completed': row[4],
            'important': row[5],
            'point': 0
        }
        diff = datetime.now() - d['due_date']
        if d['completed'] == 0:
            d['point'] = d['important'] + 2 if diff.days > 0 else 0
        return d

    def list_todo(self):
        cursor = self.connector.execute('SELECT * FROM ToDoList WHERE Completed = 0')
        results = []
        for row in cursor:
            d = self.dict_factory(row)
            results.append(TaskHelper.from_dict(d))
        return sorted(results, key=lambda r: r['point'], reverse=True)
