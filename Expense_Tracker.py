import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime


class ExpenseTracker:
    """Класс для управления трекером расходов"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("?? Expense Tracker")
        self.root.geometry("950x750")
        self.root.minsize(850, 700)
        self.root.configure(bg="#f0f0f0")
        
        self.expenses = []
        self.filename = "expenses.json"
        
        # Категории по умолчанию
        self.categories = ["Еда", "Транспорт", "Развлечения", "Здоровье", 
                          "Одежда", "Дом", "Образование", "Другое"]
        
        self.create_widgets()
        self.load_expenses()
    
    def create_widgets(self):
        """Создание элементов интерфейса"""
        
        # Заголовок
        title_label = tk.Label(
            self.root,
            text="?? Expense Tracker",
            font=("Arial", 20, "bold"),
            bg="#f0f0f0",
            fg="#1a1a2e"
        )
        title_label.pack(pady=15)
        
        # Фрейм для добавления расхода
        add_frame = tk.LabelFrame(
            self.root,
            text="Добавить новый расход",
            font=("Arial", 12, "bold"),
            bg="#ffffff",
            padx=15,
            pady=15
        )
        add_frame.pack(fill="x", padx=20, pady=10)
        
        # Сумма
        tk.Label(add_frame, text="Сумма (?):", bg="#ffffff", 
                font=("Arial", 10)).grid(row=0, column=0, sticky="e", pady=5)
        self.entry_amount = tk.Entry(add_frame, width=15, font=("Arial", 10))
        self.entry_amount.grid(row=0, column=1, padx=10, pady=5)
        self.create_tooltip(self.entry_amount, "Введите сумму расхода (положительное число)")
        
        # Категория
        tk.Label(add_frame, text="Категория:", bg="#ffffff", 
                font=("Arial", 10)).grid(row=0, column=2, sticky="e", pady=5)
        self.combo_category = ttk.Combobox(add_frame, width=20, font=("Arial", 10), 
                                           values=self.categories, state="readonly")
        self.combo_category.grid(row=0, column=3, padx=10, pady=5)
        self.combo_category.set("Выберите категорию")
        self.create_tooltip(self.combo_category, "Выберите категорию расхода")
        
        # Дата
        tk.Label(add_frame, text="Дата (ДД.ММ.ГГГГ):", bg="#ffffff", 
                font=("Arial", 10)).grid(row=0, column=4, sticky="e", pady=5)
        self.entry_date = tk.Entry(add_frame, width=15, font=("Arial", 10))
        self.entry_date.grid(row=0, column=5, padx=10, pady=5)
        self.create_tooltip(self.entry_date, "Введите дату в формате ДД.ММ.ГГГГ")
        
        # Описание
        tk.Label(add_frame, text="Описание:", bg="#ffffff", 
                font=("Arial", 10)).grid(row=1, column=0, sticky="e", pady=5)
        self.entry_description = tk.Entry(add_frame, width=50, font=("Arial", 10))
        self.entry_description.grid(row=1, column=1, columnspan=5, padx=10, pady=5, sticky="w")
        self.create_tooltip(self.entry_description, "Необязательно: описание расхода")
        
        # Кнопка добавления
        btn_add = tk.Button(
            add_frame,
            text="? Добавить расход",
            command=self.add_expense,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 11, "bold"),
            width=20,
            height=2
        )
        btn_add.grid(row=2, column=0, columnspan=6, pady=10)
        self.create_tooltip(btn_add, "Добавить расход в таблицу")
        
        # Фрейм для фильтрации и статистики
        filter_frame = tk.LabelFrame(
            self.root,
            text="Фильтрация и статистика",
            font=("Arial", 12, "bold"),
            bg="#ffffff",
            padx=15,
            pady=15
        )
        filter_frame.pack(fill="x", padx=20, pady=10)
        
        # Фильтр по категории
        tk.Label(filter_frame, text="Категория:", bg="#ffffff", 
                font=("Arial", 10)).grid(row=0, column=0, padx=5)
        self.filter_category = ttk.Combobox(filter_frame, width=15, font=("Arial", 10),
                                            values=["Все"] + self.categories, state="readonly")
        self.filter_category.grid(row=0, column=1, padx=5)
        self.filter_category.set("Все")
        self.create_tooltip(self.filter_category, "Фильтр по категории")
        
        # Дата начала
        tk.Label(filter_frame, text="С даты:", bg="#ffffff", 
                font=("Arial", 10)).grid(row=0, column=2, padx=5)
        self.filter_date_from = tk.Entry(filter_frame, width=12, font=("Arial", 10))
        self.filter_date_from.grid(row=0, column=3, padx=5)
        self.filter_date_from.insert(0, "ДД.ММ.ГГГГ")
        self.create_tooltip(self.filter_date_from, "Дата начала периода")
        
        # Дата окончания
        tk.Label(filter_frame, text="По дату:", bg="#ffffff", 
                font=("Arial", 10)).grid(row=0, column=4, padx=5)
        self.filter_date_to = tk.Entry(filter_frame, width=12, font=("Arial", 10))
        self.filter_date_to.grid(row=0, column=5, padx=5)
        self.filter_date_to.insert(0, "ДД.ММ.ГГГГ")
        self.create_tooltip(self.filter_date_to, "Дата окончания периода")
        
        # Кнопки фильтрации
        btn_filter = tk.Button(
            filter_frame,
            text="?? Применить",
            command=self.apply_filter,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10, "bold"),
            width=12
        )
        btn_filter.grid(row=0, column=6, padx=10)
        self.create_tooltip(btn_filter, "Применить фильтры")
        
        btn_reset = tk.Button(
            filter_frame,
            text="?? Сбросить",
            command=self.reset_filter,
            bg="#FF9800",
            fg="white",
            font=("Arial", 10, "bold"),
            width=12
        )
        btn_reset.grid(row=0, column=7, padx=10)
        self.create_tooltip(btn_reset, "Сбросить все фильтры")
        
        # Статистика
        self.label_total = tk.Label(
            filter_frame,
            text="?? Общая сумма: 0 ?",
            font=("Arial", 14, "bold"),
            bg="#e8f5e9",
            fg="#2E7D32",
            padx=20,
            pady=10
        )
        self.label_total.grid(row=1, column=0, columnspan=8, pady=15, sticky="ew")
        
        # Таблица расходов (Treeview)
        table_frame = tk.Frame(self.root, bg="#ffffff")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        columns = ("date", "category", "amount", "description")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)
        
        # Настройка заголовков
        self.tree.heading("date", text="Дата")
        self.tree.heading("category", text="Категория")
        self.tree.heading("amount", text="Сумма (?)")
        self.tree.heading("description", text="Описание")
        
        # Настройка ширины колонок
        self.tree.column("date", width=100, minwidth=80)
        self.tree.column("category", width=120, minwidth=100)
        self.tree.column("amount", width=100, minwidth=80)
        self.tree.column("description", width=300, minwidth=200)
        
        # Полоса прокрутки
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Кнопки управления
        btn_frame = tk.Frame(self.root, bg="#f0f0f0")
        btn_frame.pack(pady=10)
        
        btn_delete = tk.Button(
            btn_frame,
            text="??? Удалить выбранный",
            command=self.delete_expense,
            bg="#f44336",
            fg="white",
            font=("Arial", 10, "bold"),
            width=18,
            height=2
        )
        btn_delete.pack(side="left", padx=5)
        self.create_tooltip(btn_delete, "Удалить выбранный расход")
        
        btn_save = tk.Button(
            btn_frame,
            text="?? Сохранить",
            command=self.save_expenses,
            bg="#9C27B0",
            fg="white",
            font=("Arial", 10, "bold"),
            width=18,
            height=2
        )
        btn_save.pack(side="left", padx=5)
        self.create_tooltip(btn_save, "Сохранить данные в JSON")
        
        btn_export = tk.Button(
            btn_frame,
            text="?? Экспорт отчёта",
            command=self.export_report,
            bg="#00BCD4",
            fg="white",
            font=("Arial", 10, "bold"),
            width=18,
            height=2
        )
        btn_export.pack(side="left", padx=5)
        self.create_tooltip(btn_export, "Экспортировать отчёт в текстовый файл")
        
        # Статус бар
        self.status_label = tk.Label(
            self.root,
            text=f"Всего расходов: 0",
            font=("Arial", 10),
            bg="#1a1a2e",
            fg="white",
            pady=5
        )
        self.status_label.pack(fill="x", side="bottom")
    
    def create_tooltip(self, widget, text):
        """Создание подсказки для виджета"""
        tooltip = tk.Toplevel(widget)
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry("+0+0")
        tooltip.withdraw()
        
        label = tk.Label(
            tooltip,
            text=text,
            background="#ffffe0",
            relief="solid",
            borderwidth=1,
            font=("Arial", 9)
        )
        label.pack()
        
        def show_tooltip(event):
            tooltip.deiconify()
            x = widget.winfo_rootx() + 20
            y = widget.winfo_rooty() + widget.winfo_height() + 5
            tooltip.wm_geometry(f"+{x}+{y}")
        
        def hide_tooltip(event):
            tooltip.withdraw()
        
        widget.bind("<Enter>", show_tooltip)
        widget.bind("<Leave>", hide_tooltip)
    
    def validate_amount(self, amount):
        """Проверка суммы (положительное число)"""
        try:
            value = float(amount)
            if value <= 0:
                messagebox.showerror("Ошибка", "Сумма должна быть положительным числом!")
                return False
            return True
        except ValueError:
            messagebox.showerror("Ошибка", "Сумма должна быть числом!")
            return False
    
    def validate_date(self, date_string):
        """Проверка даты в формате ДД.ММ.ГГГГ"""
        try:
            datetime.strptime(date_string, "%d.%m.%Y")
            return True
        except ValueError:
            messagebox.showerror("Ошибка", "Дата должна быть в формате ДД.ММ.ГГГГ!")
            return False
    
    def validate_category(self, category):
        """Проверка категории"""
        if not category or category == "Выберите категорию":
            messagebox.showerror("Ошибка", "Выберите категорию!")
            return False
        return True
    
    def add_expense(self):
        """Добавление нового расхода"""
        
        amount = self.entry_amount.get().strip()
        category = self.combo_category.get()
        date = self.entry_date.get().strip()
        description = self.entry_description.get().strip()
        
        # Валидация суммы
        if not self.validate_amount(amount):
            return
        
        # Валидация категории
        if not self.validate_category(category):
            return
        
        # Валидация даты
        if not date:
            # Если дата не введена, используем текущую
            date = datetime.now().strftime("%d.%m.%Y")
        
        if not self.validate_date(date):
            return
        
        # Создание записи
        expense = {
            "amount": float(amount),
            "category": category,
            "date": date,
            "description": description if description else "—"
        }
        
        self.expenses.append(expense)
        self.update_table()
        self.save_expenses()
        self.calculate_total()
        
        # Очистка полей
        self.entry_amount.delete(0, tk.END)
        self.combo_category.set("Выберите категорию")
        self.entry_date.delete(0, tk.END)
        self.entry_description.delete(0, tk.END)
        
        messagebox.showinfo("Успех", f"Расход {amount} ? добавлен!")
    
    def delete_expense(self):
        """Удаление выбранного расхода"""
        
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите расход для удаления!")
            return
        
        index = self.tree.index(selected[0])
        expense = self.expenses[index]
        confirm = messagebox.askyesno("Подтверждение", 
                                      f"Удалить расход {expense['amount']} ? ({expense['category']})?")
        
        if confirm:
            self.expenses.pop(index)
            self.update_table()
            self.save_expenses()
            self.calculate_total()
            messagebox.showinfo("Успех", "Расход удалён!")
    
    def apply_filter(self):
        """Применение фильтрации"""
        
        category_filter = self.filter_category.get()
        date_from = self.filter_date_from.get().strip()
        date_to = self.filter_date_to.get().strip()
        
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        filtered = []
        date_from_obj = None
        date_to_obj = None
        
        # Парсинг дат
        if date_from and date_from != "ДД.ММ.ГГГГ":
            if not self.validate_date(date_from):
                return
            date_from_obj = datetime.strptime(date_from, "%d.%m.%Y")
        
        if date_to and date_to != "ДД.ММ.ГГГГ":
            if not self.validate_date(date_to):
                return
            date_to_obj = datetime.strptime(date_to, "%d.%m.%Y")
        
        # Фильтрация
        for expense in self.expenses:
            # Фильтр по категории
            if category_filter and category_filter != "Все":
                if expense["category"] != category_filter:
                    continue
            
            # Фильтр по дате
            expense_date = datetime.strptime(expense["date"], "%d.%m.%Y")
            
            if date_from_obj and expense_date < date_from_obj:
                continue
            
            if date_to_obj and expense_date > date_to_obj:
                continue
            
            filtered.append(expense)
        
        # Вывод отфильтрованных
        for expense in filtered:
            self.tree.insert("", "end", values=(
                expense["date"],
                expense["category"],
                f"{expense['amount']:.2f}",
                expense["description"]
            ))
        
        # Подсчёт суммы
        total = sum(e["amount"] for e in filtered)
        self.label_total.config(text=f"?? Общая сумма: {total:.2f} ?")
        self.status_label.config(text=f"Показано: {len(filtered)} из {len(self.expenses)}")
    
    def reset_filter(self):
        """Сброс фильтров"""
        
        self.filter_category.set("Все")
        self.filter_date_from.delete(0, tk.END)
        self.filter_date_from.insert(0, "ДД.ММ.ГГГГ")
        self.filter_date_to.delete(0, tk.END)
        self.filter_date_to.insert(0, "ДД.ММ.ГГГГ")
        
        self.update_table()
    
    def calculate_total(self):
        """Подсчёт общей суммы расходов"""
        
        total = sum(e["amount"] for e in self.expenses)
        self.label_total.config(text=f"?? Общая сумма: {total:.2f} ?")
    
    def update_table(self):
        """Обновление таблицы расходов"""
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for expense in self.expenses:
            self.tree.insert("", "end", values=(
                expense["date"],
                expense["category"],
                f"{expense['amount']:.2f}",
                expense["description"]
            ))
        
        self.calculate_total()
        self.status_label.config(text=f"Всего расходов: {len(self.expenses)}")
    
    def save_expenses(self):
        """Сохранение расходов в JSON"""
        
        try:
            with open(self.filename, "w", encoding="utf-8") as file:
                json.dump(self.expenses, file, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить: {e}")
    
    def load_expenses(self):
        """Загрузка расходов из JSON"""
        
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as file:
                    self.expenses = json.load(file)
                self.update_table()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить: {e}")
                self.expenses = []
    
    def export_report(self):
        """Экспорт отчёта в текстовый файл"""
        
        if not self.expenses:
            messagebox.showwarning("Внимание", "Нет расходов для экспорта!")
            return
        
        try:
            with open("expense_report.txt", "w", encoding="utf-8") as file:
                file.write("=" * 60 + "\n")
                file.write("?? EXPENSE TRACKER — ОТЧЁТ ПО РАСХОДАМ\n")
                file.write("=" * 60 + "\n\n")
                
                total = sum(e["amount"] for e in self.expenses)
                
                file.write(f"Всего расходов: {len(self.expenses)}\n")
                file.write(f"Общая сумма: {total:.2f} ?\n\n")
                file.write("-" * 60 + "\n\n")
                
                # Группировка по категориям
                categories = {}
                for expense in self.expenses:
                    cat = expense["category"]
                    if cat not in categories:
                        categories[cat] = 0
                    categories[cat] += expense["amount"]
                
                file.write("?? ПО КАТЕГОРИЯМ:\n\n")
                for cat, amount in sorted(categories.items(), key=lambda x: x[1], reverse=True):
                    file.write(f"  {cat}: {amount:.2f} ?\n")
                
                file.write("\n" + "-" * 60 + "\n\n")
                file.write("?? ВСЕ РАСХОДЫ:\n\n")
                
                for expense in self.expenses:
                    file.write(f"  {expense['date']} | {expense['category']:15} | "
                              f"{expense['amount']:>10.2f} ? | {expense['description']}\n")
                
                file.write("\n" + "=" * 60 + "\n")
            
            messagebox.showinfo("Успех", "Отчёт экспортирован в expense_report.txt!")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось экспортировать: {e}")


# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
