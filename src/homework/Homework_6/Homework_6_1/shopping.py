from os.path import exists
from src.homework.Homework_6.avl_tree import *


def check_files(file_input: str, file_logs: str, file_balance: str) -> bool:
    if exists(file_input) and not exists(file_logs) and not exists(file_balance):
        return True
    if not exists(file_input):
        print(f"File {file_input} is not found")
    if exists(file_logs) or exists(file_balance):
        print(f"File for writing is already exist")
    return False


def add(storage: TreeMap[Value], size: int, count: int):
    if has_key(storage, size):
        new_count = count + get_value(storage, size)
        put(storage, size, new_count)
    else:
        put(storage, size, count)


def get(storage: TreeMap[Value], size: int) -> int:
    try:
        return get_value(storage, size)
    except ValueError:
        return 0


def select(storage: TreeMap[Value], size: int) -> str:
    try:
        customer_size = get_lower_bound(storage, size)
    except ValueError:
        return "SORRY"
    available_count = get_value(storage, customer_size)
    if available_count > 1:
        put(storage, customer_size, available_count - 1)
    else:
        remove(storage, customer_size)
    return str(customer_size)


def is_correct_data(input_data: str) -> bool:
    try:
        input_data = int(input_data)
    except ValueError:
        return False
    return input_data <= 100000


def run_commands(storage: TreeMap[Value], command: str) -> str:
    command = command.split()
    input_len = len(command)
    if command[0] == "ADD" and input_len == 3:
        size, count = command[1:]
        if is_correct_data(size) and is_correct_data(count):
            add(storage, int(size), int(count))
            return ""
    elif command[0] == "GET" and input_len == 2:
        size = command[1]
        if is_correct_data(size):
            return str(get(storage, int(size)))
    elif command[0] == "SELECT" and input_len == 2:
        size = command[1]
        if is_correct_data(size):
            return select(storage, int(size))
    return "SORRY"


def file_scrolling(storage: TreeMap[Value], file_name_input: str) -> list:
    results = list()
    with open(file_name_input, "r") as file_input:
        count_command = int(file_input.readline())
        for i in range(count_command):
            command = file_input.readline()
            result = run_commands(storage, command)
            if result:
                results.append(result + "\n")
    return results


def file_writing_logs(results: list, file_name_output: str):
    with open(file_name_output, "w") as file_output:
        file_output.writelines(results)


def file_writing_balance(balance: list, file_name_output: str):
    with open(file_name_output, "w") as file_output:
        for size, count in balance:
            file_output.write(f"{size} {count}\n")


def get_results_and_balance(file_input: str):
    storage = create_tree_map()
    results = file_scrolling(storage, file_input)
    balance = traverse(storage, "inorder")
    return results, balance


def main():
    file_input = input("Input file for reading: ")
    file_logs = input("Input file for logs: ")
    file_balance = input("Input file for balance: ")
    if check_files(file_input, file_logs, file_balance):
        results, balance = get_results_and_balance(file_input)
        file_writing_logs(results, file_logs)
        file_writing_balance(balance, file_balance)


if __name__ == "__main__":
    main()
