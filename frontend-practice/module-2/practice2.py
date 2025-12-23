import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

sns.set_style("whitegrid")
plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["figure.dpi"] = 100

np.random.seed(42)

n_students = 25
students = [f"Ученик_{i}" for i in range(1, n_students + 1)]
subjects = ["Математика", "Английский", "Физика", "Информатика", "История"]

data = {"Ученик": students}
for subject in subjects:
    data[subject] = np.random.randint(3, 6, n_students)

df = pd.DataFrame(data)
df["Средний_балл"] = df[subjects].mean(axis=1).round(2)

quarters_data = pd.DataFrame({
    "Четверть": ["1 четв.", "2 четв.", "3 четв.", "4 четв."],
    "Средний_балл": [3.9, 4.0, 4.2, 4.3]
})

fig = plt.figure(figsize=(20, 12))
fig.suptitle(
    "ДАШБОРД УСПЕВАЕМОСТИ КЛАССА",
    fontsize=24,
    fontweight="bold",
    y=0.98
)

ax1 = plt.subplot(3, 3, 1)

subject_means = df[subjects].mean().sort_values(ascending=False)
colors = plt.cm.viridis(np.linspace(0, 1, len(subjects)))

bars = ax1.bar(
    subject_means.index,
    subject_means.values,
    color=colors,
    edgecolor="black"
)

ax1.set_title("Средние баллы по предметам", fontsize=12, fontweight="bold")
ax1.set_ylabel("Средний балл", fontsize=11, fontweight="bold")
ax1.set_ylim(0, 5)
ax1.grid(axis="y", alpha=0.3)

for bar in bars:
    height = bar.get_height()
    ax1.text(
        bar.get_x() + bar.get_width() / 2,
        height + 0.05,
        f"{height:.2f}",
        ha="center",
        va="bottom",
        fontsize=10,
        fontweight="bold"
    )

plt.setp(ax1.get_xticklabels(), rotation=45, ha="right")

ax2 = plt.subplot(3, 3, 2)

all_grades = pd.concat([df[s] for s in subjects])
grade_counts = all_grades.value_counts().sort_index()

ax2.pie(
    grade_counts.values,
    labels=[str(int(g)) for g in grade_counts.index],
    autopct="%1.1f%%",
    startangle=90,
    explode=[0.05] * len(grade_counts),
    textprops={"fontsize": 11, "fontweight": "bold"}
)

ax2.set_title("Распределение оценок", fontsize=12, fontweight="bold")

ax3 = plt.subplot(3, 3, 3)

top10 = df.nlargest(10, "Средний_балл")
colors_top = plt.cm.RdYlGn(np.linspace(0.3, 1, len(top10)))

ax3.barh(
    top10["Ученик"],
    top10["Средний_балл"],
    color=colors_top,
    edgecolor="black"
)

ax3.set_title("Топ-10 лучших учеников", fontsize=12, fontweight="bold")
ax3.set_xlabel("Средний балл", fontsize=11, fontweight="bold")
ax3.invert_yaxis()
ax3.grid(axis="x", alpha=0.3)

for i, value in enumerate(top10["Средний_балл"]):
    ax3.text(
        value + 0.05,
        i,
        f"{value:.2f}",
        va="center",
        fontsize=9,
        fontweight="bold"
    )

ax4 = plt.subplot(3, 3, (4, 6))

heatmap_data = df.set_index("Ученик")[subjects]

sns.heatmap(
    heatmap_data,
    annot=True,
    fmt=".0f",
    cmap="RdYlGn",
    vmin=2,
    vmax=5,
    linewidths=0.5,
    linecolor="gray",
    cbar_kws={"label": "Оценка"},
    ax=ax4
)

ax4.set_title("Оценки учеников по предметам", fontsize=12, fontweight="bold")
ax4.set_xlabel("Предмет", fontsize=11, fontweight="bold")
ax4.set_ylabel("Ученик", fontsize=11, fontweight="bold")

ax5 = plt.subplot(3, 3, 7)

ax5.plot(
    quarters_data["Четверть"],
    quarters_data["Средний_балл"],
    marker="o",
    linewidth=3,
    markersize=10
)

ax5.set_title("Динамика успеваемости по четвертям", fontsize=12, fontweight="bold")
ax5.set_ylabel("Средний балл класса", fontsize=11, fontweight="bold")
ax5.set_ylim(3.5, 4.5)
ax5.grid(True, alpha=0.3)

for i, row in quarters_data.iterrows():
    ax5.text(
        i,
        row["Средний_балл"] + 0.05,
        f"{row['Средний_балл']:.1f}",
        ha="center",
        fontsize=10,
        fontweight="bold"
    )

ax6 = plt.subplot(3, 3, 8)

df_melted = df[subjects].melt(var_name="Предмет", value_name="Балл")

sns.boxplot(
    x="Предмет",
    y="Балл",
    data=df_melted,
    palette="Set2",
    ax=ax6
)

ax6.set_title("Разброс оценок по предметам", fontsize=12, fontweight="bold")
ax6.set_xlabel("Предмет", fontsize=11, fontweight="bold")
ax6.set_ylabel("Балл", fontsize=11, fontweight="bold")
ax6.grid(axis="y", alpha=0.3)

plt.setp(ax6.get_xticklabels(), rotation=45, ha="right")

ax7 = plt.subplot(3, 3, 9)
ax7.axis("off")

subject_means = df[subjects].mean()
best_subject = subject_means.idxmax()
worst_subject = subject_means.idxmin()

stats_text = f"""
Всего учеников: {len(df)}

Средний балл: {df['Средний_балл'].mean():.2f}
Медиана: {df['Средний_балл'].median():.2f}

РАСПРЕДЕЛЕНИЕ:
  Отличники (≥4.5): {(df['Средний_балл'] >= 4.5).sum()}
  Хорошисты (≥3.5): {((df['Средний_балл'] >= 3.5) & (df['Средний_балл'] < 4.5)).sum()}
  Троечники (<3.5): {(df['Средний_балл'] < 3.5).sum()}

ПРЕДМЕТЫ:
  Лучший: {best_subject} ({subject_means[best_subject]:.2f})
  Сложный: {worst_subject} ({subject_means[worst_subject]:.2f})

Дата: {datetime.now().strftime('%d.%m.%Y')}
"""

ax7.text(
    0.02,
    0.98,
    stats_text,
    transform=ax7.transAxes,
    fontsize=11,
    fontfamily="monospace",
    verticalalignment="top",
    bbox=dict(boxstyle="round", facecolor="lightblue", alpha=0.8)
)

plt.tight_layout()
plt.savefig("dashboard.png", dpi=300, bbox_inches="tight")
print("Дашборд успешно сохранён в файл dashboard.png")
plt.show()