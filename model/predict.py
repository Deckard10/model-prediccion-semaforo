import pandas as pd
import joblib

# ==========================================
# CARGAR MODELO
# ==========================================

model = joblib.load("semaforo_model.pkl")

# ==========================================
# NUEVO DATO
# ==========================================
nuevo_dato = pd.DataFrame([{
    "CarCount": 20,
    "BikeCount": 5,
    "BusCount": 3,
    "TruckCount": 2,
    "Hour": 10,
    "DayNumber": 3
}])

# PREDICCIÓN
resultado = model.predict(nuevo_dato)[0]


print("\nNivel de tráfico:", resultado)

# TIEMPO DE VERDE PARA DESCONGESTIÓN

if resultado.lower() == "low":
    tiempo_verde = 20   # poco tráfico

elif resultado.lower() == "normal":
    tiempo_verde = 40   # tráfico medio

elif resultado.lower() == "high":
    tiempo_verde = 80   # tráfico alto

else:
    tiempo_verde = 30   # default

# SALIDA FINAL

print("\nOPTIMIZACIÓN DE SEMÁFORO")
print("===========================")
print("Tiempo de luz verde:", tiempo_verde, "segundos")
