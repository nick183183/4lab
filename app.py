from flask import Flask, render_template, request
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
from scipy.integrate import odeint

app = Flask(__name__)

# Система дифференциальных уравнений (пример)
def kolmogorov_chepman_system(y, t, lambdas, mus):
    dydt = [
        -lambdas[0] * y[0] + mus[0] * y[1],
        lambdas[1] * y[0] - mus[1] * y[1]
    ]
    return dydt

@app.route("/", methods=["GET", "POST"])
def index():
    graph_url = None
    lambda_values = []
    mu_values = []
    
    if request.method == "POST":
        # Получение значений из формы
        for i in range(6):
            try:
                lambda_values.append(float(request.form[f"lambda_{i}"]))
                mu_values.append(float(request.form[f"mu_{i}"]))
            except ValueError:
                lambda_values.append(0)  # Если не удалось конвертировать в число, ставим 0
                mu_values.append(0)
        
        # Начальные условия
        y0 = [1, 0]  # Начальные значения для y1 и y2
        t = np.linspace(0, 10, 100)  # Временной интервал
        
        # Пример использования полученных значений lambda и mu для построения графиков
        plt.figure(figsize=(10, 8))
        
        for i in range(6):
            # Решение системы для каждой пары lambda и mu
            solution = odeint(kolmogorov_chepman_system, y0, t, args=([lambda_values[i], lambda_values[i]], [mu_values[i], mu_values[i]]))
            
            # Построение графиков для каждого значения
            plt.plot(t, solution[:, 0], label=f"λ{i+1}, μ{i+1} - y1")
            plt.plot(t, solution[:, 1], label=f"λ{i+1}, μ{i+1} - y2")
        
        plt.xlabel("Время")
        plt.ylabel("Вероятности")
        plt.title("Оценка вероятностей (Колмогоров-Чепмен)")
        plt.legend()
        plt.grid()

        # Сохранение графика в буфер
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        graph_url = base64.b64encode(buf.getvalue()).decode('utf-8')
        buf.close()
        plt.close()

    return render_template("index.html", graph_url=graph_url, lambda_values=lambda_values, mu_values=mu_values)

if __name__ == "__main__":
    
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
