LOW = "1"
MEDIUM = "2"
HIGH = "3"
STATUS = {
    LOW: "Low",
    MEDIUM: "Medium",
    HIGH: "High"
}

OPEN = "1"
IN_PROGRESS = "2"
CLOSED = "3"
PRIORITY = {
    OPEN: "Open",
    IN_PROGRESS: "In Progress",
    CLOSED: "Closed"
}

READ_GENERAL = "1"
READ_STATUS = "2"
READ_PRIORITY = "3"
READ_SEARCH = "4"
READ_MENU = {
    READ_GENERAL: "Read as is",
    READ_STATUS: "Read sorted by status",
    READ_PRIORITY: "Read sorted by priority",
    READ_SEARCH: "Read with search",
}

UPDATE_NAME = "1"
UPDATE_DESCRIPTION = "2"
UPDATE_PRIORITY = "3"
UPDATE_STATUS = "4"
UPDATE_MENU = {
    UPDATE_NAME: "Update name",
    UPDATE_DESCRIPTION: "Update description",
    UPDATE_PRIORITY: "Update priority",
    UPDATE_STATUS: "Update status"
}

NEW_TASK = "1"
READ_TASKS = "2"
UPDATE_TASK = "3"
DELETE_TASK = "4"
EXIT = "0"
MAIN_MENU = {
    NEW_TASK: "New task",
    READ_TASKS: "Read tasks",
    UPDATE_TASK: "Update task",
    DELETE_TASK: "Delete task",
    EXIT: "Exit"
}


def input_task() -> dict:
    name = input("Enter task name: ")
    description = input("Enter task description: ")
    priority = input_process(PRIORITY)
    status = input_process(STATUS)
    return get_task(name, description, PRIORITY[priority], STATUS[status])


def print_menu(menu: dict) -> None:
    print("Possible options:")
    for value, means in menu.items():
        print(f"{value}: {means}")


def validate_input(value: str, options: dict) -> None:
    if value not in options:
        raise ValueError


def generate_id(tasks: dict) -> int:
    return max(tasks.keys()) + 1 if tasks else 1


def task_to_string(task: dict, task_id: int) -> str:
    return f"{task_id}: {', '.join([str(v) for k, v in task.items()])}"


def get_task(name: str, description: str, priority: str, status: str) -> dict:
    return {'name': name, 'description': description, 'priority': priority, 'status': status}


def add_task(task: dict, tasks: dict) -> None:
    task_id = generate_id(tasks)
    tasks[task_id] = task
    tasks_to_file(tasks)
    print('Task added')


def delete_task(task_id: int, tasks: dict) -> None:
    if task_id in tasks:
        del tasks[task_id]
        tasks_to_file(tasks)
    else:
        print(f'Task {task_id} not found')
        raise ValueError


def search_tasks(tasks: dict, search) -> dict:
    return {task_id: task for task_id, task in tasks.items() if
            search.lower() in task['name'].lower() or search.lower() in task['description'].lower()}


def ordering_tasks(tasks: dict, ordering) -> dict:
    if ordering == 'priority':
        return dict(sorted(tasks.items(), key=lambda x: x[1]['priority']))
    elif ordering == 'status':
        return dict(sorted(tasks.items(), key=lambda x: x[1]['status']))
    else:
        raise ValueError


def get_tasks(tasks: dict, ordering: str | None = None, search: str | None = None) -> list[str]:
    if not ordering and not search:
        filtered_tasks = tasks
    elif not ordering and search:
        filtered_tasks = search_tasks(tasks, search)
    elif ordering and not search:
        filtered_tasks = ordering_tasks(tasks, ordering)
    else:
        filtered_tasks = ordering_tasks(search_tasks(tasks, search), ordering)
    return [task_to_string(task, task_id) for task_id, task in filtered_tasks.items()]


def tasks_to_file(tasks: dict) -> None:
    with open('tasks.txt', 'w') as file:
        for task_id, task in tasks.items():
            file.write(task_to_string(task, task_id) + '\n')


def from_file_to_tasks() -> dict:
    tasks = {}
    try:
        with open('tasks.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                task_id, task_info = line.strip().split(': ')
                task = {'name': (task_info.split(', '))[0], 'description': (task_info.split(', '))[1],
                        'priority': (task_info.split(', '))[2], 'status': (task_info.split(', '))[3]}
                tasks[int(task_id)] = task
    except FileNotFoundError:
        pass
    finally:
        return tasks


def input_process(menu: dict) -> str:
    while True:
        print_menu(menu)
        input_value = input("Please select an option: ")
        try:
            validate_input(input_value, menu)
        except ValueError:
            print(f"'{input_value}' is not a valid option")
        else:
            return input_value


def print_tasks(tasks: list[str]) -> None:
    for task in tasks:
        print(task)


def validate_task_id(task_id: int, tasks: dict) -> None:
    if task_id not in tasks.keys():
        raise ValueError


def get_task_id(tasks: dict) -> int:
    while True:
        try:
            task_id = int(input("Please type task id: "))
        except ValueError:
            print(f"value should be a number")
            continue
        try:
            validate_task_id(task_id, tasks)
        except ValueError:
            print(f'Task {task_id} not found. Please try again.')
        else:
            return int(task_id)


def update_task_by_field(field: str, task_id: int, tasks: dict) -> None:
    if field == 'status':
        value = STATUS[input_process(STATUS)]
    elif field == 'priority':
        value = PRIORITY[input_process(PRIORITY)]
    else:
        value = input("Input value:")
    tasks[task_id][field] = value
    print(f'Task {task_id} updated {field}: {value}')


def run_main_process(tasks: dict) -> None:
    while True:
        menu_selection = input_process(MAIN_MENU)
        if menu_selection == NEW_TASK:
            task = input_task()
            add_task(task, tasks)
        elif menu_selection == READ_TASKS:
            read_menu_selection = input_process(READ_MENU)
            if read_menu_selection == READ_GENERAL:
                print_tasks(get_tasks(tasks))
            elif read_menu_selection == READ_STATUS:
                print_tasks(get_tasks(tasks, ordering="status"))
            elif read_menu_selection == READ_PRIORITY:
                print_tasks(get_tasks(tasks, ordering="priority"))
            elif read_menu_selection == READ_SEARCH:
                search_value = input("Please enter a search string: ")
                print_tasks(get_tasks(tasks, search=search_value))
        elif menu_selection == UPDATE_TASK:
            task_id = get_task_id(tasks)
            update_menu_selection = input_process(UPDATE_MENU)
            if update_menu_selection == UPDATE_NAME:
                update_task_by_field('name', task_id, tasks)
            elif update_menu_selection == UPDATE_DESCRIPTION:
                update_task_by_field('description', task_id, tasks)
            elif update_menu_selection == UPDATE_PRIORITY:
                update_task_by_field('priority', task_id, tasks)
            elif update_menu_selection == UPDATE_STATUS:
                update_task_by_field('status', task_id, tasks)
        elif menu_selection == DELETE_TASK:
            task_id = get_task_id(tasks)
            delete_task(task_id, tasks)
        elif menu_selection == EXIT:
            break


def main():
    all_tasks = from_file_to_tasks()
    run_main_process(all_tasks)


main()
