from config.app_config import AppConfig
from services.dictionary_service import DictionaryService
from validation.validator import Validator


class Menu:
    """Console menu for the dictionary application."""

    def __init__(self, dictionary_service=None):
        self.dictionary_service = dictionary_service or DictionaryService()

    def show_main_menu(self):
        print("\nEnglish-Vietnamese Dictionary")
        print("1. Add new word")
        print("2. Add synonym")
        print("3. Exact search")
        print("4. Approximate search")
        print("5. Show search history")
        print("6. Add favorite")
        print("7. Remove favorite")
        print("8. Show favorites")
        print("9. Show all words")
        print("10. Save data")
        print("0. Exit")

    def input_choice(self):
        while True:
            choice = input("Choose an option: ")
            if Validator.is_valid_menu_choice(
                choice, AppConfig.MIN_MENU_OPTION, AppConfig.MAX_MENU_OPTION
            ):
                return int(choice)
            print("Invalid option. Please enter a number from 0 to 10.")

    def run(self):
        self.dictionary_service.load_data()
        while True:
            self.show_main_menu()
            choice = self.input_choice()
            if choice == 1:
                self.dictionary_service.add_word_interactive()
            elif choice == 2:
                self.dictionary_service.add_synonym_interactive()
            elif choice == 3:
                self.dictionary_service.search_exact_interactive()
            elif choice == 4:
                self.dictionary_service.search_approximate_interactive()
            elif choice == 5:
                self.dictionary_service.show_history()
            elif choice == 6:
                self.dictionary_service.add_favorite_interactive()
            elif choice == 7:
                self.dictionary_service.remove_favorite_interactive()
            elif choice == 8:
                self.dictionary_service.show_favorites()
            elif choice == 9:
                self.dictionary_service.display_all_words()
            elif choice == 10:
                self.dictionary_service.save_data()
                print("Data saved.")
            elif choice == 0:
                self.dictionary_service.save_data()
                print("Goodbye.")
                break
