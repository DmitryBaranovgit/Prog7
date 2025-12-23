import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

def analyze(results_df, info_df):
    tasks = [c for c in results_df.columns if c.startswith('Задание_')]
    results_df['Общий_балл'] = results_df[tasks].sum(axis=1)
    results_df['Процент'] = (results_df['Общий_балл'] / len(tasks) * 100).round(1)

    stats = []
    for t in tasks:
        stats.append({
            'Задание': t,
            'Правильных_ответов': results_df[t].sum(),
            'Всего_учеников': len(results_df),
            'Процент_правильных': results_df[t].mean() * 100
        })

    task_df = pd.DataFrame(stats).merge(info_df, on='Задание')
    topic_df = task_df.groupby('Тема')['Процент_правильных'].mean().reset_index()
    topic_df = topic_df.rename(columns={'Процент_правильных':'Средний_процент'}).sort_values('Средний_процент')
    return results_df, task_df, topic_df

def visualize(results_df, task_df, topic_df):
    fig = plt.figure(figsize=(18,12))
    fig.suptitle('АНАЛИЗ РЕЗУЛЬТАТОВ ТЕСТИРОВАНИЯ', fontsize=20, fontweight='bold', y=0.98)

    ax1 = plt.subplot(3,3,1)
    ax1.hist(results_df['Процент'], bins=10, color='skyblue', edgecolor='black', alpha=0.7)
    ax1.axvline(results_df['Процент'].mean(), color='red', linestyle='--', linewidth=2, 
                label=f'Среднее: {results_df["Процент"].mean():.1f}%')
    ax1.set_title('Распределение результатов')
    ax1.set_xlabel('Процент')
    ax1.set_ylabel('Количество учеников')
    ax1.legend()
    ax1.grid(axis='y', alpha=0.3)

    ax2 = plt.subplot(3,3,(2,3))
    colors = ['green' if x>=70 else 'orange' if x>=50 else 'red' for x in task_df['Процент_правильных']]
    bars = ax2.barh(task_df['Задание'], task_df['Процент_правильных'], color=colors, alpha=0.7)
    ax2.axvline(60, color='black', linestyle='--', linewidth=2, label='Порог 60%')
    ax2.set_xlabel('Процент правильных')
    ax2.set_title('Успеваемость по заданиям')
    ax2.legend()
    ax2.grid(axis='x', alpha=0.3)
    for bar, val in zip(bars, task_df['Процент_правильных']):
        ax2.text(val+1, bar.get_y()+bar.get_height()/2, f'{val:.0f}%', va='center', fontsize=8, fontweight='bold')

    ax3 = plt.subplot(3,3,4)
    colors_topics = ['red' if x<60 else 'orange' if x<70 else 'green' for x in topic_df['Средний_процент']]
    bars = ax3.barh(topic_df['Тема'], topic_df['Средний_процент'], color=colors_topics, alpha=0.7)
    ax3.axvline(60, color='black', linestyle='--', linewidth=2)
    ax3.set_xlabel('Средний % правильных')
    ax3.set_title('Успеваемость по темам')
    ax3.grid(axis='x', alpha=0.3)
    for bar, val in zip(bars, topic_df['Средний_процент']):
        ax3.text(val+1, bar.get_y()+bar.get_height()/2, f'{val:.0f}%', va='center', fontweight='bold')

    ax4 = plt.subplot(3,3,5)
    top5 = results_df.nlargest(5,'Процент')[['Ученик','Процент']]
    bottom5 = results_df.nsmallest(5,'Процент')[['Ученик','Процент']]
    combined = pd.concat([top5,bottom5])
    colors_students = ['green']*5 + ['red']*5
    ax4.barh(range(len(combined)), combined['Процент'].values, color=colors_students, alpha=0.7)
    ax4.set_yticks(range(len(combined)))
    ax4.set_yticklabels(combined['Ученик'].values, fontsize=8)
    ax4.set_xlabel('Процент')
    ax4.set_title('Топ-5 и аутсайдеры')
    ax4.invert_yaxis()
    ax4.grid(axis='x', alpha=0.3)
    ax4.axhline(y=4.5, color='black', linestyle='-', linewidth=2)

    ax5 = plt.subplot(3,3,6)
    sns.boxplot(x='Сложность', y='Процент_правильных', data=task_df,
                palette='Set2', ax=ax5, order=['Легко','Средне','Сложно'])
    ax5.set_ylabel('Процент правильных')
    ax5.set_xlabel('Уровень сложности')
    ax5.set_title('Успеваемость по уровням')
    ax5.grid(axis='y', alpha=0.3)

    ax6 = plt.subplot(3,3,(7,9))
    question_cols = [c for c in results_df.columns if c.startswith('Задание_')]
    sns.heatmap(results_df.set_index('Ученик')[question_cols], annot=False,
                cmap='RdYlGn', vmin=0, vmax=1, linewidths=0.5, linecolor='gray', ax=ax6)
    ax6.set_title('Результаты всех учеников по заданиям')
    ax6.set_xlabel('Задание')
    ax6.set_ylabel('Ученик')

    plt.tight_layout()
    plt.savefig('test_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

def report(results_df, task_df, topic_df):
    with open('test_report.txt', 'w', encoding='utf-8') as f:
        f.write('АНАЛИТИЧЕСКИЙ ОТЧЁТ ПО РЕЗУЛЬТАТАМ КОНТРОЛЬНОЙ РАБОТЫ\n')
        f.write(f"Дата: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n")
        f.write('\n\n')
        f.write(f"Количество учеников: {len(results_df)}\n")
        f.write(f"Количество заданий: {len([c for c in results_df.columns if c.startswith('Задание_')])}\n")
        f.write(f"Средний результат: {results_df['Процент'].mean():.1f}%\n")
        f.write(f"Лучший результат: {results_df['Процент'].max():.1f}%\n")
        f.write(f"Худший результат: {results_df['Процент'].min():.1f}%\n\n")
        f.write('Проблемные задания (<60%):\n')
        for _, r in task_df[task_df['Процент_правильных']<60].iterrows():
            f.write(f"{r['Задание']} ({r['Тема']}) {r['Процент_правильных']:.0f}%\n")
        f.write('\nПроблемные темы (<60%):\n')
        for _, r in topic_df[topic_df['Средний_процент']<60].iterrows():
            f.write(f"{r['Тема']} {r['Средний_процент']:.0f}%\n")
        f.write('\nУченики группы риска (<50%):\n')
        for _, r in results_df[results_df['Процент']<50].iterrows():
            f.write(f"{r['Ученик']} {r['Процент']:.1f}%\n")

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    results = pd.read_csv(os.path.join(base_dir,'test_results.csv'))
    info = pd.read_csv(os.path.join(base_dir,'test_info.csv'))

    results_df, task_df, topic_df = analyze(results, info)
    visualize(results_df, task_df, topic_df)
    report(results_df, task_df, topic_df)

    with pd.ExcelWriter('test_analysis.xlsx') as writer:
        results_df.to_excel(writer, sheet_name='Ученики', index=False)
        task_df.to_excel(writer, sheet_name='Задания', index=False)
        topic_df.to_excel(writer, sheet_name='Темы', index=False)

if __name__ == '__main__':
    main()