#main.py
import teacher_functions as tf
import os
import sys
import io

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    os.system('chcp 65001 > nul')

def display_menu():
    print("\n" + "="*50)
    print("ПРОГРАММА УПРАВЛЕНИЯ ДАННЫМИ О ПРЕПОДАВАТЕЛЯХ")
    print("="*50)
    print("1. Добавить нового преподавателя")
    print("2. Добавить дисциплину преподавателю")
    print("3. Изменить название дисциплины")
    print("4. Показать всех преподавателей и дисциплины")
    print("5. Удалить преподавателя")
    print("6. Показать статистику")
    print("7. Найти преподавателя с максимальным количеством дисциплин")
    print("8. Поиск преподавателя по имени")
    print("9. Показать все уникальные дисциплины")
    print("10. Выход")
    print("="*50)

def main():
    filename = "teachers_data.txt"

    teachers = tf.load_from_file(filename)
    print(f"Загружено {len(teachers)} преподавателей из файла")

    while True:
        display_menu()

        try:
            choice = input("Выберите опцию (1-10): ").strip()

            if choice == '1':
                tf.add_teacher(teachers, filename)

            elif choice == '2':
                if not teachers:
                    print("Список преподавателей пуст! Сначала добавьте преподавателей.")

                else:
                    teacher_name = input("Введите имя_фамилию преподавателя: ").strip()
                    tf.add_disciplines_to_teacher(teachers, teacher_name, filename)
            
            elif choice == '3':
                tf.edit_discipline(teachers, filename)

            elif choice == '4':
                tf.display_teachers(teachers)

            elif choice == '5':
                tf.delete_teacher(teachers, filename)

            elif choice == '6':
                tf.get_statistics(teachers)

            elif choice == '7':
                tf.find_teacher_with_max_disciplines(teachers)

            elif choice == '8':
                tf.search_teachers(teachers)

            elif choice == '9':
                tf.display_unique_disciplines(teachers)

            elif choice == '10':
                print("Программа завершена.")
                break

            else:
                print("Ошибка! Введите число от 1 до 10")
        
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            print("Попробуйте снова")

if __name__ == "__main__":
    main()

             

