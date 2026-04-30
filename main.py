import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import random
import json
from datetime import datetime
import os
import sys

class QuoteGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Quote Generator")
        self.root.geometry("800x600")
        
        # Определяем пути к файлам в той же директории, что и скрипт
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.quotes_file = os.path.join(self.script_dir, 'quotes_data.json')
        self.history_file = os.path.join(self.script_dir, 'history.json')
        
        # Предопределенные цитаты
        self.quotes = [
            {"text": "Будьте сами собой, все остальные роли уже заняты.", "author": "Оскар Уайльд", "theme": "жизнь"},
            {"text": "Единственный способ делать великие дела — любить то, что вы делаете.", "author": "Стив Джобс", "theme": "мотивация"},
            {"text": "Жизнь — это то, что происходит с вами, пока вы строите другие планы.", "author": "Джон Леннон", "theme": "жизнь"},
            {"text": "Лучшее время посадить дерево было 20 лет назад. Следующее лучшее время — сегодня.", "author": "Китайская пословица", "theme": "мотивация"},
            {"text": "Будьте изменением, которое хотите видеть в мире.", "author": "Махатма Ганди", "theme": "мудрость"},
            {"text": "Успех — это способность идти от поражения к поражению, не теряя энтузиазма.", "author": "Уинстон Черчилль", "theme": "успех"},
            {"text": "Образование — это то, что остается после того, как забываешь все, чему учили в школе.", "author": "Альберт Эйнштейн", "theme": "образование"},
            {"text": "В конце концов, все будет хорошо. Если сейчас плохо — значит, это еще не конец.", "author": "Джон Леннон", "theme": "оптимизм"},
            {"text": "Настоящий друг — это тот, кто будет держать тебя за руку и чувствовать твое сердце.", "author": "Габриэль Гарсиа Маркес", "theme": "дружба"},
            {"text": "Сложнее всего начать действовать, все остальное зависит только от упорства.", "author": "Амелия Эрхарт", "theme": "мотивация"}
        ]
        
        # История сгенерированных цитат
        self.history = []
        
        # Загрузка данных из файлов
        self.load_quotes()
        self.load_history()
        
        # Создание интерфейса
        self.setup_ui()
        
        # Сохраняем начальные данные
        self.save_quotes()
        
    def setup_ui(self):
        # Создание вкладок
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Вкладка генерации цитат
        gen_frame = ttk.Frame(notebook)
        notebook.add(gen_frame, text='Генератор цитат')
        self.create_generator_tab(gen_frame)
        
        # Вкладка истории
        history_frame = ttk.Frame(notebook)
        notebook.add(history_frame, text='История')
        self.create_history_tab(history_frame)
        
        # Вкладка добавления цитат
        add_frame = ttk.Frame(notebook)
        notebook.add(add_frame, text='Добавить цитату')
        self.create_add_quote_tab(add_frame)
        
        # Вкладка фильтрации
        filter_frame = ttk.Frame(notebook)
        notebook.add(filter_frame, text='Фильтры')
        self.create_filter_tab(filter_frame)
        
        # Добавляем кнопку проверки файлов
        self.add_debug_button()
        
    def add_debug_button(self):
        """Добавляет кнопку для проверки состояния файлов"""
        debug_frame = ttk.Frame(self.root)
        debug_frame.pack(pady=5)
        
        debug_btn = ttk.Button(debug_frame, text="Проверить файлы", 
                               command=self.check_files)
        debug_btn.pack(side=tk.LEFT, padx=5)
        
        self.debug_label = ttk.Label(debug_frame, text="")
        self.debug_label.pack(side=tk.LEFT, padx=5)
        
    def check_files(self):
        """Проверяет существование и права доступа к файлам"""
        info = []
        for file_path in [self.quotes_file, self.history_file]:
            if os.path.exists(file_path):
                info.append(f"✓ {os.path.basename(file_path)} существует")
                # Проверяем права на запись
                if os.access(file_path, os.W_OK):
                    info.append(f"  - есть права на запись")
                else:
                    info.append(f"  - ❌ нет прав на запись!")
            else:
                info.append(f"❌ {os.path.basename(file_path)} не существует")
                info.append(f"  - путь: {file_path}")
        
        self.debug_label.config(text=" | ".join(info))
        print("\n".join(info))  # Также выводим в консоль
        
    def create_generator_tab(self, parent):
        # Фрейм для отображения цитаты
        quote_frame = ttk.LabelFrame(parent, text="Случайная цитата", padding="10")
        quote_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.quote_text = scrolledtext.ScrolledText(quote_frame, height=5, wrap=tk.WORD)
        self.quote_text.pack(fill='both', expand=True)
        
        self.author_label = ttk.Label(quote_frame, text="", font=('Arial', 10, 'italic'))
        self.author_label.pack()
        
        self.theme_label = ttk.Label(quote_frame, text="", font=('Arial', 9))
        self.theme_label.pack()
        
        # Кнопки
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(pady=10)
        
        generate_btn = ttk.Button(btn_frame, text="Сгенерировать цитату", 
                                 command=self.generate_random_quote)
        generate_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = ttk.Button(btn_frame, text="Очистить", 
                              command=self.clear_display)
        clear_btn.pack(side=tk.LEFT, padx=5)
        
    def create_history_tab(self, parent):
        # Список истории
        history_frame = ttk.Frame(parent)
        history_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Дерево для отображения истории
        columns = ('Дата', 'Цитата', 'Автор', 'Тема')
        self.history_tree = ttk.Treeview(history_frame, columns=columns, show='headings')
        
        for col in columns:
            self.history_tree.heading(col, text=col)
            self.history_tree.column(col, width=150)
        
        self.history_tree.pack(fill='both', expand=True, side=tk.LEFT)
        
        # Скроллбар
        scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        
        # Кнопки управления историей
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(pady=5)
        
        refresh_btn = ttk.Button(btn_frame, text="Обновить", 
                                command=self.refresh_history_display)
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        clear_history_btn = ttk.Button(btn_frame, text="Очистить историю", 
                                      command=self.clear_history)
        clear_history_btn.pack(side=tk.LEFT, padx=5)
        
        # Загружаем историю при создании
        self.refresh_history_display()
        
    def create_add_quote_tab(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Поля ввода
        ttk.Label(frame, text="Текст цитаты:").pack(anchor=tk.W)
        self.new_quote_text = tk.Text(frame, height=3, width=50)
        self.new_quote_text.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(frame, text="Автор:").pack(anchor=tk.W)
        self.new_quote_author = ttk.Entry(frame, width=50)
        self.new_quote_author.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(frame, text="Тема:").pack(anchor=tk.W)
        self.new_quote_theme = ttk.Entry(frame, width=50)
        self.new_quote_theme.pack(fill=tk.X, pady=(0, 20))
        
        # Кнопка добавления
        add_btn = ttk.Button(frame, text="Добавить цитату", 
                            command=self.add_new_quote)
        add_btn.pack()
        
    def create_filter_tab(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Фильтр по автору
        ttk.Label(frame, text="Фильтр по автору:").pack(anchor=tk.W)
        self.author_filter = ttk.Entry(frame, width=50)
        self.author_filter.pack(fill=tk.X, pady=(0, 20))
        
        # Фильтр по теме
        ttk.Label(frame, text="Фильтр по теме:").pack(anchor=tk.W)
        self.theme_filter = ttk.Entry(frame, width=50)
        self.theme_filter.pack(fill=tk.X, pady=(0, 20))
        
        # Кнопки фильтрации
        btn_frame = ttk.Frame(frame)
        btn_frame.pack()
        
        apply_filter_btn = ttk.Button(btn_frame, text="Применить фильтр", 
                                     command=self.apply_filters)
        apply_filter_btn.pack(side=tk.LEFT, padx=5)
        
        clear_filter_btn = ttk.Button(btn_frame, text="Сбросить фильтры", 
                                     command=self.clear_filters)
        clear_filter_btn.pack(side=tk.LEFT, padx=5)
        
        # Результаты фильтрации
        result_frame = ttk.LabelFrame(frame, text="Результаты фильтрации", padding="10")
        result_frame.pack(fill='both', expand=True, pady=20)
        
        self.filter_result = scrolledtext.ScrolledText(result_frame, height=10)
        self.filter_result.pack(fill='both', expand=True)
        
    def generate_random_quote(self):
        if not self.quotes:
            messagebox.showwarning("Предупреждение", "Нет доступных цитат!")
            return
            
        quote = random.choice(self.quotes)
        
        # Отображаем цитату
        self.quote_text.delete(1.0, tk.END)
        self.quote_text.insert(1.0, quote['text'])
        self.author_label.config(text=f"— {quote['author']}")
        self.theme_label.config(text=f"Тема: {quote['theme']}")
        
        # Добавляем в историю
        history_entry = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'quote': quote['text'],
            'author': quote['author'],
            'theme': quote['theme']
        }
        self.history.append(history_entry)
        self.save_history()
        self.refresh_history_display()
        
    def add_new_quote(self):
        # Получаем данные из полей
        text = self.new_quote_text.get(1.0, tk.END).strip()
        author = self.new_quote_author.get().strip()
        theme = self.new_quote_theme.get().strip()
        
        # Проверка на пустые строки
        if not text:
            messagebox.showerror("Ошибка", "Текст цитаты не может быть пустым!")
            return
        if not author:
            messagebox.showerror("Ошибка", "Имя автора не может быть пустым!")
            return
        if not theme:
            messagebox.showerror("Ошибка", "Тема не может быть пустой!")
            return
            
        # Добавляем новую цитату
        new_quote = {
            'text': text,
            'author': author,
            'theme': theme.lower()
        }
        self.quotes.append(new_quote)
        
        # Сохраняем и проверяем результат
        if self.save_quotes():
            # Очищаем поля только при успешном сохранении
            self.new_quote_text.delete(1.0, tk.END)
            self.new_quote_author.delete(0, tk.END)
            self.new_quote_theme.delete(0, tk.END)
            messagebox.showinfo("Успех", "Цитата успешно добавлена и сохранена!")
        else:
            messagebox.showerror("Ошибка", "Цитата добавлена в программу, но не сохранена в файл!")
        
    def apply_filters(self):
        author_filter = self.author_filter.get().strip().lower()
        theme_filter = self.theme_filter.get().strip().lower()
        
        filtered_quotes = []
        
        for quote in self.quotes:
            if author_filter and theme_filter:
                if (author_filter in quote['author'].lower() and 
                    theme_filter in quote['theme'].lower()):
                    filtered_quotes.append(quote)
            elif author_filter:
                if author_filter in quote['author'].lower():
                    filtered_quotes.append(quote)
            elif theme_filter:
                if theme_filter in quote['theme'].lower():
                    filtered_quotes.append(quote)
                    
        # Отображаем результаты
        self.filter_result.delete(1.0, tk.END)
        
        if not filtered_quotes:
            self.filter_result.insert(1.0, "Цитаты не найдены по заданным критериям.")
        else:
            for i, quote in enumerate(filtered_quotes, 1):
                self.filter_result.insert(tk.END, f"{i}. \"{quote['text']}\"\n")
                self.filter_result.insert(tk.END, f"   — {quote['author']} | Тема: {quote['theme']}\n\n")
                
    def clear_filters(self):
        self.author_filter.delete(0, tk.END)
        self.theme_filter.delete(0, tk.END)
        self.filter_result.delete(1.0, tk.END)
        
    def clear_display(self):
        self.quote_text.delete(1.0, tk.END)
        self.author_label.config(text="")
        self.theme_label.config(text="")
        
    def clear_history(self):
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите очистить всю историю?"):
            self.history = []
            if self.save_history():
                self.refresh_history_display()
                messagebox.showinfo("Успех", "История очищена!")
            else:
                messagebox.showerror("Ошибка", "Не удалось очистить историю в файле!")
            
    def refresh_history_display(self):
        # Очищаем дерево
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
            
        # Добавляем элементы из истории (показываем последние 50)
        for entry in self.history[-50:]:
            self.history_tree.insert('', 0, values=(
                entry['timestamp'],
                entry['quote'],
                entry['author'],
                entry['theme']
            ))
            
    def save_quotes(self):
        """Сохраняет цитаты в JSON файл. Возвращает True при успехе, False при ошибке"""
        try:
            print(f"Попытка сохранить цитаты в: {self.quotes_file}")
            
            # Создаем директорию, если её нет
            os.makedirs(os.path.dirname(self.quotes_file), exist_ok=True)
            
            with open(self.quotes_file, 'w', encoding='utf-8') as f:
                json.dump(self.quotes, f, ensure_ascii=False, indent=2)
            
            print(f"Успешно сохранено {len(self.quotes)} цитат")
            return True
            
        except PermissionError as e:
            messagebox.showerror("Ошибка доступа", 
                               f"Нет прав на запись в файл:\n{self.quotes_file}\n\nОшибка: {e}")
            print(f"PermissionError: {e}")
            return False
            
        except Exception as e:
            messagebox.showerror("Ошибка сохранения", 
                               f"Не удалось сохранить цитаты:\n{e}")
            print(f"Ошибка сохранения: {e}")
            return False
            
    def load_quotes(self):
        """Загружает цитаты из JSON файла"""
        try:
            if os.path.exists(self.quotes_file):
                print(f"Загрузка цитат из: {self.quotes_file}")
                with open(self.quotes_file, 'r', encoding='utf-8') as f:
                    self.quotes = json.load(f)
                print(f"Загружено {len(self.quotes)} цитат")
            else:
                print(f"Файл цитат не найден: {self.quotes_file}")
                print("Будут использоваться предопределенные цитаты")
                
        except Exception as e:
            print(f"Ошибка загрузки цитат: {e}")
            messagebox.showwarning("Предупреждение", 
                                 f"Не удалось загрузить цитаты из файла.\nИспользуются предопределенные цитаты.\nОшибка: {e}")
            
    def save_history(self):
        """Сохраняет историю в JSON файл. Возвращает True при успехе, False при ошибке"""
        try:
            print(f"Попытка сохранить историю в: {self.history_file}")
            
            # Создаем директорию, если её нет
            os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
            
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
            
            print(f"Успешно сохранено {len(self.history)} записей истории")
            return True
            
        except PermissionError as e:
            messagebox.showerror("Ошибка доступа", 
                               f"Нет прав на запись в файл:\n{self.history_file}\n\nОшибка: {e}")
            print(f"PermissionError: {e}")
            return False
            
        except Exception as e:
            messagebox.showerror("Ошибка сохранения", 
                               f"Не удалось сохранить историю:\n{e}")
            print(f"Ошибка сохранения: {e}")
            return False
            
    def load_history(self):
        """Загружает историю из JSON файла"""
        try:
            if os.path.exists(self.history_file):
                print(f"Загрузка истории из: {self.history_file}")
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
                print(f"Загружено {len(self.history)} записей истории")
            else:
                print(f"Файл истории не найден: {self.history_file}")
                
        except Exception as e:
            print(f"Ошибка загрузки истории: {e}")
            messagebox.showwarning("Предупреждение", 
                                 f"Не удалось загрузить историю из файла.\nИстория будет пустой.\nОшибка: {e}")

def main():
    # Выводим информацию о рабочей директории
    print(f"Рабочая директория: {os.getcwd()}")
    print(f"Директория скрипта: {os.path.dirname(os.path.abspath(__file__))}")
    
    root = tk.Tk()
    app = QuoteGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()