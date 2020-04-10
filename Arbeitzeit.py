from time import strftime, localtime, mktime, time
from os import path
from shutil import copyfile


class Arbeitszeit:
    def __init__(self):
        self.accuracy = -1

        try:
            file = open("localization/language.setting", "r")
            if file.read() == "DE":
                import localization.de as language
                self.language = "DE"
            elif file.read() == "EN":
                import localization.en as language
                self.language = "EN"
            else:
                raise OSError("Config file not readable.")
        except OSError as Error:
            print(Error)
            input("Choose a language / Wähle eine Sprache: (Type 'en' for English and 'de' for German): ")

    def set_accuracy(self):
        while self.accuracy <= 1:
            accuracy_input = input("Genauigkeit in Minuten (mindestens 1, maximal 60): ")
            try:
                self.accuracy = int(accuracy_input)
                if self.accuracy <= 1 <= 60:
                    raise ValueError("Zahl nicht gültig")
            except (ValueError, TypeError) as Error:
                print(Error)
                continue
        print(f"Die Zeit wird auf {self.accuracy} Minuten genau erfasst.")
        open("arbeitszeit.temp", "w").close()

    def begin_working(self):
        activity_time = localtime(time())
        accuracy_time = activity_time[4] % self.accuracy
        activity_minutes = activity_time[4] - accuracy_time
        file = open("arbeitszeit.temp", "a")
        file.write(f"[{activity_time[3]}:{activity_minutes}] --ARBEITSBEGINN--\n")
        file.close()
        print(f"Die Arbeitszeit wird jetzt erfasst. Du hast um {activity_time[3]}:{activity_minutes} angefangen.")


    def user_input(self):
        print("Info: '/end' eingeben, um die Erfassung zu beenden und eine Tätigkeitsliste zu exportieren.")
        print("'/pause' eingeben, um eine Pause zu erfassen.")
        working = True
        while working is True:
            user_input = input("Tätigkeit erfassen: ")
            if user_input == "/end":
                filename = strftime("[%d.%m.%Y, %H.%M.%S] Arbeitszeit.txt", localtime())
                pathname = path.dirname(path.realpath(__file__))
                activity_time = localtime(time())
                accuracy_time = activity_time[4] % self.accuracy
                activity_minutes = activity_time[4] + (self.accuracy - accuracy_time)
                file = open("arbeitszeit.temp", "a")
                file.write(f"[{activity_time[3]}:{activity_minutes}] Arbeitszeiterfassung beendet.\n")
                file.close()
                copyfile("arbeitszeit.temp", f"{filename}")
                print(f"Gute Arbeit! Die Datei wurde als '{filename}' unter '{pathname}' gespeichert. Schönen Feierabend!")
                working = False
            elif user_input == "/pause":
                activity_time = localtime(time())
                accuracy_time = activity_time[4] % self.accuracy
                activity_minutes = activity_time[4] + (self.accuracy - accuracy_time)
                file = open("arbeitszeit.temp", "a")
                file.write(f"[{activity_time[3]}:{activity_minutes}] --PAUSE--\n")
                file.close()
                print("Entspannte Pause!")
            else:
                activity_time = localtime(time())
                accuracy_time = activity_time[4] % self.accuracy
                activity_minutes = activity_time[4] - accuracy_time
                file = open("arbeitszeit.temp", "a")
                file.write(f"[{activity_time[3]}:{activity_minutes}] {user_input}\n")
                file.close()
                print(f"Um {activity_time[3]}:{activity_minutes} wurde die Tätigkeit '{user_input}' erfasst.")


arbeiten = Arbeitszeit()
arbeiten.set_accuracy()
arbeiten.begin_working()
arbeiten.user_input()
