import streamlit as st
import pandas as pd
import joblib

# Cargar modelo
modelo = joblib.load('modelo_random_forest.pkl')

st.title("Predicción de días de hospitalización")
st.write("Ingrese los datos del paciente:")

# =========================
# INPUTS
# =========================

edad = st.number_input("Edad", min_value=0, max_value=120, value=30)

# Via ingreso (solo existe _3)
via_ingreso = st.selectbox("Tipo de ingreso", [
    "No es tipo 3",
    "Tipo 3"
])

# Sexo
sexo = st.selectbox("Sexo", [
    "Femenino",
    "Masculino"
])

# Causa externa (solo tienes 12, 13, 15 → sin base)
causa = st.selectbox("Causa externa", [
    "Otra",
    "12",
    "13",
    "15"
])

# Tipo usuario (base = Tipo 1)
tipo_usuario = st.selectbox("Tipo de usuario", [
    "Tipo 1",
    "Tipo 2",
    "Tipo 3",
    "Tipo 4"
])

# Grupo CIE10
grupo = st.selectbox("Grupo diagnóstico", [
    "Otro",
    "Circulatorio",
    "Congénitas",
    "Embarazo",
    "Infecciosas",
    "Mentales",
    "Musculoesquelético",
    "Respiratorio",
    "Sentidos",
    "Tumores"
])

# =========================
# PREDICCIÓN
# =========================

if st.button("Predecir"):

    data = {
        'edad_anios': edad,

        # Via ingreso
        'ViaIngreso_3': True if via_ingreso == "Tipo 3" else False,

        # Causa externa
        'CausaExterna_12': False,
        'CausaExterna_13': False,
        'CausaExterna_15': False,

        # Tipo usuario
        'TipoUsuario_2': False,
        'TipoUsuario_3': False,
        'TipoUsuario_4': False,

        # Sexo
        'Sexo_M': True if sexo == "Masculino" else False,

        # Grupos
        'grupo_cie10_Circulatorio': False,
        'grupo_cie10_Congénitas': False,
        'grupo_cie10_Embarazo': False,
        'grupo_cie10_Infecciosas y parasitarias': False,
        'grupo_cie10_Mentales': False,
        'grupo_cie10_Musculoesquelético': False,
        'grupo_cie10_Respiratorio': False,
        'grupo_cie10_Sentidos (ojo/oído)': False,
        'grupo_cie10_Tumores': False
    }

    # =========================
    # ACTIVAR VARIABLES
    # =========================

    # Causa externa
    if causa == "12":
        data['CausaExterna_12'] = True
    elif causa == "13":
        data['CausaExterna_13'] = True
    elif causa == "15":
        data['CausaExterna_15'] = True
    # "Otra" → todas False

    # Tipo usuario
    if tipo_usuario == "Tipo 2":
        data['TipoUsuario_2'] = True
    elif tipo_usuario == "Tipo 3":
        data['TipoUsuario_3'] = True
    elif tipo_usuario == "Tipo 4":
        data['TipoUsuario_4'] = True
    # Tipo 1 → todas False

    # Grupo CIE10
    if grupo == "Circulatorio":
        data['grupo_cie10_Circulatorio'] = True
    elif grupo == "Congénitas":
        data['grupo_cie10_Congénitas'] = True
    elif grupo == "Embarazo":
        data['grupo_cie10_Embarazo'] = True
    elif grupo == "Infecciosas":
        data['grupo_cie10_Infecciosas y parasitarias'] = True
    elif grupo == "Mentales":
        data['grupo_cie10_Mentales'] = True
    elif grupo == "Musculoesquelético":
        data['grupo_cie10_Musculoesquelético'] = True
    elif grupo == "Respiratorio":
        data['grupo_cie10_Respiratorio'] = True
    elif grupo == "Sentidos":
        data['grupo_cie10_Sentidos (ojo/oído)'] = True
    elif grupo == "Tumores":
        data['grupo_cie10_Tumores'] = True
    # "Otro" → todas False

    # =========================
    # PREDICCIÓN
    # =========================

    df = pd.DataFrame([data])

    pred = modelo.predict(df)

    st.success(f"Días estimados de hospitalización: {pred[0]:.2f}")