import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from tkinter import *
from tkinter import filedialog, messagebox
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def load_journal(filename):
    try:
        return pd.read_csv(filename)
    except FileNotFoundError:
        return None


def calculate_statistics(df):
    subjects = [c for c in df.columns if c != 'Ученик']
    df['Средний_балл'] = df[subjects].mean(axis=1).round(2)

    def status(avg):
        if avg >= 4.5:
            return 'Отличник'
        elif avg >= 3.5:
            return 'Хорошист'
        elif avg >= 2.5:
            return 'Троечник'
        else:
            return 'Требует внимания'

    df['Статус'] = df['Средний_балл'].apply(status)
    return df, subjects


def quarter_dynamics(df):
    return pd.DataFrame({
        '1 четверть': df['Средний_балл'],
        '2 четверть': df['Средний_балл'] + np.random.uniform(-0.3, 0.3, len(df)),
        '3 четверть': df['Средний_балл'] + np.random.uniform(-0.3, 0.3, len(df)),
        '4 четверть': df['Средний_балл'] + np.random.uniform(-0.3, 0.3, len(df))
    }, index=df['Ученик'])


def generate_recommendations(df):
    result = {}
    for _, row in df.iterrows():
        if row['Средний_балл'] < 3.5:
            result[row['Ученик']] = (
                "Рекомендуется усилить подготовку и посещать консультации."
            )
        elif row['Средний_балл'] < 4.5:
            result[row['Ученик']] = (
                "Хороший уровень. Рекомендуется закрепить знания."
            )
        else:
            result[row['Ученик']] = (
                "Отличный результат. Рекомендуется участие в олимпиадах."
            )
    return result


def visualize(df, subjects):
    plt.figure()
    df['Статус'].value_counts().plot(kind='bar')
    plt.title('Распределение учеников по статусам')
    plt.ylabel('Количество')
    plt.show()

    plt.figure()
    df[subjects].mean().plot(kind='bar')
    plt.title('Средний балл по предметам')
    plt.ylabel('Средний балл')
    plt.show()


def export_pdf(df, recommendations, filename='report.pdf'):
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(filename)
    content = []

    content.append(Paragraph("ОТЧЁТ ПО УСПЕВАЕМОСТИ", styles['Title']))
    content.append(Paragraph(
        f"Дата: {datetime.now().strftime('%d.%m.%Y %H:%M')}",
        styles['Normal']
    ))

    for _, row in df.iterrows():
        content.append(Paragraph(
            f"{row['Ученик']}: {row['Средний_балл']} ({row['Статус']})",
            styles['Normal']
        ))
        content.append(Paragraph(
            f"Рекомендация: {recommendations[row['Ученик']]}",
            styles['Italic']
        ))

    doc.build(content)


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Анализ успеваемости")
        self.root.geometry("720x520")
        self.root.resizable(False, False)

        self.df = None
        self.subjects = None

        font_title = ("Segoe UI", 16, "bold")
        font_btn = ("Segoe UI", 11)
        font_text = ("Consolas", 10)

        Label(root, text="Система анализа успеваемости", font=font_title).pack(pady=10)

        top = Frame(root)
        top.pack(pady=5)

        Button(top, text="Загрузить CSV", width=18, font=font_btn, command=self.load).grid(row=0, column=0, padx=5)
        Button(top, text="Графики", width=18, font=font_btn, command=self.show_plots).grid(row=0, column=1, padx=5)
        Button(top, text="Экспорт PDF", width=18, font=font_btn, command=self.save_pdf).grid(row=0, column=2, padx=5)

        frame_text = Frame(root)
        frame_text.pack(padx=10, pady=10, fill=BOTH, expand=True)

        scrollbar = Scrollbar(frame_text)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.text = Text(
            frame_text,
            font=font_text,
            yscrollcommand=scrollbar.set,
            wrap=WORD
        )
        self.text.pack(fill=BOTH, expand=True)
        scrollbar.config(command=self.text.yview)

    def load(self):
        file = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not file:
            return

        self.df = load_journal(file)
        if self.df is None:
            messagebox.showerror("Ошибка", "Файл не найден")
            return

        self.df, self.subjects = calculate_statistics(self.df)
        recs = generate_recommendations(self.df)

        self.text.delete(1.0, END)
        for _, row in self.df.iterrows():
            self.text.insert(
                END,
                f"{row['Ученик']}\n"
                f"Средний балл: {row['Средний_балл']} ({row['Статус']})\n"
                f"Рекомендация: {recs[row['Ученик']]}\n\n"
            )

    def show_plots(self):
        if self.df is not None:
            visualize(self.df, self.subjects)

    def save_pdf(self):
        if self.df is None:
            return
        recs = generate_recommendations(self.df)
        export_pdf(self.df, recs)
        messagebox.showinfo("Готово", "PDF-отчёт сохранён")


if __name__ == "__main__":
    root = Tk()
    App(root)
    root.mainloop()