import streamlit as st
import datetime
import json
import os

st.set_page_config(layout="wide", page_title="Cultivapp Alpha 3")
DB_FILE = "cultivapp_data.json"

def cargar_datos():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
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

st.markdown("""
    <style>
    body, p, div, span, label, input, button, select { font-family: 'Arial', sans-serif !important; }
    .card-madre { background-color: #E8F5E9; padding: 12px; border-radius: 6px 6px 0px 0px; border: 1px solid #C8E6C9; color: #2E7D32; }
    .card-esqueje { background-color: #E3F2FD; padding: 12px; border-radius: 0px 0px 6px 6px; border: 1px solid #BBDEFB; color: #0D47A1; }
    .header-banner { background-color: #E8F5E9; padding: 10px; border-radius: 6px; text-align: center; border: 1px solid #A5D6A7; font-weight: bold; color: #2E7D32; margin-bottom: 15px; }
    .header-banner-flora { background-color: #F3E5F5; padding: 10px; border-radius: 6px; text-align: center; border: 1px solid #CE93D8; font-weight: bold; color: #6A1B9A; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

if not st.session_state.config:
    st.markdown("### 🪴 Configuración Inicial (Alpha 3)")
    maceta = st.selectbox("Maceta:", ["3L", "5L", "7L", "10L", "15L", "20L"], index=3)
    sustrato = st.selectbox("Sustrato:", ["Cultivate", "Treemix", "Casero"])
    raza = st.selectbox("Raza:", ["Tangie", "Gorilla Ghost"])
    potencia = st.text_input("Luz:", value="LED 350W")
    usar_esquejes = st.checkbox("Incluir sección de esquejes", value=True)
    if st.button("💾 Inicializar Cultivo", use_container_width=True):
        st.session_state.config = {"maceta": maceta, "sustrato": sustrato, "raza": raza, "potencia": potencia, "usar_esquejes": usar_esquejes}
        if not st.session_state.bitacora and raza == "Tangie":
            st.session_state.bitacora = {
                datetime.date(2026, 9, 11): {"tareas_madre": ["Trasplantar a 10L", "Regar con Treemix+Under+Melaza"], "tareas_esqueje": ["Cortar 6 esquejes", "Aplicar King Clon y domo"], "done_m": [False, False], "done_e": [False, False]},
                datetime.date(2026, 9, 16): {"tareas_madre": ["Riego control (Agua sola)", "Ph Down Namasté a 6.2"], "tareas_esqueje": ["Ventilar botellas 5 min"], "done_m": [False, False], "done_e": [False]},
                datetime.date(2026, 9, 19): {"tareas_madre": ["Primer riego Flora (Veg+Under+Melaza)", "Timer a 12/12"], "tareas_esqueje": ["Buscar raíces blancas"], "done_m": [False, False], "done_e": [False]}
            }
        guardar_datos()
        st.rerun()
    st.stop()

col_menu, col_main = st.columns([1, 4])

with col_menu:
    banner_style = "header-banner" if st.session_state.fase == "Vegetativo" else "header-banner-flora"
    st.markdown(f"<div class='{banner_style}'>🧬 {st.session_state.config['raza']}</div>", unsafe_allow_html=True)
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
    now_utc = datetime.datetime.utcnow()
    now = now_utc - datetime.timedelta(hours=3)
    st.caption(f"🕒 {now.strftime('%H:%M')} ART")

with col_main:
    if st.session_state.menu_action == "info":
        st.markdown("### 📖 Manual Técnico: Parámetros")
        if st.session_state.config["raza"] == "Tangie":
            litros_num = float(st.session_state.config["maceta"].replace("L", ""))
            agua_veg, agua_flo1, agua_flo2 = litros_num * 0.10, litros_num * 0.10, litros_num * 0.15
            tab_veg, tab_flo = st.tabs(["🌱 VEGETATIVO", "🟣 FLORACIÓN (9 Semanas)"])
            with tab_veg:
                st.write(f"- **Agua (10%):** {agua_veg:.1f}L por planta.\n- **pH:** 6.0-6.2 | **EC:** 1.0-1.4\n- **Nutrientes:** N + Microvida + Melaza.")
            with tab_flo:
                st.write(f"**Semanas 1-4 (Estiramiento):**\n- **Agua (10%):** {agua_flo1:.1f}L\n- **pH:** 6.2 | **EC:** 1.1-1.3\n- **Nutrientes:** Mínimo N + P + K + Melaza.")
                st.write(f"**Semanas 5-9 (Engorde):**\n- **Agua (15%):** {agua_flo2:.1f}L\n- **pH:** 6.3-6.5 | **EC:** 1.3-1.6\n- **Nutrientes:** Máximo P + K + Melaza.")
        if st.button("❌ Cerrar Info", use_container_width=True):
            st.session_state.menu_action = None
            st.rerun()

    elif st.session_state.menu_action == "editar":
        st.markdown("### 📝 Modificar o Eliminar Tarea")
        fecha_edit = st.date_input("Fecha:", datetime.date(2026, 9, 16))
        if fecha_edit in st.session_state.bitacora:
            secciones_disp = ["Plantas Grandes"]
            if st.session_state.config["usar_esquejes"]: secciones_disp.append("Esquejes")
            tipo = st.radio("Sección:", secciones_disp)
            lista_target = "tareas_madre" if tipo == "Plantas Grandes" else "tareas_esqueje"
            done_target = "done_m" if tipo == "Plantas Grandes" else "done_e"
            if st.session_state.bitacora[fecha_edit][lista_target]:
                idx_tarea = st.selectbox("Selecciona tarea:", range(len(st.session_state.bitacora[fecha_edit][lista_target])), format_func=lambda x: st.session_state.bitacora[fecha_edit][lista_target][x])
                texto_nuevo = st.text_input("Texto (vacío para eliminar):", value=st.session_state.bitacora[fecha_edit][lista_target][idx_tarea])
                col_e1, col_e2 = st.columns(2)
                with col_e1:
                    if st.button("💾 Actualizar", use_container_width=True):
                        if texto_nuevo.strip() == "":
                            st.session_state.bitacora[fecha_edit][lista_target].pop(idx_tarea)
                            st.session_state.bitacora[fecha_edit][done_target].pop(idx_tarea)
                        else:
                            st.session_state.bitacora[fecha_edit][lista_target][idx_tarea] = texto_nuevo
                        guardar_datos(); st.rerun()
                with col_e2:
                    if st.button("❌ Cancelar", use_container_width=True):
                        st.session_state.menu_action = None; st.rerun()
        st.write("---")

    elif st.session_state.menu_action == "planificar":
        st.markdown("### ✏️ Planificar Nueva Tarea")
        fecha_ingresada = st.date_input("Fecha:", datetime.date(2026, 9, 16))
        secciones_disp = ["Plantas Grandes"]
        if st.session_state.config["usar_esquejes"]: secciones_disp.append("Esquejes")
        tipo_tarea = st.selectbox("Sección:", secciones_disp)
        nueva_tarea = st.text_input("Tarea:")
        cb1, cb2 = st.columns(2)
        with cb1:
            if st.button("💾 Guardar Tarea", use_container_width=True):
                if fecha_ingresada not in st.session_state.bitacora:
                    st.session_state.bitacora[fecha_ingresada] = {"tareas_madre": [], "tareas_esqueje": [], "done_m": [], "done_e": []}
                if tipo_tarea == "Plantas Grandes":
                    st.session_state.bitacora[fecha_ingresada]["tareas_madre"].append(nueva_tarea)
                    st.session_state.bitacora[fecha_ingresada]["done_m"].append(False)
                else:
                    st.session_state.bitacora[fecha_ingresada]["tareas_esqueje"].append(nueva_tarea)
                    st.session_state.bitacora[fecha_ingresada]["done_e"].append(False)
                guardar_datos(); st.rerun()
        with cb2:
            if st.button("❌ Cerrar", use_container_width=True):
                st.session_state.menu_action = None; st.rerun()
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
            if tiene_tarea: st.markdown(f"<div style='background-color:{accent_color_fase}; height:5px; border-radius:2px; margin-top:-5px; margin-bottom:10px;'></div>", unsafe_allow_html=True)
            else: st.markdown("<div style='height:5px; margin-top:-5px; margin-bottom:10px;'></div>", unsafe_allow_html=True)

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
                        for i, t in enumerate(data_dia["tareas_madre"]): data_dia["done_m"][i] = st.checkbox(t, value=data_dia["done_m"][i], key=f"m_{fecha_sel}_{i}")
                    else: st.caption("Sin tareas.")
                with col_clones:
                    st.markdown("<div class='card-esqueje'><b>🧬 ESQUEJES (2ª Gen)</b></div>", unsafe_allow_html=True)
                    if data_dia.get("tareas_esqueje"):
                        for i, t in enumerate(data_dia["tareas_esqueje"]): data_dia["done_e"][i] = st.checkbox(t, value=data_dia["done_e"][i], key=f"e_{fecha_sel}_{i}")
                    else: st.caption("Sin tareas.")
            else:
                st.markdown(f"<div class='card-madre' style='border-radius:6px;'><b>🌿 MACETAS ({st.session_state.config['maceta']})</b></div>", unsafe_allow_html=True)
                if data_dia.get("tareas_madre"):
                    for i, t in enumerate(data_dia["tareas_madre"]): data_dia["done_m"][i] = st.checkbox(t, value=data_dia["done_m"][i], key=f"m_{fecha_sel}_{i}")
                else: st.caption("Sin tareas.")
            st.session_state.bitacora[fecha_sel] = data_dia; guardar_datos()
        else: st.info("Día sin tareas.")
        if st.button("❌ Cerrar Tarjeta", use_container_width=True):
            st.session_state.selected_date = None; st.rerun()
