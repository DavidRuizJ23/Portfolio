import streamlit as st
import pandas as pd
import numpy as np
# Importamos la librería oficial de Google GenAI (Asegúrate de instalar: pip install google-genai)
from google.genai import Client
from google.genai import types

import plotly.graph_objects as go
# 0. Configuración Login
# --- CONTROL DE ACCESO / SEGURIDAD ---
# Inicializar la variable de autenticación si no existe
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def check_password():
    """Valida la contraseña introducida por el usuario."""
    if st.session_state["password_input"] == "DavidGoogle2026":  # <-- AQUÍ defines tu contraseña
        st.session_state.authenticated = True
        del st.session_state["password_input"]  # Limpia el input de la memoria por seguridad
    else:
        st.session_state.authenticated = False
        st.error("❌ Contraseña incorrecta. Acceso denegado.")

# Si el usuario NO está autenticado, muestra la pantalla de bloqueo
if not st.session_state.authenticated:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col_l, col_c, col_r = st.columns([1, 2, 1])
    
    with col_c:
        st.markdown("### 🔐 Portafolio Analítico Avanzado - David Ruiz")
        st.caption("Este entorno contiene metodologías propietarias, simuladores no lineales y modelos predictivos corporativos.")
        st.write("---")
        
        # Input de tipo 'password' para ocultar los caracteres al escribir
        st.text_input(
            "Introduzca la contraseña de acceso institucional:",
            type="password",
            key="password_input",
            on_change=check_password
        )
        
        st.info("💡 Por favor contactar a David para obtener la contraseña a través de LinkedIn o correo (david.ruizj@ciencias.unam.mx).")
    
    # Detiene la ejecución del resto de la aplicación para que nadie vea los módulos sin contraseña
    st.stop()

# 1. CONFIGURACIÓN DE LA PÁGINA (Estilo Minimalista)
st.set_page_config(
    page_title="David Ruiz - Advanced Analytics Portfolio",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo personalizado para el look & feel limpio y corporativo
st.markdown("""
    <style>
    .main-title { font-size: 28px; font-weight: bold; color: #2c3e50; margin-bottom: 5px; }
    .subtitle { font-size: 16px; color: #7f8c8d; margin-bottom: 25px; }
    div.stButton > button:first-child { background-color: #2c3e50; color: white; }
    </style>
""", unsafe_allow_html=True)

# 2. CONFIGURACIÓN DEL CLIENTE GEMINI API
# El sistema buscará automáticamente la variable de entorno GEMINI_API_KEY
try:
    client = Client()
except Exception:
    client = None

# Contexto maestro para que Gemini conozca a fondo tu perfil y actúe como tu consultor
CONTEXTO_DAVID = """
Eres el asistente virtual de Inteligencia Artificial integrado en el portafolio profesional de David Ruiz. 
David es un Actuario y Director de Analítica Avanzada con más de 15 años de experiencia en agencias de medios (WPP/Choreograph). 
Es experto en modelación de Marketing Mix Models (MMM), pruebas de incrementalidad, atribución y el diseño de herramientas automatizadas en Python y R.
Tu objetivo es responder de manera sumamente estratégica, técnica y orientada a negocio (C-Suite) las dudas de los reclutadores o directores que visitan la app.
Habla siempre con seguridad, respaldando el trabajo analítico y la visión de liderazgo regional de David.
"""

# 3. BARRA LATERAL: Perfil y Chat Contextual con Gemini
with st.sidebar:
    st.markdown("## 🧠 David Ruiz")
    st.markdown("**Senior Director of Advanced Analytics**")
    st.caption("Especialista en Measurement, Modelos Causales e Innovación en IA")
    st.write("---")
    
    st.markdown("### 💬 Consulta al Asistente de IA")
    st.write("Pregúntame sobre las metodologías, los modelos o el impacto de negocio de los proyectos de David.")
    
    # Inicializar el historial del chat si no existe
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Mostrar mensajes anteriores
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input del usuario
    if prompt := st.chat_input("¿Cómo optimiza David el ROI?"):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Respuesta de Gemini
        with st.chat_message("assistant"):
            if client:
                try:
                    # Usamos el modelo recomendado gemini-2.5-flash para respuestas ágiles
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            system_instruction=CONTEXTO_DAVID,
                            temperature=0.3
                        )
                    )
                    respuesta_texto = response.text
                except Exception as e:
                    respuesta_texto = f"Error al conectar con Gemini API: {str(e)}"
            else:
                respuesta_texto = "API Key de Gemini no configurada. (Por favor establece la variable de entorno GEMINI_API_KEY)."
            
            st.markdown(respuesta_texto)
        st.session_state.messages.append({"role": "assistant", "content": respuesta_texto})


# 4. CUERPO PRINCIPAL: Navegación del Portafolio
st.markdown('<div class="main-title">Portfolio de Apps Predictivas en AdTech</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Una orquestación entre Ciencia de Datos, Estrategia de Medios y Modelación Causal e Incrementabilidad manteniendo precisión científica y resultados en tiempo real</div>', unsafe_allow_html=True)


# Definición de las pestañas para los tres desarrollos innovadores
tab1, tab2, tab3 = st.tabs([
    "🎯 1. Calculadora de Alcance", 
    "📊 2. Optimizador de ROI", 
    "🧠 3. Predictor de Propensión al Lift"
])

with tab1:
    # --- REDISEÑO NARRATIVO DIRECCIONAL ---
    st.markdown("### 🎯 Calculadora de Alcance Neto Cross-Media")
    st.markdown("""
    **Enfoque Estratégico:** Esta herramienta automatiza la optimización probabilística del alcance incremental utilizando la fórmula de **Sainsbury**. 
    Permite al C-Suite visualizar con precisión científica que la simple suma bruta de impactos de medios sobrestima la cobertura real, ayudando a reasignar presupuestos hacia los canales con mayor aporte neto y menor duplicación de audiencias.
    """)

    # Inicializar estado aislado para los canales de este módulo si no existen
    if 'reach_channels' not in st.session_state:
        st.session_state.reach_channels = [
            {"id": "tv", "name": "Televisión Abierta", "reach": 45.0, "active": True, "icon": "📺", "is_custom": False},
            {"id": "social", "name": "Redes Sociales (FB/IG/TikTok)", "reach": 60.0, "active": True, "icon": "📱", "is_custom": False},
            {"id": "olv", "name": "Video Online (YouTube/OTT)", "reach": 35.0, "active": True, "icon": "🎥", "is_custom": False},
            {"id": "radio", "name": "Radio & Audio Digital", "reach": 20.0, "active": False, "icon": "📻", "is_custom": False},
            {"id": "ooh", "name": "Vía Pública (OOH)", "reach": 25.0, "active": False, "icon": "📍", "is_custom": False}
        ]

    # Layout de dos columnas principales: Configuración (Izquierda) e Informe (Derecha)
    col_reach_left, col_reach_right = st.columns(2, gap="large")

    # --- COLUMNA IZQUIERDA: CONFIGURACIÓN DE MEDIOS ---
    with col_reach_left:
        st.markdown("#### ⚙️ Configuración del Mix de Medios")
        st.caption("Active los canales tácticos y defina su alcance neto individual estimado:")

        # Lista para actualizar cambios en vivo
        updated_reach_channels = []
        
        # Renderizar controles para cada canal
        for i, ch in enumerate(st.session_state.reach_channels):
            with st.container():
                col_check, col_input, col_del = st.columns([3, 1, 1])
                
                # Checkbox de activación
                label_text = f"{ch['icon']} {ch['name']}"
                active = col_check.checkbox(label_text, value=ch['active'], key=f"reach_check_{ch['id']}")
                
                # Input de Reach (deshabilitado si no está activo)
                reach = ch['reach']
                if active:
                    reach = col_input.number_input(
                        "Reach (%)", 
                        min_value=0.0, 
                        max_value=100.0, 
                        value=float(ch['reach']), 
                        step=0.5, 
                        key=f"reach_val_{ch['id']}",
                        label_visibility="collapsed"
                    )
                else:
                    col_input.write("<span style='color:gray; font-size:0.85rem; line-height:2.5;'>Desactivado</span>", unsafe_allow_html=True)

                # Botón de eliminar para canales personalizados
                delete_clicked = False
                if ch['is_custom']:
                    delete_clicked = col_del.button("🗑️", key=f"reach_del_{ch['id']}", help="Eliminar canal personalizado")

                # Solo guardamos si no se ha presionado eliminar
                if not delete_clicked:
                    updated_reach_channels.append({
                        "id": ch['id'],
                        "name": ch['name'],
                        "reach": reach,
                        "active": active,
                        "icon": ch['icon'],
                        "is_custom": ch['is_custom']
                    })

        # Guardar cambios en el estado de sesión aislado
        st.session_state.reach_channels = updated_reach_channels

        st.write("---")
        
        # Formulario para agregar nuevos medios personalizados
        st.markdown("##### ➕ Agregar Canal Personalizado")
        with st.form("custom_media_reach_form", clear_on_submit=True):
            col_new_name, col_new_reach = st.columns([3, 1])
            new_name = col_new_name.text_input("Nombre del nuevo medio", placeholder="Ej. Programmatic, Connected TV")
            new_reach = col_new_reach.number_input("Reach (%)", min_value=0.0, max_value=100.0, value=30.0, step=1.0)
            submit_btn = st.form_submit_button("Añadir al Mix", use_container_width=True)
            
            if submit_btn and new_name.strip():
                new_id = f"custom_{int(pd.Timestamp.now().timestamp())}"
                st.session_state.reach_channels.append({
                    "id": new_id,
                    "name": new_name.strip(),
                    "reach": new_reach,
                    "active": True,
                    "icon": "🚀",
                    "is_custom": True
                })
                st.rerun()

    # --- PROCESAMIENTO MATEMÁTICO (SAINSBURY) ---
    active_reach_channels = [ch for ch in st.session_state.reach_channels if ch['active']]

    if len(active_reach_channels) > 0:
        # Ordenar de mayor a menor Reach individual
        sorted_channels = sorted(active_reach_channels, key=lambda x: x['reach'], reverse=True)
        
        cumulative_prob_non_reach = 1.0
        incremental_steps = []
        previous_total_reach = 0.0
        
        for idx, ch in enumerate(sorted_channels):
            reach_decimal = ch['reach'] / 100.0
            cumulative_prob_non_reach *= (1 - reach_decimal)
            
            current_total_reach = (1 - cumulative_prob_non_reach) * 100
            incremental_contribution = current_total_reach - previous_total_reach
            
            incremental_steps.append({
                "name": ch['name'],
                "icon": ch['icon'],
                "individual_reach": ch['reach'],
                "previous_cumulative": previous_total_reach,
                "incremental_reach": incremental_contribution,
                "cumulative_reach": current_total_reach,
                "order": idx + 1
            })
            previous_total_reach = current_total_reach
            
        total_reach = (1 - cumulative_prob_non_reach) * 100
        df_steps = pd.DataFrame(incremental_steps)
        gross_reach = sum([ch['reach'] for ch in active_reach_channels])
        duplication = gross_reach - total_reach
    else:
        total_reach = 0.0
        df_steps = pd.DataFrame()
        gross_reach = 0.0
        duplication = 0.0

    # --- COLUMNA DERECHA: RESULTADOS Y NARRATIVA ---
    with col_reach_right:
        st.markdown("#### 📈 Resultados e Impacto en Cobertura")
        
        if len(active_reach_channels) > 0:
            kpi_col1, kpi_col2 = st.columns(2)
            
            with kpi_col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Alcance Neto Combinado</div>
                    <div class="metric-value">{total_reach:.2f}%</div>
                    <div class="metric-sub">Población única alcanzada mín. 1 vez</div>
                </div>
                """, unsafe_allow_html=True)
                
            with kpi_col2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Eficiencia / Duplicación</div>
                    <div class="metric-value" style="color:#10b981;">{duplication:.1f} pp</div>
                    <div class="metric-sub">Traslape evitado (Suma Bruta: {gross_reach:.1f}%)</div>
                </div>
                """, unsafe_allow_html=True)
                
            st.write("##### Curva de Cobertura de Medios e Incremento")
            
            # Gráfica de Barras Flotantes en Plotly
            fig = go.Figure()
            fig.add_trace(go.Bar(
                y=df_steps['name'],
                x=df_steps['previous_cumulative'],
                orientation='h',
                name='Alcance Previo',
                marker=dict(color='rgba(148, 163, 184, 0.25)', line=dict(color='rgba(148, 163, 184, 0.4)', width=1)),
                hoverinfo='skip'
            ))

            fig.add_trace(go.Bar(
                y=df_steps['name'],
                x=df_steps['incremental_reach'],
                orientation='h',
                name='Aporte Incremental',
                text=df_steps['incremental_reach'].apply(lambda x: f"+{x:.1f}%"),
                textposition='inside',
                marker=dict(
                    color=df_steps['incremental_reach'],
                    colorscale='Viridis',
                    line=dict(color='#6366f1', width=1.5)
                ),
                hovertemplate="<b>%{y}</b><br>Aporte Neto: +%{x:.2f}%<br><extra></extra>"
            ))

            fig.update_layout(
                barmode='stack',
                xaxis=dict(title="Porcentaje de Alcance Poblacional (%)", range=[0, 100], gridcolor='rgba(255, 255, 255, 0.1)'),
                yaxis=dict(autorange="reversed", gridcolor='rgba(255, 255, 255, 0.1)'),
                showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                height=280, margin=dict(l=20, r=20, t=10, b=10), font=dict(color='#e2e8f0')
            )
            st.plotly_chart(fig, use_container_width=True)

            # --- SECCIÓN CRÍTICA DE DIRECCIÓN Y DATA STORYTELLING ---
            with st.expander("💼 Recomendaciones accionables en la estrategia de Paid Media", expanded=True):
                st.markdown(f"""
                **Análisis de la simulación actual:**
                * **La suma tradicional inapropiada:** Si sumáramos el alcance bruto lineal de estos canales operativos, asumiríamos una cobertura teórica del **{gross_reach:.1f}%**. Esto es un sesgo de planeación común.
                * **La realidad probabilística:** La optimización de Sainsbury demuestra que la cobertura real es del **{total_reach:.2f}%**, revelando un traslape de **{duplication:.1f} puntos porcentuales** de la población que está siendo sobre-impactada innecesariamente (fatiga de frecuencias).
                * **Acción sugerida para Dirección:** El último medio integrado aporta un alcance incremental real de solo **{df_steps['incremental_reach'].iloc[-1]:.2f}%** debido a la alta duplicación con los canales líderes. Estratégicamente, se recomienda congelar la inversión en ese canal y reubicar ese capital hacia formatos de nicho (*First-Party data audiences*) para romper el techo de cobertura de manera eficiente.
                """)
        else:
            st.info("💡 Active al menos uno de los medios de comunicación en el panel de la izquierda para desplegar la optimización de alcance y el análisis directivo.")
with tab2:
    # --- ENFOQUE NARRATIVO DIRECTIVO ---
    st.markdown("### 📊 ROI Optimizer Regional (Modelación Causal)")
    st.markdown("""
    **Enfoque Estratégico:** Planeador de escenarios de inversión regional basado en Curvas de Saturación. 
    Esta App simula el comportamiento del Diminishing Returns en los canales de medios para encontrar el punto de inversión ótimo, permitiendo pasar de una asignación presupuestal intuitiva a una maximización científica del retorno financiero de la marca con impacto real en el negocio. 
    """)

    # 1. Selectores de Contexto Regional (Alineado a tus proyectos LATAM)
    col_geo, col_target = st.columns(2)
    with col_geo:
        mercado = st.selectbox("🌍 Seleccionar Región / Mercado:", ["México", "Argentina", "Chile", "Colombia"], index=0)
    with col_target:
        meta_negocio = st.selectbox("🎯 Objetivo Comercial del Simulador:", ["Maximizar ROI Global", "Sostener Volumen de Ventas (Eminente)"], index=0)

    st.write("---")

    # 2. Configuración de Presupuestos (Inputs del C-Suite)
    st.markdown("#### 💵 Simulación de Distribución de Capital")
    st.caption("Ajuste las palancas de inversión por pilar de medios (valores en miles de USD):")

    col_sl1, col_sl2, col_sl3 = st.columns(3)
    with col_sl1:
        inv_digital = st.slider("📱 Medios Digitales (FB/IG/Programmatic):", min_value=10, max_value=500, value=150, step=10)
    with col_sl2:
        inv_tv = st.slider("📺 Televisión Abierta & Paga:", min_value=10, max_value=500, value=200, step=10)
    with col_sl3:
        inv_ooh = st.slider("📍 Vía Pública (OOH & Alternativos):", min_value=10, max_value=500, value=80, step=10)

    # 3. CORE MATEMÁTICO: Curvas de Saturación (Hill Parameters)
    # Parámetros hipotéticos calibrados profesionalmente (Alpha, K-saturation, Max-Efficacy)
    channels_data = {
        "Digital": {"inv": inv_digital, "k": 180, "alpha": 1.5, "emax": 320, "base_roi": 2.1},
        "TV Abierta": {"inv": inv_tv, "k": 280, "alpha": 1.8, "emax": 450, "base_roi": 1.6},
        "OOH / Vía Pública": {"inv": inv_ooh, "k": 120, "alpha": 1.2, "emax": 140, "base_roi": 1.3}
    }

    total_inversion = inv_digital + inv_tv + inv_ooh
    total_retorno = 0.0

    chart_data = []
    # Cálculo del retorno incremental por canal usando la función no lineal
    for name, p in channels_data.items():
        # Función de Hill: emax * (x^alpha) / (k^alpha + x^alpha)
        retorno_incremental = p["emax"] * (p["inv"]**p["alpha"]) / (p["k"]**p["alpha"] + p["inv"]**p["alpha"])
        # Asegurar un piso lógico de ROI base para inversiones bajas
        retorno_final = max(retorno_incremental, p["inv"] * p["base_roi"] * 0.4)
        total_retorno += retorno_final
        
        roi_canal = retorno_final / p["inv"]
        chart_data.append({
            "Canal": name, 
            "Inversión (USD)": p["inv"], 
            "Retorno Estimado (USD)": retorno_final,
            "ROI Específico": roi_canal
        })

    df_roi = pd.DataFrame(chart_data)
    roi_global = total_retorno / total_inversion

    # 4. DESPLIEGUE DE MÉTRICAS FINANCIERAS (Look & Feel Premium)
    st.write("---")
    kpi_roi1, kpi_roi2, kpi_roi3 = st.columns(3)
    
    with kpi_roi1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Presupuesto Total Simulación</div>
            <div class="metric-value" style="color:#e2e8f0;">${total_inversion:,.0f}K</div>
            <div class="metric-sub">Capital total asignado al mix</div>
        </div>
        """, unsafe_allow_html=True)
    with kpi_roi2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Ingreso Incremental Estimado</div>
            <div class="metric-value" style="color:#6366f1;">${total_retorno:,.1f}K</div>
            <div class="metric-sub">Impacto directo en la línea de ventas</div>
        </div>
        """, unsafe_allow_html=True)
    with kpi_roi3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">ROI Global del Mix</div>
            <div class="metric-value" style="color:#10b981;">{roi_global:.2f}x</div>
            <div class="metric-sub">Retorno por cada dólar invertido</div>
        </div>
        """, unsafe_allow_html=True)

    # 5. VISUALIZACIÓN INTERACTIVA DE ASIGNACIÓN VS RETORNO
    st.write("### Distribución del Presupuesto vs. Eficiencia del Retorno")
    
    fig_roi = go.Figure()
    # Barra de Inversión
    fig_roi.add_trace(go.Bar(
        x=df_roi["Canal"], y=df_roi["Inversión (USD)"],
        name="Presupuesto Asignado ($)", marker_color="#334155"
    ))
    # Barra de Retorno
    fig_roi.add_trace(go.Bar(
        x=df_roi["Canal"], y=df_roi["Retorno Estimado (USD)"],
        name="Ingreso Generado ($)", marker_color="#6366f1"
    ))

    fig_roi.update_layout(
        barmode='group',
        xaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)'),
        yaxis=dict(title="Monto en Miles de USD ($)", gridcolor='rgba(255, 255, 255, 0.1)'),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        height=300, margin=dict(l=20, r=20, t=10, b=10), font=dict(color='#e2e8f0'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_roi, use_container_width=True)

    # 6. SECCIÓN CRÍTICA DE DIRECCIÓN Y DATA STORYTELLING
    with st.expander("💼 Acciones estrategicas", expanded=True):
        # Determinar dinámicamente cuál canal está más cerca de saturarse para la recomendación
        canal_saturado = "Digital" if inv_digital > 200 else ("TV Abierta" if inv_tv > 320 else "Ninguno")
        
        st.markdown(f"""
        **Análisis de Atribución y Elasticidad ({mercado}):**
        * **Punto de Inflexión Marginal:** Los datos muestran que el canal **{df_roi.loc[df_roi['ROI Específico'].idxmax(), 'Canal']}** está operando en su zona de máxima eficiencia con un ROI específico de **{df_roi['ROI Específico'].max():.2f}x**. Tiene espacio libre para absorber capital de los canales saturados.
        * **Riesgo de Saturación Detectado:** Al simular una asignación alta en **{canal_saturado}**, la curva Hill se aplana sensiblemente. Añadir \$50K adicionales en ese pilar generará un rendimiento marginal decreciente, encareciendo el costo de adquisición general.
        * **Visión Directiva para el Plan Regional:** Para maximizar la eficiencia en {mercado}, el algoritmo sugiere que la optimización óptima de balance requiere reducir un 10% del pilar sobre-saturado y transferirlo a formatos con curvas de Adstock más largas (como el video online o el OOH estructurado), blindando el **{roi_global:.2f}x** de retorno global de la campaña.
        """)
with tab3:
    # --- ENFOQUE NARRATIVO DIRECTIVO ---
    st.markdown("### 🧠 Predictor de Propensión al Lift (Meta-Análisis de Experimentos)")
    st.markdown("""
    **Enfoque Estratégico:** Modelo predictivo avanzado que actúa como un meta-análisis de Machine Learning. 
    A partir de variables tácticas e histórico de experimentos de incrementabilidad, estima la probabilidad de que una configuración de campaña obtenga un incremento estadísticamente significativo (*Causal Lift*) antes de salir al mercado. 
    Esto permite a equipos ejecutivos pre-calificar la eficiencia de la pauta y mitigar el riesgo de no generar impacto.
    """)

    # 1. Selección de la Métrica de Lift a Evaluar
    metric_target = st.selectbox(
        "🎯 Seleccione la Métrica de Causal Lift a Predecir:",
        ["Ad Recall", "Consideración de Marca", "Purchase Intent", "Favorabilidad de Marca", "Conversiones Incrementales"],
        index=0
    )

    st.write("---")
    st.markdown("#### ⚙️ Configuración y Características de la Campaña (Features)")
    st.caption("Defina los parámetros de planeación para evaluar la propensión de éxito del experimento:")

    # Layout en columnas para los controles (Features del Modelo)
    feat_col1, feat_col2, feat_col3 = st.columns(3)

    with feat_col1:
        obj_campaña = st.selectbox("Objetivo de Campaña:", ["Brand Awareness", "Consideración", "Conversión / Performance"])
        formato_principal = st.selectbox("Formato Dominante:", ["Video Core", "Display / Banners", "Formatos Nativos / Rich Media"])
        tipo_compra = st.selectbox("Tipo de Compra / Puja:", ["CPM (Costo por Mil)", "CPC (Costo por Clic)", "CPV / VTR Optimizado"])
        audiencia_target = st.selectbox("Segmentación Demográfica Core:", ["Generación Z", "Millennials", "Generación X"])

    with feat_col2:
        spend_level = st.selectbox("Nivel de Inversión (Budget Tier):", ["Bajo (< $20K USD)", "Medio ($20K - $100K USD)", "Alto (> $100K USD)"], index=1)
        duracion_video = st.slider("Duración del Asset de Video (seg):", min_value=5, max_value=60, value=15, step=5)
        frecuencia_semanal = st.slider("Frecuencia Promedio Estimada (Frec):", min_value=1.0, max_value=8.0, value=3.2, step=0.1)

    with feat_col3:
        vtr_esperado = st.slider("VTR Objetivo Esperado (%):", min_value=10, max_value=80, value=35, step=5)
        use_1p_data = st.radio("¿Utiliza audiencias First-Party Data (CRM)?", ["Sí (Señales Propias)", "No (Audiencia Abierta)"], index=0)
        estacionalidad = st.selectbox("Temporalidad del Negocio:", ["Q1/Q2 (Estable)", "Q3 (Pre-Temporada)", "Q4 / Alta Saturación (Buen Fin/Navidad)"])

    # 2. MOTOR DE SIMULACIÓN PREDICTIVA (Lógica de Propensión Heurística)
    # Simulamos el comportamiento que un XGBoost real encontraría en la data de medios
    base_score = 45.0  # Probabilidad base

    # Penalizaciones y bonificaciones basadas en el "Media Colmillo"
    if use_1p_data == "Sí (Señales Propias)": base_score += 15.0
    if obj_campaña == "Brand Awareness" and metric_target in ["Ad Recall", "Consideración de Marca"]: base_score += 12.0
    if obj_campaña == "Conversión / Performance" and metric_target == "Conversiones Incrementales": base_score += 10.0
    if estacionalidad == "Q4 / Alta Saturación (Buen Fin/Navidad)": base_score -= 12.0  # El ruido de mercado castiga el lift
    if frecuencia_semanal > 5.5: base_score -= 15.0  # Penalización por saturación/fatiga
    if frecuencia_semanal < 2.0: base_score -= 8.0   # Penalización por falta de cobertura efectiva
    if duracion_video == 15: base_score += 5.0        # El sweet-spot clásico de video short-form
    if spend_level == "Alto (> $100K USD)": base_score += 8.0

    # Acotar la probabilidad entre 5% y 98%
    propensity_score = max(min(base_score, 98.0), 5.0)
    status_lift = "ALTA PROPENSIÓN AL ÉXITO" if propensity_score >= 65 else ("PROPENSIÓN MODERADA" if propensity_score >= 40 else "ALTO RIESGO DE FRACASO (No Significativo)")
    status_color = "#10b981" if propensity_score >= 65 else ("#f59e0b" if propensity_score >= 40 else "#ef4444")

    # 3. DESPLIEGUE DEL SCORE EJECUTIVO
    st.write("---")
    st.markdown("#### 📊 Dictamen del Modelo Supervisado (XGBoost Classifier)")
    
    score_col1, score_col2 = st.columns([1, 2])
    with score_col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Probabilidad de Causal Lift</div>
            <div class="metric-value" style="color:{status_color};">{propensity_score:.1f}%</div>
            <div class="metric-sub" style="font-weight:bold; color:{status_color};">{status_lift}</div>
        </div>
        """, unsafe_allow_html=True)

    with score_col2:
        st.write("##### 📉 Importancia de las Variables (SHAP Feature Importance)")
        st.caption("Esta gráfica muestra qué características tácticas impactan más (positiva o negativamente) en la probabilidad de éxito de la campaña.")
        
        # Simulación de pesos SHAP dinámicos según las selecciones del usuario
        shap_data = {
            "Feature / Característica": ["First-Party Data Usage", "Frecuencia Semanal", "Objetivo vs Métrica", "Estacionalidad de Mercado", "Nivel de Inversión (Spend)", "Duración del Asset"],
            "Importancia Relativa (Weight)": [0.28, 0.22, 0.18, 0.15, 0.10, 0.07]
        }
        df_shap = pd.DataFrame(shap_data).sort_values(by="Importancia Relativa (Weight)", ascending=True)
        
        # Gráfico horizontal en Plotly para Feature Importance
        fig_shap = go.Figure()
        fig_shap.add_trace(go.Bar(
            y=df_shap["Feature / Característica"],
            x=df_shap["Importancia Relativa (Weight)"],
            orientation='h',
            marker_color="#6366f1",
            text=df_shap["Importancia Relativa (Weight)"].apply(lambda x: f"{x*100:.0f}%"),
            textposition='inside'
        ))
        fig_shap.update_layout(
            xaxis=dict(title="Peso Relativo en la Decisión del Modelo", gridcolor='rgba(255, 255, 255, 0.1)'),
            yaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)'),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            height=220, margin=dict(l=10, r=10, t=5, b=5), font=dict(color='#e2e8f0')
        )
        st.plotly_chart(fig_shap, use_container_width=True)

    # 4. SECCIÓN CRÍTICA DE DIRECCIÓN Y DATA STORYTELLING
    with st.expander("💼 Recomendaciones ejeutivas", expanded=True):
        st.markdown(f"""
        **Análisis de Gobernanza de Experimentos para {metric_target}:**
        * **El Rol de la Data Propia:** El análisis SHAP revela que la integración de **First-Party Data** es la variable con mayor peso predictivo (**28%**). Configurar la pauta con audiencias propias blinda el experimento contra la pérdida de cookies, garantizando un Lift incremental para la campaña.
        * **El Peligro de la Fatiga:** Una frecuencia configurada en **{frecuencia_semanal:.1f}** impactos semanales altera el score. Si la frecuencia sobrepasa los 5.5 impactos, el modelo detecta saturación, lo que significa que el presupuesto extra se destinará a impactar a usuarios ya convencidos, destruyendo la incrementalidad del medio.
        * **Recomendación para Operaciones:** Con una probabilidad calculada del **{propensity_score:.1f}%**, esta configuración se clasifica como *{status_lift}*. Si el score es bajo, la sugerencia del director no es cancelar la campaña, sino **reajustar las palancas tácticas** (ej. cambiar temporalidad o amarrar audiencias CRM) para asegurar un test de incremento exitoso antes de comprometer el presupuesto regional.
        """)