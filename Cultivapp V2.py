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
if "ver_calendario" not in st.session_state:
    st.session_state.ver_calendario = False if not st.session_state.config else True

st.markdown("""
    <style>
    body, p, div, span, label, input, button, select { font-family: 'Arial', sans-serif !important; }
    .card-madre { background-color: #E8F5E9; padding: 12px; border-radius: 6px 6px 0px 0px; border: 1px solid #C8E6C9; color: #2E7D32; }
    .card-esqueje { background-color: #E3F2FD; padding: 12px; border-radius: 0px 0px 6px 6px; border: 1px solid #BBDEFB; color: #0D47A1; }
    .header-banner { background-color: #FAFAFA; padding: 10px; border-radius: 6px; text-align: center; border: 1px solid #E0E0E0; font-weight: bold; color: #333; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

if not st.session_state.ver_calendario:
    st.markdown("### 🪴 Configuración del Cultivo (Alpha 3)")
    col_ini1, col_ini2 = st.columns(2)
    with col_ini1:
        st.markdown("#### ➕ Crear Nuevo Calendario")
        maceta = st.selectbox("Maceta:", ["3L", "5L", "7L", "10L", "15L", "20L"], index=3)
        sustrato = st.selectbox("Sustrato:", ["Cultivate", "Treemix", "Casero"])
        raza = st.selectbox("Raza:", ["Tangie", "Gorilla Ghost"])
        tipo_luz = st.selectbox("Tipo de luz:", ["Led", "Sodio", "Mercurio"])
        potencia = st.selectbox("Potencia (W):", ["150", "200", "250", "300", "350", "400"], index=4)
        usar_esquejes = st.checkbox("Incluir sección de esquejes", value=True)
        if st.button("💾 Inicializar e Ingresar", use_container_width=True):
            st.session_state.config = {"maceta": maceta, "sustrato": sustrato, "raza": raza, "tipo_luz": tipo_luz, "potencia": potencia, "usar_esquejes": usar_esquejes}
            st.session_state.bitacora = {}
            st.session_state.ver_calendario = True
            guardar_datos(); st.rerun()
            
    with col_ini2:
        st.markdown("#### 📂 Cultivo Guardado en Memoria")
        if st.session_state.config:
            st.info(f"Se detectó un cultivo activo de: **{st.session_state.config['raza']}**")
            col_g1, col_g2 = st.columns(2) # CORREGIDO: Añadido el número 2 para evitar el TypeError
            with col_g1:
                if st.button(f"🚀 Entrar a {st.session_state.config['raza']}", use_container_width=True):
                    st.session_state.ver_calendario = True; st.rerun()
            with col_g2:
                if st.button("❌", help="Eliminar este calendario"):
                    st.session_state.menu_action = "confirmar_borrado"
            if "menu_action" in st.session_state and st.session_state.menu_action == "confirmar_borrado":
                st.warning("⚠️ ¿Borrar toda la bitácora?")
                col_conf1, col_conf2 = st.columns(2)
                with col_conf1:
                    if st.button("💥 SÍ, BORRAR", use_container_width=True):
                        st.session_state.config = {}; st.session_state.bitacora = {}; st.session_state.fase = "Vegetativo"; st.session_state.menu_action = None
                        if os.path.exists(DB_FILE): os.remove(DB_FILE)
                        st.success("Cultivo eliminado."); st.rerun()
                with col_conf2:
                    if st.button("Cancelar", use_container_width=True):
                        st.session_state.menu_action = None; st.rerun()
        else: st.caption("No hay ningún calendario guardado.")
    st.stop()

# Proporción fija 20/80 para el panel principal
col_menu, col_main = st.columns([1, 4])

with col_menu:
    st.markdown(f"<div class='header-banner'>🧬 {st.session_state.config['raza']}</div>", unsafe_allow_html=True)
    if st.button("🏠 Inicio", use_container_width=True):
        st.session_state.ver_calendario = False; st.rerun()
    st.write("---")
    if st.button("✏️ Planificar Tarea", use_container_width=True):
        st.session_state.menu_action = "planificar"
    if st.button("📝 Editar Tareas", use_container_width=True):
        st.session_state.menu_action = "editar"
    if st.button("📖 Info Raza", use_container_width=True):
        st.session_state.menu_action = "info"
    st.write("---")
    st.markdown(f"**Fase:** {st.session_state.fase}")
    if st.button("⏱️ Alternar Veg/Flora", use_container_width=True):
        st.session_state.fase = "Floración" if st.session_state.fase == "Vegetativo" else "Vegetativo"
        guardar_datos(); st.rerun()
    if st.session_state.fase == "Vegetativo": st.code("18 hs LUZ / 6 hs OFF")
    else: st.code("12 hs LUZ / 12 hs OFF")
    now_utc = datetime.datetime.utcnow()
    now = now_utc - datetime.timedelta(hours=3)
    st.caption(f"🕒 {now.strftime('%H:%M')} ART")

with col_main:
    if st.session_state.menu_action == "info":
        st.markdown("### 📖 Manual Técnico: Parámetros y Clima")
        if st.session_state.config["raza"] == "Tangie":
            st.write("**Variedad:** Tangie | **Ciclo:** 9 Semanas")
            litros_num = float(st.session_state.config["maceta"].replace("L", ""))
            agua_veg, agua_flo1, agua_flo2 = litros_num * 0.10, litros_num * 0.10, litros_num * 0.15
            t_luz = st.session_state.config.get("tipo_luz", "Led")
            pot = int(st.session_state.config.get("potencia", "350"))
            if t_luz == "Led": dist_lamp = "30 a 40 cm" if pot >= 300 else "25 a 30 cm"
            elif t_luz == "Sodio": dist_lamp = "40 a 50 cm" if pot >= 300 else "30 a 40 cm"
            else: dist_lamp = "45 a 55 cm" if pot >= 300 else "35 a 45 cm"
            tab_veg, tab_flo = st.tabs(["🌱 VEGETATIVO", "🟣 FLORACIÓN"])
            with tab_veg:
                st.write("**Clima:** Temp: 24°C-28°C | Humedad: 55%-70%")
                st.write(f"- **Distancia Luz ({t_luz} {pot}W):** A {dist_lamp} de las punt.")
                st.write(f"- **Agua (10%):** {agua_veg:.1f}L\n- **pH:** 6.0-6.2 | **EC:** 1.0-1.4\n- **Nutrientes:** N + Microvida + Melaza.")
            with tab_flo:
                st.write("**Semanas 1-4 (Stretch):**\n- **Clima:** Temp: 23°C-27°C | Humedad: 50%-60%")
                st.write(f"- **Agua (10%):** {agua_flo1:.1f}L\n- **pH:** 6.2 | **EC:** 1.1-1.3\n- **Nutrientes:** Mínimo N + P + K + Melaza.")
                st.write(f"**Semanas 5-9 (Engorde):**\n- **Clima:** Temp: 20°C-25°C | Humedad: 40%-50%")
                st.write(f"- **Distancia Luz:** A {dist_lamp} de las punt.\n- **Agua (15%):** {agua_flo2:.1f}L\n- **pH:** 6.3-6.5 | **EC:** 1.3-1.6\n- **Nutrientes:** Máximo P + K + Melaza.")
        if st.button("❌ Cerrar Info", use_container_width=True):
            st.session_state.menu_action = None; st.rerun()

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
                        else: st.session_state.bitacora[fecha_edit][lista_target][idx_tarea] = texto_nuevo
                        guardar_datos(); st.rerun()
                with col_e2:
                    if st.button("❌ Cancelar", use_container_width=True):
                        st.session_state.menu_action = None; st.rerun()
            else: st.warning("No hay tareas en esta sección.")
        else: st.info("No hay tareas registradas en esta fecha.")
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
    
    # CORREGIDO: Color fijo en el fondo de botones. No se altera de forma aleatoria
    for idx, fecha in enumerate(dias_septiembre):
        col_target = cols_dias[idx % 7]
        tiene_tarea = fecha in st.session_state.bitacora
        with col_target:
            if st.button(f"{fecha.day}", key=f"day_{fecha.day}_{idx}", use_container_width=True):
                st.session_state.selected_date = fecha
            if tiene_tarea: st.markdown(f"<div style='background-color:#A5D6A7; height:5px; border-radius:2px; margin-top:-5px; margin-bottom:10px;'></div>", unsafe_allow_html=True)
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
                    # CORREGIDO: Texto simplificado a sólo "ESQUEJES"
                    st.markdown("<div class='card-esqueje'><b>🧬 ESQUEJES</b></div>", unsafe_allow_html=True)
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
