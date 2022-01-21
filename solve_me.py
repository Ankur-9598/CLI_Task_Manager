from ast import arg
from turtle import pen


class TasksCommand:
    TASKS_FILE = "tasks.txt"
    COMPLETED_TASKS_FILE = "completed.txt"

    current_items = {}
    completed_items = []

    def read_current(self):
        try:
            file = open(self.TASKS_FILE, "r")
            for line in file.readlines():
                item = line[:-1].split(" ")
                self.current_items[int(item[0])] = " ".join(item[1:])
            file.close()
        except Exception:
            pass

    def read_completed(self):
        try:
            file = open(self.COMPLETED_TASKS_FILE, "r")
            for line in file.readlines():
                completed_task = line[:-1]
                self.completed_items.append(completed_task);
            file.close()
        except Exception:
            pass

    def write_current(self):
        with open(self.TASKS_FILE, "w+") as f:
            f.truncate(0)
            for key in sorted(self.current_items.keys()):
                f.write(f"{key} {self.current_items[key]}\n")

    def write_completed(self):
        with open(self.COMPLETED_TASKS_FILE, "w+") as f:
            f.truncate(0)
            for item in self.completed_items:
                f.write(f"{item}\n")

    def run(self, command, args):
        self.read_current()
        self.read_completed()
        if command == "add":
            self.add(args)
        elif command == "done":
            self.done(args)
        elif command == "delete":
            self.delete(args)
        elif command == "ls":
            self.ls()
        elif command == "report":
            self.report()
        elif command == "help":
            self.help()

    def help(self):
        print(
            """Usage :-
$ python tasks.py add 2 hello world # Add a new item with priority 2 and text "hello world" to the list
$ python tasks.py ls # Show incomplete priority list items sorted by priority in ascending order
$ python tasks.py del PRIORITY_NUMBER # Delete the incomplete item with the given priority number
$ python tasks.py done PRIORITY_NUMBER # Mark the incomplete item with the given PRIORITY_NUMBER as complete
$ python tasks.py help # Show usage
$ python tasks.py report # Statistics"""
        )

    def add(self, args):
        try:
            if len(args) == 0:
                raise Exception("Priority and Task name is not given!")

            if len(args) == 1:
                raise Exception("Task name is not provided!")

            curr_priority = int(args[0])
            curr_task = args[1:][0]
            print(f'Added task: "{curr_task}" with priority {curr_priority}')

            while(self.current_items.get(curr_priority)):
                temp_task_name = self.current_items.get(curr_priority)
                self.current_items[curr_priority] = curr_task
                curr_task = temp_task_name
                curr_priority += 1
            
            self.current_items[curr_priority] = curr_task
            self.write_current()

        except TypeError:
            print("Error: No prority and task name is given!")

        except Exception as e:
            print(e)

    def done(self, args):
        try:
            task_priority = int(args[0])
            if not self.current_items.get(task_priority):
                raise Exception(f"Error: no incomplete item with priority {task_priority} exists.")
            
            completed_task = self.current_items[task_priority]
            self.completed_items.append(completed_task)
            self.write_completed()

            self.current_items.pop(task_priority)
            self.write_current()

            print("Marked item as done.")
        
        except TypeError:
            print("Error: No task priority is given to mark done!")

        except Exception as e:
            print(e)

    def delete(self, args):
        try:
            task_priority = int(args[0])
            if not self.current_items.get(task_priority):
                raise Exception(f"Error: item with priority {task_priority} does not exist. Nothing deleted.")

            self.current_items.pop(task_priority)
            print(f"Deleted item with priority {task_priority}")

        except TypeError:
            print("No task priority given!")

        except Exception as e:
            print(e)
        pass

    def ls(self):
        if len(self.current_items) == 0:
            print("No incomplete tasks!")
            return
        for index, priority in enumerate(self.current_items):
            print(f"{index + 1}. {self.current_items[priority]} [{priority}]")


    def report(self):
        pending_task_cnt = len(self.current_items)
        print(f"Pending : {pending_task_cnt}")
        self.ls()
        print()

        completed_task_cnt = len(self.completed_items)
        print(f"Completed : {completed_task_cnt}")
        for index, completed_task in enumerate(self.completed_items):
            print(f"{index + 1}. {completed_task}")
