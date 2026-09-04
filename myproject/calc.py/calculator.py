import tkinter as tk
from tkinter import messagebox

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Калькулятор")
        self.root.geometry("300x400")
        self.root.resizable(False, False) # Запрещаем менять размер окна, чтобы сетка не плыла
        
        # Переменная для хранения выражения
        self.expression = ""
        
        # Создание поля ввода
        self.entry = tk.Entry(root, font=('Arial', 20), 
                              justify='right', bd=5, relief='ridge')
        self.entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
        
        # Список кнопок в порядке их отображения в сетке
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            'C', '0', '=', '+'
        ]
        
        row_val = 1
        col_val = 0
        
        # Настройка адаптивности сетки (чтобы кнопки растягивались аккуратно)
        for i in range(4):
            root.grid_columnconfigure(i, weight=1)
        for i in range(5):
            root.grid_rowconfigure(i, weight=1)
        
        # Цикл для создания и размещения кнопок
        for button in buttons:
            # Используем lambda, чтобы передать конкретный символ кнопки в метод click_event
            action = lambda x=button: self.click_event(x)
            
            tk.Button(root, text=button, font=('Arial', 15),
                      bd=3, relief='ridge', command=action).grid(row=row_val, column=col_val, sticky="nsew", padx=2, pady=2)
            
            col_val += 1
            if col_val > 3:
                col_val = 0
                row_val += 1
 
    def click_event(self, key):
        if key == '=':
            try:
                # eval вычисляет строку как математическое выражение
                result = str(eval(self.expression))
                
                # Полностью очищаем поле ввода перед показом результата
                self.entry.delete(0, tk.END)
                self.entry.insert(0, result)
                
                # Записываем результат в выражение, чтобы можно было продолжить считать дальше
                self.expression = result
            except ZeroDivisionError:
                messagebox.showerror("Ошибка", "Деление на ноль невозможно")
                self.clear_fields()
            except Exception:
                messagebox.showerror("Ошибка", "Неверное выражение")
                self.clear_fields()
                
        elif key == 'C':
            self.clear_fields()
            
        else:
            # Добавляем символ к текущему выражению
            self.expression += str(key)
            # Обновляем поле ввода, чтобы всё отображалось корректно
            self.entry.delete(0, tk.END)
            self.entry.insert(0, self.expression)

    def clear_fields(self):
        """Вспомогательный метод для полной очистки поля и памяти калькулятора"""
        self.expression = ""
        self.entry.delete(0, tk.END)
 
if __name__ == "__main__":
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()