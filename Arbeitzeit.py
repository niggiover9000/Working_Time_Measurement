from time import strftime, localtime, mktime, time
from os import path
from shutil import copyfile


def startup():
    accuracy = -1
    while accuracy <= 1:
        accuracy_input = input("Genauigkeit in Minuten (mindestens 1, maximal 60): ")
        try:
            accuracy = int(accuracy_input)
            if accuracy <= 1 <= 60:
                raise ValueError("Zahl nicht gültig")
        except (ValueError, TypeError) as Error:
            print(Error)
            continue
    print(f"Die Zeit wird auf {accuracy} Minuten genau erfasst.")
    open("arbeitszeit.temp", "w").close()
    return accuracy
        

def begin_working(accuracy):
    activity_time = localtime(time())
    accuracy_time = activity_time[4] % accuracy
    activity_minutes = activity_time[4] - accuracy_time
    print(f"Die Arbeitszeit wird jetzt erfasst. Du hast um {activity_time[3]}:{activity_minutes} angefangen.")


def user_input(accuracy):
    print("Info: '/end' eingeben, um die Erfassung zu beenden und eine Tätigkeitsliste zu exportieren!")
    working = True
    while working is True:
        user_input = input("Tätigkeit erfassen: ")
        if user_input == "/end":
            filename = strftime("[%d.%m.%Y, %H.%M.%S] Arbeitszeit.txt", localtime())
            pathname = path.dirname(path.realpath(__file__))
            activity_time = localtime(time())
            accuracy_time = activity_time[4] % accuracy
            activity_minutes = activity_time[4] + (accuracy - accuracy_time)
            file = open("arbeitszeit.temp", "a")
            file.write(f"[{activity_time[3]}:{activity_minutes}] Arbeitszeiterfassung beendet.\n")
            file.close()
            copyfile("arbeitszeit.temp", f"{filename}")
            print(f"Gute Arbeit! Die Datei wurde als '{filename}' unter '{pathname}' gespeichert. Schönen Feierabend!")
            working = False
        else:
            activity_time = localtime(time())
            accuracy_time = activity_time[4] % accuracy
            activity_minutes = activity_time[4] - accuracy_time
            file = open("arbeitszeit.temp", "a")
            file.write(f"[{activity_time[3]}:{activity_minutes}] {user_input}\n")
            file.close()
            print(f"Um {activity_time[3]}:{activity_minutes} wurde die Tätigkeit '{user_input}' erfasst.")


accuracy = startup()
begin_working(accuracy)
user_input(accuracy)

