import streamlit as st
import datetime
import json
import os

# 1. CONFIGURACIÓN GENERAL Y PERSISTENCIA (Archivo Local JSON)
st.set_page_config(layout="wide", page_title="Cultivapp Alpha 3")

DB_FILE = "cultivapp_data.json"

def cargar_datos():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Convertir las claves de texto a objetos datetime.date
                bitacora_convertida = {}
                for k, v in data.get("bitacora", {}).items():
                    fecha_obj = datetime.datetime.strptime(k, "%Y-%m-%d").date()
                    bitacora_convertida[fecha_obj] = v
                data["bitacora"] = bitacora_convertida
                return data
        except:
            return {"config": {}, "bitacora": {}, "fase": "Vegetativo"}
    return {"config": {}, "bitacora": {}, "fase": "Vegetativo"}

def guardar_datos():
    data_to_save = {
        "config": st.session_state.config,
        "fase": st.session_state.fase,
        "bitacora": {k.strftime("%Y-%m-%d"): v for k, v in st.session_state.bitacora.items()}
    }
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data_to_save, f, ensure_ascii=False, indent=4)

# Cargar datos iniciales en el estado de la sesión
datos_guardados = cargar_datos()
if "config" not in st.session_state:
    st.session_state.config = datos_guardados.get("config", {})
if "bitacora" not in st.session_state:
    st.session_state.bitacora = datos_guardados.get("bitacora", {})
if "fase" not in st.session_state:
    st.session_state.fase = datos_guardados.get("fase", "Vegetativo")
if "selected_date" not in st.session_state:
    st.session_state.selected_date = None
if "menu_action" not in st.session_state:
    st.session_state.menu_action = None

# INYECCIÓN DE ESTILOS CSS (Tipografía Arial, proporciones limpias)
st.markdown("""
    <style>
    body, p, div, span, label, input, button, select { font-family: 'Arial', sans-serif !important; }
    .card-madre { background-color: #E8F5E9; padding: 12px; border-radius: 6px 6px 0px 0px; border: 1px solid #C8E6C9; color: #2E7D32; }
    .card-esqueje { background-color: #E3F2FD; padding: 12px; border-radius: 0px 0px 6px 6px; border: 1px solid #BBDEFB; color: #0D47A1; }
    .header-banner { background-color: #E8F5E9; padding: 10px; border-radius: 6px; text-align: center; border: 1px solid #A5D6A7; font-weight: bold; color: #2E7D32; margin-bottom: 15px; }
    .header-banner-flora { background-color: #F3E5F5; padding: 10px; border-radius: 6px; text-align: center; border: 1px solid #CE93D8; font-weight: bold; color: #6A1B9A; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

# 2. TARJETA DE PARÁMETROS INICIALES (Formulario Obligatorio)
if not st.session_state.config:
    st.markdown("### 🪴 Configuración Inicial del Cultivo (Alpha 3)")
    st.write("Completa los parámetros base para inicializar tu calendario personalizado.")
    
    maceta = st.selectbox("Capacidad de la maceta:", ["3L", "5L", "7L", "10L", "15L", "20L"], index=3)
    sustrato = st.selectbox("Sustrato:", ["Cultivate", "Treemix", "Casero"])
    raza = st.selectbox("Raza de semillas (Banco BSF):", ["Tangie", "Gorilla Ghost"])
    potencia = st.text_input("Potencia de la iluminación:", value="LED Full Spectrum 350W")
    usar_esquejes = st.checkbox("¿Deseas incluir la sección de esquejes?", value=True)
    
    if st.button("💾 Inicializar Calendario y Guardar", use_container_width=True):
        st.session_state.config = {
            "maceta": maceta,
            "sustrato": sustrato,
            "raza": raza,
            "potencia": potencia,
            "usar_esquejes": usar_esquejes
        }
        # Inyectar bitácora automatizada base para la Tangie si está vacía
        if not st.session_state.bitacora and raza == "Tangie":
            st.session_state.bitacora = {
                datetime.date(2026, 9, 11): {"tareas_madre": ["Trasplantar a 10L 🪴", "Regar con Treemix + Under + Melaza 🧪"], "tareas_esqueje": ["Cortar 6 esquejes ✂️", "Aplicar King Clon y domo 🧬"], "done_m": [False, False], "done_e": [False, False]},
                datetime.date(2026, 9, 16): {"tareas_madre": ["Riego de control (Agua sola) 💧", "Ph Down Namasté a 6.2 🧪"], "tareas_esqueje": ["Ventilar botellas 5 min 💨"], "done_m": [False, False], "done_e": [False]},
                datetime.date(2026, 9, 19): {"tareas_madre": ["Primer riego de Flora (Top Veg+Under+Melaza) 🧪", "Timer directo a 12/12 ⏱️"], "tareas_esqueje": ["Buscar raíces blancas 🔍"], "done_m": [False, False], "done_e": [False]}
            }
        guardar_datos()
        st.rerun()
    st.stop()

# 3. INTERFAZ PRINCIPAL (Proporción 20/80 entre Menú y Calendario)
col_menu, col_main = st.columns([1, 4])

with col_menu:
    # Encabezado dinámico de la Raza iniciada
    banner_style = "header-banner" if st.session_state.fase == "Vegetativo" else "header-banner-flora"
    st.markdown(f"<div class='{banner_style}'>🧬 {st.session_state.config['raza']}</div>", unsafe_allow_html=True)
    
    # Botones en el orden exacto solicitado
    if st.button("✏️ Planificar Día", use_container_width=True):
        st.session_state.menu_action = "planificar"
    if st.button("📝 Editar Tareas", use_container_width=True):
        st.session_state.menu_action = "editar"
    if st.button("📖 Info Raza", use_container_width=True):
        st.session_state.menu_action = "info"
        
    st.write("---")
    st.markdown(f"**Fase:** {st.session_state.fase}")
    if st.button("⏱️ Alternar Veg/Flora", use_container_width=True):
        st.session_state.fase = "Floración" if st.session_state.fase == "Vegetativo" else "Vegetativo"
        guardar_datos()
        st.rerun()
        
    # Reloj local corregido (ART)
    now_utc = datetime.datetime.utcnow()
    now = now_utc - datetime.timedelta(hours=3)
    st.caption(f"🕒 {now.strftime('%H:%M')} ART")
    st.code("18h LUZ / 6h OFF" if st.session_state.fase == "Vegetativo" else "12h LUZ / 12h OFF")

with col_main:
    # MÓDULO DE INFORMACIÓN DINÁMICA (Cálculos Agronómicos de la Tangie)
    if st.session_state.menu_action == "info":
        st.markdown("### 📖 Manual Técnico: Parámetros de la Raza")
        if st.session_state.config["raza"] == "Tangie":
            st.write("**Variedad:** Tangie (70% Sativa / 30% Indica) | **Ciclo total:** 9 Semanas")
            
            # Cálculo de agua por litro de sustrato (10% y 15%)
            litros_num = float(st.session_state.config["maceta"].replace("L", ""))
            agua_veg = litros_num * 0.10
            agua_flora_1 = litros_num * 0.10
            agua_flora_2 = litros_num * 0.15
            
            tab_veg, tab_flo = st.tabs(["🌱 ETAPA VEGETATIVA", "🟣 ETAPA FLORACIÓN (9 Semanas)"])
            
            with tab_veg:
                st.markdown(f"""
                * **Cantidad de Agua por Riego (10%):** {agua_veg:.1f} Litros por planta.
                * **Sustrato seleccionado:** {st.session_state.config['sustrato']}
                * **pH Ideal Entrada / Salida:** 6.0 - 6.2 / 6.0 - 6.5
                * **EC Ideal Entrada / Salida:** 1.0 - 1.4 mS/cm / 0.8 - 1.2 mS/cm
                * **Nutrición sugerida:** Intercalada. Aplicar **N (Nitrógeno)** + **Hongos benéficos** + **Melaza**.
                """)
            with tab_flo:
                st.markdown(f"""
                **Semanas 1 a 4 (Prefloración y Estiramiento):**
                * **Cantidad de Agua por Riego (10%):** {agua_flora_1:.1f} Litros por planta.
                * **pH Ideal Entrada / Salida:** 6.2 / 6.2 - 6.5
                * **EC Ideal Entrada / Salida:** 1.1 - 1.3 mS/cm / 0.9 - 1.3 mS/cm
                * **Nutrición sugerida:** Aporte mínimo de **N (Nitrógeno)** para estiramiento + **Fósforo (P)** y **Potasio (K)** + **Melaza**.
                
                **Semanas 5 a 9 (Engorde Avanzado y Lavado):**
                * **Cantidad de Agua por Riego (15%):** {agua_flora_2:.1f} Litros por planta.
                * **pH Ideal Entrada / Salida:** 6.3 - 6.5 / 6.3 - 6.5
                * **EC Ideal Entrada / Salida:** 1.3 - 1.6 mS/cm / 1.0 - 1.4 mS/cm
                * **Nutrición sugerida:** Máximo aporte de **P (Fósforo)** y **K (Potasio)** + **Melaza**. Detener abonos en semana 8 para lavado final.
                """)
        if st.button("❌ Cerrar Info", use_container_width=True):
            st.session_state.menu_action = None
            st.rerun()
        st.write("---")

    # MÓDULO EDITAR CON FUNCIÓN DE BORRADO AUTOMÁTICO SI QUEDA VACÍO
    elif st.session_state.menu_action == "editar":
        st.markdown("### 📝 Modificar o Eliminar Tarea")
        fecha_edit = st.date_input("Fecha a modificar:", datetime.date(2026, 9, 16))
        
        if fecha_edit in st.session_state.bitacora:
            secciones_disp = ["Plantas Grandes (Madre)"]
            if st.session_state.config["usar_esquejes"]:
                secciones_disp.append("Esquejes")
                
            tipo = st.radio("Sección a modificar:", secciones_disp)
            lista_target = "tareas_madre" if tipo == "Plantas Grandes (Madre)" else "tareas_esqueje"
            done_target = "done_m" if tipo == "Plantas Grandes (Madre)" else "done_e"
            
            if st.session_state.bitacora[fecha_edit][lista_target]:
                idx_tarea = st.selectbox("Selecciona la tarea:", range(len(st.session_state.bitacora[fecha_edit][lista_target])), format_func=lambda x: st.session_state.bitacora[fecha_edit][lista_target][x])
                texto_nuevo = st.text_input("Modifica el texto (deja en blanco para eliminar la tarea):", value=st.session_state.bitacora[fecha_edit][lista_target][idx_tarea])
                
                col_e1, col_e2 = st.columns(2)
                with col_e1:
                    if st.button("💾 Actualizar", use_container_width=True):
                        if texto_nuevo.strip() == "":
  
    elif st.session_state.menu_action == "editar":
        st.markdown("### 📝 Modificar o Eliminar Tareas")
        fecha_edit = st.date_input("Fecha a modificar:", datetime.date(2026, 9, 16))
        if fecha_edit in st.session_state.bitacora:
            secciones_disp = ["Plantas Grandes (Madre)"]
            if st.session_state.config["usar_esquejes"]:
                secciones_disp.append("Esquejes")
            tipo = st.radio("Sección a modificar:", secciones_disp)
            lista_target = "tareas_madre" if tipo == "Plantas Grandes (Madre)" else "tareas_esqueje"
            done_target = "done_m" if tipo == "Plantas Grandes (Madre)" else "done_e"
            if st.session_state.bitacora[fecha_edit][lista_target]:
                idx_tarea = st.selectbox("Selecciona la tarea:", range(len(st.session_state.bitacora[fecha_edit][lista_target])), format_func=lambda x: st.session_state.bitacora[fecha_edit][lista_target][x])
                texto_nuevo = st.text_input("Modifica el texto (deja en blanco para eliminar la tarea):", value=st.session_state.bitacora[fecha_edit][lista_target][idx_tarea])
                col_e1, col_e2 = st.columns(2)
                with col_e1:
                    if st.button("💾 Actualizar", use_container_width=True):
                        if texto_nuevo.strip() == "":
                            st.session_state.bitacora[fecha_edit][lista_target].pop(idx_tarea)
                            st.session_state.bitacora[fecha_edit][done_target].pop(idx_tarea)
                            st.success("¡Tarea eliminada de la bitácora!")
                        else:
                            st.session_state.bitacora[fecha_edit][lista_target][idx_tarea] = texto_nuevo
                            st.success("¡Tarea actualizada!")
                        guardar_datos()
                        st.rerun()
                with col_e2:
                    if st.button("❌ Cancelar", use_container_width=True):
                        st.session_state.menu_action = None
                        st.rerun()
            else:
                st.warning("No hay tareas en esta sección.")
        else:
            st.info("No hay tareas registradas en esta fecha.")
        st.write("---")

    elif st.session_state.menu_action == "planificar":
        st.markdown("### ✏️ Planificar Nueva Tarea Manual")
        fecha_ingresada = st.date_input("Fecha de la tarea:", datetime.date(2026, 9, 16))
        secciones_disp = ["Plantas Grandes (Madre)"]
        if st.session_state.config["usar_esquejes"]:
            secciones_disp.append("Esquejes")
        tipo_tarea = st.selectbox("Sección:", secciones_disp)
        nueva_tarea = st.text_input("Descripción de la tarea:")
        cb1, cb2 = st.columns(2)
        with cb1:
            if st.button("💾 Guardar Tarea", use_container_width=True):
                if fecha_ingresada not in st.session_state.bitacora:
                    st.session_state.bitacora[fecha_ingresada] = {"tareas_madre": [], "tareas_esqueje": [], "done_m": [], "done_e": []}
                if tipo_tarea == "Plantas Grandes (Madre)":
                    st.session_state.bitacora[fecha_ingresada]["tareas_madre"].append(nueva_tarea)
                    st.session_state.bitacora[fecha_ingresada]["done_m"].append(False)
                else:
                    st.session_state.bitacora[fecha_ingresada]["tareas_esqueje"].append(nueva_tarea)
                    st.session_state.bitacora[fecha_ingresada]["done_e"].append(False)
                guardar_datos()
                st.success("¡Tarea agendada permanentemente!")
                st.rerun()
        with cb2:
            if st.button("❌ Cerrar", use_container_width=True):
                st.session_state.menu_action = None
                st.rerun()
        st.write("---")

    st.markdown("<h2 style='text-align: center; color: #333;'>📅 Septiembre 2026</h2>", unsafe_allow_html=True)
    dias_septiembre = [datetime.date(2026, 9, d) for d in range(7, 28)]
    cols_dias = st.columns(7)
    dias_semana = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
    for idx, nombre_dia in enumerate(dias_semana):
        cols_dias[idx].markdown(f"<p style='text-align:center; font-weight:600; margin-bottom:5px;'>{nombre_dia}</p>", unsafe_allow_html=True)
    accent_color_fase = "#A5D6A7" if st.session_state.fase == "Vegetativo" else "#CE93D8"
    for idx, fecha in enumerate(dias_septiembre):
        col_target = cols_dias[idx % 7]
        tiene_tarea = fecha in st.session_state.bitacora
        with col_target:
            if st.button(f"{fecha.day}", key=f"day_{fecha.day}_{idx}", use_container_width=True):
                st.session_state.selected_date = fecha
            if tiene_tarea:
                st.markdown(f"<div style='background-color:{accent_color_fase}; height:5px; border-radius:2px; margin-top:-5px; margin-bottom:10px;'></div>", unsafe_allow_html=True)
            else:
                st.markdown("<div style='height:5px; margin-top:-5px; margin-bottom:10px;'></div>", unsafe_allow_html=True)

    if st.session_state.selected_date:
        fecha_sel = st.session_state.selected_date
        st.write("---")
        st.markdown(f"### 📋 Tareas del Día: {fecha_sel.strftime('%d/%m/%Y')}")
        if fecha_sel in st.session_state.bitacora:
            data_dia = st.session_state.bitacora[fecha_sel]
            if st.session_state.config["usar_esquejes"]:
                col_madres, col_clones = st.columns(2)
                with col_madres:
                    st.markdown(f"<div class='card-madre'><b>🌿 MACETAS ({st.session_state.config['maceta']})</b></div>", unsafe_allow_html=True)
                    if data_dia.get("tareas_madre"):
                        for i, t in enumerate(data_dia["tareas_madre"]):
                            data_dia["done_m"][i] = st.checkbox(t, value=data_dia["done_m"][i], key=f"m_{fecha_sel}_{i}")
                    else:
                        st.caption("Sin tareas asignadas.")
                with col_clones:
                    st.markdown("<div class='card-esqueje'><b>🧬 ESQUEJES (Segunda Generación)</b></div>", unsafe_allow_html=True)
                    if data_dia.get("tareas_esqueje"):
                        for i, t in enumerate(data_dia["tareas_esqueje"]):
                            data_dia["done_e"][i] = st.checkbox(t, value=data_dia["done_e"][i], key=f"e_{fecha_sel}_{i}")
                    else:
                        st.caption("Sin tareas asignadas.")
            else:
                st.markdown(f"<div class='card-madre' style='border-radius:6px;'><b>🌿 MACETAS ({st.session_state.config['maceta']})</b></div>", unsafe_allow_html=True)
                st.write("")
                if data_dia.get("tareas_madre"):
                    for i, t in enumerate(data_dia["tareas_madre"]):
                        data_dia["done_m"][i] = st.checkbox(t, value=data_dia["done_m"][i], key=f"m_{fecha_sel}_{i}")
                else:
                    st.caption("Sin tareas asignadas.")
            st.session_state.bitacora[fecha_sel] = data_dia
            guardar_datos()
        else:
            st.info("Día sin tareas automatizadas.")
        if st.button("❌ Cerrar Tarjeta", use_container_width=True):
            st.session_state.selected_date = None
            st.rerun()
