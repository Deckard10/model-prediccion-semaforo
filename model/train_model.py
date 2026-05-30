import pandas as pd
import joblib
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)

# ==========================================
# CARGA DEL DATASET
# ==========================================

print("Cargando dataset...")

df = pd.read_excel('dataset/Data.xlsx')

print("\nPrimeras filas del dataset:\n")
print(df.head())


# ==========================================
# PREPROCESAMIENTO DE DATOS
# ==========================================

print("\nPreprocesando datos...")

# Convertir día a número

dias = {
    'Monday': 1,
    'Tuesday': 2,
    'Wednesday': 3,
    'Thursday': 4,
    'Friday': 5,
    'Saturday': 6,
    'Sunday': 7
}

df['DayNumber'] = df['Day of the week'].map(dias)

# Convertir hora de texto a datetime
df['Tiempo'] = pd.to_datetime(
    df['Tiempo'],
    format='%I:%M:%S %p'
)

# Extraer hora
df['Hour'] = df['Tiempo'].dt.hour

# ==========================================
# VARIABLES DE ENTRADA
# ==========================================

X = df[
    [
        'CarCount',
        'BikeCount',
        'BusCount',
        'TruckCount',
        'Hour',
        'DayNumber'
    ]
]

# ==========================================
# VARIABLE OBJETIVO
# ==========================================

y = df['Traffic Situation']

# ==========================================
# DIVISIÓN DE DATOS
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# ==========================================
# MODELO RANDOM FOREST
# ==========================================

print("\nEntrenando modelo...")

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# ==========================================
# PREDICCIONES
# ==========================================

y_pred = model.predict(X_test)

# ==========================================
# EVALUACIÓN
# ==========================================

accuracy = accuracy_score(y_test, y_pred)

print("\n==============================")
print("RESULTADOS DEL MODELO")
print("==============================")

print(f"\nAccuracy: {accuracy:.2%}")

# ==========================================
# REPORTE DE CLASIFICACIÓN
# ==========================================

print("\nReporte de Clasificación:\n")

report = classification_report(
    y_test,
    y_pred
)

print(report)

# ==========================================
# MATRIZ DE CONFUSIÓN
# ==========================================

print("\nMatriz de Confusión:\n")

cm = confusion_matrix(
    y_test,
    y_pred
)

print(cm)

# Guardar matriz de confusión

disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=model.classes_
)

disp.plot()

plt.title("Matriz de Confusión")

plt.savefig(
    "model/confusion_matrix.png",
    bbox_inches="tight"
)

plt.close()

print("\nMatriz de confusión guardada.")

# ==========================================
# IMPORTANCIA DE VARIABLES
# ==========================================

importance = pd.DataFrame({

    'Variable': X.columns,

    'Importancia': model.feature_importances_

})

importance = importance.sort_values(
    by='Importancia',
    ascending=False
)

print("\nImportancia de Variables:\n")

print(importance)

# Guardar CSV

importance.to_csv(
    'model/feature_importance.csv',
    index=False
)

# Gráfico de importancia

plt.figure(figsize=(8,5))

plt.bar(
    importance['Variable'],
    importance['Importancia']
)

plt.title('Importancia de Variables')
plt.xlabel('Variables')
plt.ylabel('Importancia')

plt.savefig(
    'model/feature_importance.png',
    bbox_inches='tight'
)

plt.close()

print("\nGráfico de importancia guardado.")

# ==========================================
# GUARDAR RESULTADOS
# ==========================================

with open(
    "model/resultados.txt",
    "w",
    encoding="utf-8"
) as f:

    f.write("RESULTADOS DEL MODELO\n")
    f.write("=====================\n\n")

    f.write(f"Accuracy: {accuracy:.2%}\n\n")

    f.write("Reporte de Clasificación\n")
    f.write("-------------------------\n")

    f.write(report)

print("\nResultados guardados.")

# ==========================================
# GUARDAR MODELO
# ==========================================

joblib.dump(
    model,
    'model/semaforo_model.pkl'
)

print("\nModelo guardado correctamente.")

print("\n==============================")
print("PROCESO FINALIZADO")
print("==============================")