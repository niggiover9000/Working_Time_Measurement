from time import strftime, localtime, time
from os import path
from shutil import copyfile


class Arbeitszeit:
    def __init__(self):
        self.accuracy = None

        try:
            file = open("localization/language.setting", "r")
            language_setting = file.read()
            if language_setting == "DE" or language_setting == "de":
                import localization.de as language
                self.language = language
                self.language_set = "DE"
            elif language_setting == "EN" or language_setting == "en":
                import localization.en as language
                self.language = language
                self.language_set = "EN"
            else:
                raise OSError("Config file not readable or language not yet set.")
        except OSError as Error:
            print(Error)
            while True:
                user_input = \
                    input("Choose a language / Wähle eine Sprache: (Type 'en' for English and 'de' for German): ")
                if user_input == "de" or user_input == "en" or user_input == "DE" or user_input == "EN":
                    break
                else:
                    print("Not a valid language. Type 'en' for English or 'de' for German.")
                    print("Keine gültige Sprache. Gib 'en' für Englisch oder 'de' für Deutsch ein.")
            file = open("localization/language.setting", "a")
            file.write(user_input)
            file.close()
            if user_input == "DE" or user_input == "de":
                import localization.de as language
                self.language = language
                self.language_set = "DE"
            if user_input == "EN" or user_input == "en":
                import localization.en as language
                self.language = language
                self.language_set = "EN"

    def set_accuracy(self):
        while True:
            accuracy_input = input(self.language.accuracy_string)
            try:
                self.accuracy = int(accuracy_input)
                if 1 <= self.accuracy <= 60:
                    break
                else:
                    raise ValueError(self.language.value_error)
            except (ValueError, TypeError) as Error:
                print(Error)
                continue
        print(self.language.accuracy_output_1, self.accuracy, self.language.accuracy_output_2)
        open("working_time.temp", "w").close()

    def begin_working(self):
        activity_time = localtime(time())
        accuracy_time = activity_time[4] % self.accuracy
        activity_minutes = activity_time[4] - accuracy_time
        file = open("working_time.temp", "a")
        file.write(f"[{activity_time[3]}:{activity_minutes}] {self.language.begin_shift}\n")
        file.close()
        print(f"{self.language.measurement_start_1} {activity_time[3]}:{activity_minutes} "
              f"{self.language.measurement_start_2}")

    def user_input(self):
        print(self.language.input_info_1)
        print(self.language.input_info_2)
        working = True
        while working is True:
            user_input = input(self.language.record_activity)
            if user_input == "/end":
                filename = strftime(f"[%d.%m.%Y, %H.%M.%S] {self.language.file_name}", localtime())
                pathname = path.dirname(path.realpath(__file__))
                activity_time = localtime(time())
                accuracy_time = activity_time[4] % self.accuracy
                activity_minutes = activity_time[4] + (self.accuracy - accuracy_time)
                file = open("working_time.temp", "a")
                file.write(f"[{activity_time[3]}:{activity_minutes}] {self.language.record_end}\n")
                file.close()
                copyfile("working_time.temp", f"{filename}")
                print(f"{self.language.save_success_1} '{filename}' {self.language.save_success_2} '{pathname}' "
                      f"{self.language.save_success_3}")
                working = False
            elif user_input == "/pause":
                activity_time = localtime(time())
                accuracy_time = activity_time[4] % self.accuracy
                activity_minutes = activity_time[4] + (self.accuracy - accuracy_time)
                file = open("working_time.temp", "a")
                file.write(f"[{activity_time[3]}:{activity_minutes}] --PAUSE--\n")
                file.close()
                print(self.language.pause)
            else:
                activity_time = localtime(time())
                accuracy_time = activity_time[4] % self.accuracy
                activity_minutes = activity_time[4] - accuracy_time
                file = open("working_time.temp", "a")
                file.write(f"[{activity_time[3]}:{activity_minutes}] {user_input}\n")
                file.close()
                print(f"{self.language.activity_recorded_1} {activity_time[3]}:{activity_minutes} "
                      f"{self.language.activity_recorded_2} '{user_input}' {self.language.activity_recorded_3}")


work = Arbeitszeit()
work.set_accuracy()
work.begin_working()
work.user_input()
