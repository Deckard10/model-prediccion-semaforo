import joblib

model = joblib.load('model/semaforo_model.pkl')



# 'CarCount', 'BikeCount', 'BusCount', 'TruckCount', 'Total'
nuevo_trafico = [[120, 20, 10, 5, 155]]
resultado = model.predict(nuevo_trafico)[0]

print("Nivel de tráfico: ", resultado)

# Decisión semafórica

if resultado == 'low':
    green_time = 30

elif resultado == 'normal':
    green_time = 60

elif resultado == 'high':
    green_time = 90

else: 
    green_time = 120

print("Tiempo de luz verde recomendado: ", green_time)