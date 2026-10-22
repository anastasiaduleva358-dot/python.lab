import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt

from flask import Flask, render_template, request

app = Flask(__name__)

# путь к CSV
FILE_PATH = 'data/Ecommerce_Sales_Data_2024_2025.csv'


@app.route('/')
def index():

    #проверка существования файла
    if not os.path.exists(FILE_PATH):
        return "CSV файл не найден!"

    #чтение CSV
    df = pd.read_csv(FILE_PATH)

    #удаление пропущенных значений
    df = df.dropna()

    
    #проверяем названия колонок

    print(df.columns)

    # вычисление общей стоимости заказа
    df['Total_Price'] = df['Quantity'] * df['Unit Price']

    # общее количество заказов
    total_orders = len(df)

    # общий доход
    total_revenue = df['Total_Price'].sum()

    # самый продаваемый товар
    best_selling_product = (
        df.groupby('Product Name')['Quantity']
        .sum()
        .idxmax()
    )

    #категория с наибольшими продажами
    best_category = (
        df.groupby('Category')['Total_Price']
        .sum()
        .idxmax()
    )

    #Город с наибольшим количеством заказов
    top_city = (
        df['City']
        .value_counts()
        .idxmax()
    )

    # фильтрация по городу
    selected_city = request.args.get('city')

    if selected_city and selected_city != 'All':
        filtered_df = df[df['City'] == selected_city]
    else:
        filtered_df = df

    #список городов
    cities = sorted(df['City'].unique())

    #сводная таблица
    category_summary = (
        df.groupby('Category')['Total_Price']
        .sum()
        .reset_index()
    )

    # ГРАФИК

    plt.figure(figsize=(8, 5))
    plt.bar(
        category_summary['Category'],
        category_summary['Total_Price']
    )

    plt.xticks(rotation=45)
    plt.title('Sales by Category')
    plt.tight_layout()

    chart_path = 'static/chart.png'

    plt.savefig(chart_path)
    plt.close()

    # таблица заказов
    orders = filtered_df.to_dict(orient='records')

    # сводная таблица
    summary = category_summary.to_dict(orient='records')


    return render_template(
        'index.html',
        total_orders=total_orders,
        total_revenue=round(total_revenue, 2),
        best_selling_product=best_selling_product,
        best_category=best_category,
        top_city=top_city,
        orders=orders,
        summary=summary,
        cities=cities,
        selected_city=selected_city
    )


if __name__ == '__main__':
    app.run(debug=True)