import argparse
import sqlite3
import sys
from datetime import datetime

import utils
from helper import TaskSQLite
from task import Task

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', dest='attrs', action=utils.StoreDictKeyPair, metavar="KEY1=VAL1,KEY2=VAL2...")
    parser.add_argument('--list')
    parser.add_argument('--remove', metavar='ID', type=int)
    parser.add_argument('--done', metavar='ID', type=int)
    parser.add_argument('-U', dest='update', action='store_true')

    args = parser.parse_args()

    helper = TaskSQLite()
    helper.__enter__()

    helper.create_table()

    if args.list:
        if args.list == 'all':
            results = helper.collect_all()
        elif args.list == 'todo':
            results = helper.collect_uncompleted()
        else:
            sys.exit()

        print("{:<10}{:<8}{:<10}{}".format("Priority", "Id", "Done", "Title"))
        for i, r in enumerate(results):
            print("{:<10}{:<8}{:<10}{}".format(f"[{i+1}]", r.id, r.completed, r.title))
        sys.exit()

    if args.done:
        helper.update(args.done, {'completed': 1})
        sys.exit()

    if args.remove:
        helper.delete(args.remove)
        sys.exit()

    attrs = {}
    for k, v in args.attrs.items():
        attrs[k] = v

    if args.update:
        if 'id' not in attrs.keys():
            print('Not Found Any Id')
            sys.exit()
        idx = attrs.pop('id')
        helper.update(idx, attrs)

    else:
        try:
            task = Task(
                index=0,
                title=attrs['title'],
                description=attrs.get('description'),
                due_date=attrs['due_date'] if 'due_date' in attrs.keys() else datetime.now().strftime(
                    TaskSQLite.date_format),
                completed=attrs['completed'] if 'completed' in attrs.keys() else 0,
                important=attrs['important'] if 'important' in attrs.keys() else 0,
                point=0
            )

            helper.add(task)
        except sqlite3.DatabaseError as e:
            print(e)
            helper.rollback()
