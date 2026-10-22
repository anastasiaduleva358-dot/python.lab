# teacher_functions.py
import re
import os 

def initialize_data():
    return {}

def validate_name(name):
    pattern = r'^[A-Za-zA-Яа-я]+(-[A-Za-zA-Яа-я]+)?$'
    if 1 <= len(name) <= 30 and re.match(pattern, name):
        return True
    return False

def validate_discipline(discipline):
    pattern = r'^[A-Za-zA-Яа-я0-9\s]{2,50}$'
    if re.match(pattern, discipline):
       return True
    return False

def load_from_file(filename):
    teachers = {}
    if os.path.exists(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if line:
                        parts = line.split(':')
                        if len(parts) == 2:
                            name = parts[0]
                            disciplines = parts[1].split(',') if parts[1] else []
                            teachers[name] = disciplines
        except Exception as e:
            print(f"Ошибка при загрузке файла: {e}")
    return teachers

def save_to_file(filename, teachers):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            for name, disciplines in teachers.items():
                disciplines_str = ','.join(disciplines)
                file.write(f"{name}:{disciplines_str}\n")
        print("Данные успешно сохранены в файл")
    except Exception as e:
        print(f"Ошибка при сохранении в файл: {e}")

def add_teacher(teachers, filename):
    print("\n---Добавление нового преподавателя---")

    while True:
        first_name = input("Введите имя преподавателя: ").strip()
        if validate_name(first_name):
            break
        print("Ошибка! Имя должно содержать только буквы (1-30 символов), может содержать дефис")

    while  True:
        last_name = input("Введите фамилию преподавателя:").strip()
        if validate_name(last_name):
            break
        print("Ошибка! Фамилия должно содержать только буквы (1-30 символов), может содержать дефис")

    full_name = f"{first_name}_{last_name}"

    name_exists = False
    for existing_name in teachers:
        if existing_name.lower() == full_name.lower():
            name_exists = True
            break

    if name_exists:
        print(f"Преподаватель {full_name} уже существует!")
        return
    
    teachers[full_name] = []
    print(f"Преподаватель {full_name} успешно добавлен")

    add_disciplines_now = input("Хотите добавить дисциплину сейчас? (Y/N): ").upper()
    if add_disciplines_now == 'Y' or add_disciplines_now == 'Д':
        add_disciplines_to_teacher(teachers, full_name, filename)

    save_to_file(filename, teachers)

def add_disciplines_to_teacher(teachers, teacher_name, filename):
    if teacher_name not in teachers:
        print(f"Преподаватель {teacher_name} не найден!")
        return
    
    print(f"\n--- Добавление дисциплин для {teacher_name} ---")

    while True:
        while True:
            discipline = input("Введите название дисциплины: ").strip()
            if validate_discipline(discipline):
                break
            print("Ошибка! Дисциплина должна содержать буквы, цифры, пробелы (2-50 символов)")

        if discipline not in teachers[teacher_name]:
            teachers[teacher_name].append(discipline)
            print(f"Дисциплина '{discipline}' добавлена")
        else:
            print(f"Дисциплина '{discipline}' уже есть у преподавателя")

        choice = input("Добавить еще одну дисциплину? (Y/N): ").upper()
        if choice != 'Y' and choice != 'Д':
            break

    save_to_file(filename, teachers)

def edit_discipline(teachers, filename):
    print("\n---Изменение названия дисциплины---")
    if not teachers:
        print("Список преподавателей пуст!")
        return
        
    print("Список преподавателей:")
    for i, name in enumerate(teachers.keys(),1):
        print(f"{i}. {name}")

    teacher_name = input("Введите имя_фамилию преподавателя: ").strip()

    if teacher_name not in teachers:
        print("Преподаватель не найден!")
        return
    
    if not teachers[teacher_name]:
        print(f"У преподавателя {teacher_name} нет дисциплин")
        return
    
    print(f"Дисциплины преподавателя {teacher_name}:")
    for i, disc in enumerate(teachers[teacher_name], 1):
        print(f"{i}. {disc}")

    old_discipline = input("Введите название дисциплины, которую хотите изменить:").strip()

    if old_discipline not in teachers[teacher_name]:
        print("Такая дисциплина не найдена!")
        return
    
    while True:
        new_discipline = input("Введите новое название дисциплины:").strip()
        if validate_discipline(new_discipline):
            break
        print("Ошибка! Дисциплина должна содержать буквы, цифры, пробелы (2-50 символов)")

    index = teachers[teacher_name].index(old_discipline)
    teachers[teacher_name][index] = new_discipline
    print("Дисциплина успешно изменена")

    save_to_file(filename, teachers)
 
def display_teachers(teachers):
    print("\n--- Список преподавателей и дисциплин ---")
    
    if not teachers:
        print("Список преподавателей пуст!")
        return
    
    for name, disciplines in teachers.items():
        print(f"\nПреподаватель: {name}")
        print(f"Количество дисциплин {len(disciplines)}")
        if disciplines:
            print("Дисциплины:")
            for disc in disciplines:
                print(f" - {disc}")
        else:
            print(" Нет дисциплин")

def delete_teacher(teachers, filename):
    print("\n--- Удаление преподавателя ---")

    if not teachers:
        print("Список преподавателей пуст!")
        return
    
    print("Список преподавателей:")
    for i, name in enumerate(teachers.keys(),1):
        print(f"{i}. {name}")

    teacher_name = input("Введите имя_фамилию преподавателя для удаления: ").strip()

    if teacher_name not in teachers:
        print("Преподаватель не найден!")
        return

    confirmation = input(f"Вы уверены, что хотите удалить  {teacher_name}? (Y/N)").upper()
    if confirmation == 'Y' or confirmation == 'Д':
        del teachers[teacher_name]
        print(f"Преподаватель {teacher_name} удален")
        save_to_file(filename, teachers)
    else:
        print("Удаление отменено")

def get_statistics(teachers):
    print("\n--- Статистика ---")

    total_teachers = len(teachers)

    total_disciplines = 0
    for disciplines in teachers.values():
        total_disciplines += len(disciplines)

    print(f"Общее количество преподавателей: {total_teachers}")
    print(f"Общее количество дисциплин: {total_disciplines}")

    return total_teachers, total_disciplines

def find_teacher_with_max_disciplines(teachers):
    print("\n--- Преподаватель(и) с наибольшим количеством дисциплин ---")

    if not teachers:
        print("Список преподавателей пуст!")
        return
    
    max_disciplines = 0
    for disciplines in teachers.values():
        if len(disciplines) > max_disciplines:
            max_disciplines = len(disciplines)

    if max_disciplines == 0:
        print("У всех преподавателей нет дисциплин")
        return
    
    print(f"Максимальное количество дисциплин {max_disciplines}")
    print("Преподаватели:")
    for name, disciplines in teachers.items():
        if len(disciplines) == max_disciplines:
            print(f" - {name}")

def search_teachers(teachers):
    print("\n--- Поиск преподавателя ---")

    search_name = input(" Введите имя или фамилию для поиска: ").strip().lower()

    found = False
    for full_name, disciplines in teachers.items():
        if search_name in full_name.lower():
            print(f"\nНайден преподаватель: {full_name}")
            print(f"Количество дисциплин: {len(disciplines)}")
            if disciplines:
                print("Дисциплины:")
                for disc in disciplines:
                    print(f" - {disc}")
            found = True

    if not found:
        print("Преподаватели не найдены")

def display_unique_disciplines(teachers):
    print("\n---  Уникальные дисциплины (в алфавитном порядке) ---")

    all_disciplines = set()
    for disciplines in teachers.values():
        all_disciplines.update(disciplines)

    if not all_disciplines:
        print("Нет дисциплин")
        return
    
    sorted_disciplines = sorted(all_disciplines)
    for disc in sorted_disciplines:
        print(f" - {disc}")

    print(f"\nВсего уникальных дисциплин: {len(sorted_disciplines)}")



