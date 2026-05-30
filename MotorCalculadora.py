import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Configuración de página de Streamlit
st.set_page_config(
    page_title="Calculadora de Alcance Cross-Media",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar estado para canales si no existen
if 'channels' not in st.session_state:
    st.session_state.channels = [
        {"id": "tv", "name": "Televisión Abierta", "reach": 45.0, "active": True, "icon": "📺", "is_custom": False},
        {"id": "social", "name": "Redes Sociales (FB/IG/TikTok)", "reach": 60.0, "active": True, "icon": "📱", "is_custom": False},
        {"id": "olv", "name": "Video Online (YouTube/OTT)", "reach": 35.0, "active": True, "icon": "🎥", "is_custom": False},
        {"id": "radio", "name": "Radio & Audio Digital", "reach": 20.0, "active": False, "icon": "📻", "is_custom": False},
        {"id": "ooh", "name": "Vía Pública (OOH)", "reach": 25.0, "active": False, "icon": "📍", "is_custom": False}
    ]

# Estilo personalizado para un diseño premium oscuro
st.markdown("""
<style>
    .metric-card {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
    }
    .metric-title {
        font-size: 0.85rem;
        color: #94a3b8;
        font-weight: 600;
        text-transform: uppercase;
        margin-bottom: 8px;
    }
    .metric-value {
        font-size: 2.2rem;
        font-weight: 800;
        color: #6366f1;
    }
    .metric-sub {
        font-size: 0.75rem;
        color: #64748b;
        margin-top: 5px;
    }
</style>
""", unsafe_allow_html=True)

# --- CABECERA ---
st.title("📊 Calculadora de Alcance Total Cross-Media")
st.caption("Optimización de presupuestos de campaña mediante la probabilidad combinada de Sainsbury.")

# --- SECCIÓN DE EXPLICACIÓN (ACORDEÓN) ---
with st.expander("ℹ️ ¿Cómo se calcula? Conoce la fórmula de Sainsbury", expanded=False):
    st.markdown("""
    La fórmula clásica de **Sainsbury** asume que las duplicaciones de audiencia entre medios se comportan de forma probabilística e independiente. 
    Calcula el alcance combinado estimando primero la probabilidad de que una persona **no sea impactada por ningún medio**, y restando ese valor del total de la población ($1$ o $100\%$).
    """)
    st.latex(r"Alcance\ Total = 1 - \prod_{i=1}^{n} (1 - Alcance_i)")
    st.markdown("""
    * **Alcance Neto Individual:** Audiencia propia y única de cada medio.
    * **Alcance Incremental Secuencial:** Representa los usuarios nuevos y únicos que aporta cada canal a medida que lo sumamos de manera ordenada (de mayor a menor alcance) a la mezcla publicitaria.
    """)

st.write("---")

# Layout de dos columnas principales: Configuración (Izquierda) e Informe (Derecha)
col_left, col_right = st.columns(2, gap="large")

# --- COLUMNA IZQUIERDA: CONFIGURACIÓN DE MEDIOS ---
with col_left:
    st.subheader("⚙️ Configuración de Medios")
    st.write("Activa los medios y define su alcance neto individual (%):")

    # Lista para actualizar cambios en vivo
    updated_channels = []
    
    # Renderizar controles para cada canal
    for i, ch in enumerate(st.session_state.channels):
        # Usamos contenedores para organizar la interfaz
        with st.container():
            col_check, col_input, col_del = st.columns([3, 1, 1])
            
            # Checkbox de activación
            label_text = f"{ch['icon']} {ch['name']}"
            active = col_check.checkbox(label_text, value=ch['active'], key=f"check_{ch['id']}")
            
            # Input de Reach (deshabilitado si no está activo)
            reach = ch['reach']
            if active:
                reach = col_input.number_input(
                    "Reach (%)", 
                    min_value=0.0, 
                    max_value=100.0, 
                    value=float(ch['reach']), 
                    step=0.5, 
                    key=f"reach_{ch['id']}",
                    label_visibility="collapsed"
                )
            else:
                col_input.write("<span style='color:gray; font-size:0.85rem; line-height:2.5;'>Desactivado</span>", unsafe_allow_html=True)

            # Botón de eliminar para canales personalizados
            delete_clicked = False
            if ch['is_custom']:
                delete_clicked = col_del.button("🗑️", key=f"del_{ch['id']}", help="Eliminar canal personalizado")

            # Solo guardamos si no se ha presionado eliminar
            if not delete_clicked:
                updated_channels.append({
                    "id": ch['id'],
                    "name": ch['name'],
                    "reach": reach,
                    "active": active,
                    "icon": ch['icon'],
                    "is_custom": ch['is_custom']
                })

    # Guardar cambios
    st.session_state.channels = updated_channels

    st.write("---")
    
    # Formulario para agregar nuevos medios personalizados
    st.markdown("##### ➕ Agregar Medio Personalizado")
    with st.form("custom_media_form", clear_on_submit=True):
        col_new_name, col_new_reach = st.columns([3, 1])
        new_name = col_new_name.text_input("Nombre del nuevo medio", placeholder="Ej. Programmatic, Influencers")
        new_reach = col_new_reach.number_input("Reach (%)", min_value=0.0, max_value=100.0, value=30.0, step=1.0)
        submit_btn = st.form_submit_button("Añadir Medio", use_container_width=True)
        
        if submit_btn and new_name.strip():
            new_id = f"custom_{int(pd.Timestamp.now().timestamp())}"
            st.session_state.channels.append({
                "id": new_id,
                "name": new_name.strip(),
                "reach": new_reach,
                "active": True,
                "icon": "🚀",
                "is_custom": True
            })
            st.rerun()

# --- PROCESAMIENTO MATEMÁTICO (SAINSBURY) ---
active_channels = [ch for ch in st.session_state.channels if ch['active']]

if len(active_channels) > 0:
    # Ordenar de mayor a menor Reach individual
    sorted_channels = sorted(active_channels, key=lambda x: x['reach'], reverse=True)
    
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
    gross_reach = sum([ch['reach'] for ch in active_channels])
    duplication = gross_reach - total_reach
else:
    total_reach = 0.0
    df_steps = pd.DataFrame()
    gross_reach = 0.0
    duplication = 0.0

# --- COLUMNA DERECHA: RESULTADOS Y GRÁFICAS ---
with col_right:
    st.subheader("📈 Resultados de la Simulación")
    
    if len(active_channels) > 0:
        # Fila de métricas usando HTML estilizado
        kpi_col1, kpi_col2 = st.columns(2)
        
        with kpi_col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Alcance Neto Combinado</div>
                <div class="metric-value">{total_reach:.2f}%</div>
                <div class="metric-sub">Población total alcanzada mín. 1 vez</div>
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
            
        st.write("### Aporte Incremental y Curva de Cobertura")
        st.caption("Gráfico interactivo: el bloque gris representa el alcance ya obtenido y el bloque de color el aporte incremental de este canal.")

        # Construir Gráfica de Barras Flotantes (Cascada Horizontal) usando Plotly
        fig = go.Figure()

        # Agregar bloque de Alcance Acumulado Previo (Invisible o color gris neutro)
        fig.add_trace(go.Bar(
            y=df_steps['name'],
            x=df_steps['previous_cumulative'],
            orientation='h',
            name='Alcance Previo',
            marker=dict(color='rgba(148, 163, 184, 0.25)', line=dict(color='rgba(148, 163, 184, 0.4)', width=1)),
            hoverinfo='skip'
        ))

        # Agregar bloque de Aporte Incremental Neto Real
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

        # Configuración del Layout del Gráfico
        fig.update_layout(
            barmode='stack',
            xaxis=dict(
                title="Porcentaje de Alcance Poblacional (%)",
                range=[0, min(100, max(total_reach + 10, 20))],
                gridcolor='rgba(255, 255, 255, 0.1)'
            ),
            yaxis=dict(
                autorange="reversed", # Mayor alcance primero
                gridcolor='rgba(255, 255, 255, 0.1)'
            ),
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=350,
            margin=dict(l=20, r=20, t=10, b=10),
            font=dict(color='#e2e8f0')
        )

        st.plotly_chart(fig, use_container_width=True)

        # Tabla de Detalles
        st.markdown("##### Detalle Numérico del Plan de Medios")
        
        # Formatear el Dataframe para presentarlo elegante
        display_df = df_steps.copy()
        display_df.columns = ["Medio", "Icono", "Reach Individual", "Base Anterior", "Aporte Neto", "Acumulado", "Orden"]
        display_df["Reach Individual"] = display_df["Reach Individual"].apply(lambda x: f"{x:.1f}%")
        display_df["Base Anterior"] = display_df["Base Anterior"].apply(lambda x: f"{x:.1f}%")
        display_df["Aporte Neto"] = display_df["Aporte Neto"].apply(lambda x: f"+{x:.2f}%")
        display_df["Acumulado"] = display_df["Acumulado"].apply(lambda x: f"{x:.2f}%")
        
        st.dataframe(
            display_df[["Orden", "Medio", "Reach Individual", "Acumulado", "Aporte Neto"]],
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("💡 Por favor, activa al menos uno de los medios de comunicación en el panel de la izquierda para comenzar con la simulación.")