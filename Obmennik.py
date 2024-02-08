import requests
import tkinter as tk
import logging
from datetime import datetime

class CurrencyConverter:
    def __init__(self, root, log_file_path):
        # Инициализация объекта CurrencyConverter
        self.root = root
        self.root.title("Currency Converter")  # Заголовок окна
        self.log_file_path = log_file_path

        # Настройка логирования для предупреждений и ошибок
        self.setup_logging("warnings.log", level=logging.WARNING)
        self.setup_logging("errors.log", level=logging.ERROR)

        # Создание виджетов (элементов интерфейса)
        self.create_widgets()

    def create_widgets(self):
        # Создание фрейма для ввода данных
        input_frame = tk.Frame(self.root)
        input_frame.pack(padx=10, pady=10)

        # Элементы для ввода суммы, выбора начальной и конечной валюты
        self.amount_entry = tk.Entry(input_frame, width=10, font=("Arial", 12))
        self.amount_entry.pack(side=tk.LEFT, padx=5)

        self.from_currency_var = tk.StringVar()
        self.from_currency_var.set("USD")
        self.from_currency_menu = tk.OptionMenu(input_frame, self.from_currency_var, "USD", "EUR", "GBP")
        self.from_currency_menu.config(width=5, font=("Arial", 10))
        self.from_currency_menu.pack(side=tk.LEFT, padx=5)

        to_label = tk.Label(input_frame, text="to", font=("Arial", 12))
        to_label.pack(side=tk.LEFT)

        self.to_currency_var = tk.StringVar()
        self.to_currency_var.set("KZT")
        self.to_currency_menu = tk.OptionMenu(input_frame, self.to_currency_var, "USD", "EUR", "GBP", "KZT")
        self.to_currency_menu.config(width=5, font=("Arial", 10))
        self.to_currency_menu.pack(side=tk.LEFT, padx=5)

        # Кнопка для выполнения конвертации
        convert_button = tk.Button(input_frame, text="Convert", command=self.convert_currency, font=("Arial", 12), bg="#4CAF50", fg="white", padx=10)
        convert_button.pack(side=tk.LEFT, padx=5)

        # Элемент для вывода результата
        self.result_label = tk.Label(self.root, text="", font=("Arial", 14), wraplength=400)
        self.result_label.pack(padx=10, pady=10)

    def convert_currency(self):
        # Получение данных из элементов интерфейса
        amount = self.amount_entry.get()
        from_currency = self.from_currency_var.get()
        to_currency = self.to_currency_var.get()

        try:
            # Запрос к API для получения курса обмена
            base_url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
            response = requests.get(base_url)
            response.raise_for_status()

            data = response.json()
            conversion_rate = data["rates"][to_currency]
            converted_amount = float(amount) * conversion_rate

            # Форматирование и вывод результата
            result_text = f"{amount} {from_currency} = {converted_amount:.2f} {to_currency}"
            self.result_label.config(text=result_text)

            # Добавление логирования в файл info.txt
            log_message = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Converted {amount} {from_currency} to {converted_amount:.2f} {to_currency}"
            self.log_data(log_message)

        except requests.RequestException as e:
            # Обработка ошибок запроса
            self.result_label.config(text="Failed to fetch currency rates. Please try again later.")
            self.log_error(f"Request Exception: {str(e)}")

        except Exception as e:
            # Обработка других ошибок
            self.result_label.config(text="An error occurred during conversion.")
            self.log_error(f"Exception: {str(e)}")

    def log_data(self, message):
        # Запись информации в файл info.txt
        log_file_path = "info.txt"
        with open(log_file_path, 'a') as log_file:
            log_file.write(message + '\n')

    def log_error(self, message):
        # Запись сообщений об ошибке в файл info.txt
        log_file_path = "info.txt"
        with open(log_file_path, 'a') as log_file:
            log_file.write(f"ERROR: {message}\n")

    def setup_logging(self, log_file_path, level):
        # Настройка логирования
        logging.basicConfig(filename=log_file_path, level=level, format='%(asctime)s - %(levelname)s - %(message)s')

# Запуск приложения
if __name__ == "__main__":
    log_path = "Desktop\2119"  # Путь к папке для логов
    root = tk.Tk()
    app = CurrencyConverter(root, log_path)
    root.mainloop()
