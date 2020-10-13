import sqlite3
from datetime import datetime

from task import Task


class TaskSQLite:
    date_format = "%Y-%m-%d %H:%M:%S"

    def __enter__(self):
        self.connector = sqlite3.connect('db.sqlite3')

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connector.close()

    def create_table(self):
        self.connector.execute('''
        CREATE TABLE IF NOT EXISTS ToDoList (
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        Title CHAR(50) NOT NULL,
        Description TEXT,
        DueDate TEXT,
        Completed INTEGER ,
        Important INTEGER       
        );''')

    def add(self, task: Task):
        self.connector.execute('''
        INSERT INTO ToDoList ('Title','Description','DueDate','Completed','Important')
        VALUES (:title,:description,:due_date,:completed,:important)
        ''', task.to_dict())
        self.connector.commit()

    def update(self, index, data):
        row = self.collect(index)
        if row:
            d = self.dict_factory(row)
            d.update(data)
            self.connector.execute('''
                        UPDATE ToDoList SET
                        Title = :title,
                        Description = :description,
                        DueDate = :due_date,
                        Completed = :completed,
                        Important = :important
                        WHERE Id = :id
                        ''', d)
            self.connector.commit()

    def delete(self, index):
        self.connector.execute('''
        DELETE FROM ToDoList WHERE Id = ?
        ''', (index,))
        self.connector.commit()

    def rollback(self):
        self.rollback()

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
        diff = datetime.now() - datetime.strptime(d['due_date'], TaskSQLite.date_format)
        if d['completed'] == 0:
            d['point'] = d['important'] + 2 if diff.seconds > 0 else 0
        return d

    def collect_all(self):
        cursor = self.connector.execute('SELECT * FROM ToDoList')
        results = []
        for row in cursor:
            d = self.dict_factory(row)
            results.append(Task.from_dict(d))
        return sorted(results, key=lambda r: r.point, reverse=True)

    def collect(self, index):
        cursor = self.connector.execute('SELECT * FROM ToDoList WHERE Id = ?', (index,))
        return cursor.fetchone()

    def collect_uncompleted(self):
        cursor = self.connector.execute('SELECT * FROM ToDoList WHERE Completed = 0')
        results = []
        for row in cursor:
            d = self.dict_factory(row)
            results.append(Task.from_dict(d))
        return sorted(results, key=lambda r: r.point, reverse=True)
