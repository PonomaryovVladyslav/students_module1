def generate_id(tasks: dict) -> int:
    return max(tasks.keys()) + 1 if tasks else 1


def task_to_string(task: dict, task_id: int) -> str:
    return f"{task_id}: {', '.join([str(v) for k, v in task.items()])}"


def new_task(name: str, description: str, priority: str, status: str) -> dict:
    return {'name': name, 'description': description, 'priority': priority, 'status': status}


def add_task(name: str, description: str, priority: str, status: str, tasks: dict) -> None:
    task_id = generate_id(tasks)
    tasks[task_id] = new_task(name, description, priority, status)
    tasks_to_file(tasks)


def update_task(task_id: int, tasks: dict, to_update: dict) -> None:
    tasks[task_id].update(to_update)
    tasks_to_file(tasks)


def delete_task(task_id: int, tasks: dict) -> None:
    if task_id in tasks:
        del tasks[task_id]
        tasks_to_file(tasks)
    else:
        print(f'Task {task_id} not found')


def search_tasks(tasks: dict, search) -> dict:
    return {task_id: task for task_id, task in tasks.items() if
            search.lower() in task['name'].lower() or search.lower() in task['description'].lower()}


def ordering_tasks(tasks: dict, ordering) -> dict:
    if ordering == 'priority':
        return dict(sorted(tasks.items(), key=lambda x: x[1]['priority']))
    elif ordering == 'status':
        return dict(sorted(tasks.items(), key=lambda x: x[1]['status']))
    else:
        return tasks


def get_tasks(tasks: dict, ordering: str | None, search: str | None) -> list[str]:
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


def from_file_to_tasks() -> None:
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
        return tasks


def main():
    all_tasks = from_file_to_tasks()


main()
