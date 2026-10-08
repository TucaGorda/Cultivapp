import streamlit as st
import datetime
import calendar
import json
import os

st.set_page_config(layout="wide", page_title="Cultivapp Alpha 5.0")
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
    st.session_state.selected_date = datetime.date.today()
if "menu_action" not in st.session_state:
    st.session_state.menu_action = None
if "ver_calendario" not in st.session_state:
    st.session_state.ver_calendario = False if not st.session_state.config else True
if "idx_tarea_editar" not in st.session_state:
    st.session_state.idx_tarea_editar = None

st.markdown("""
    <style>
    body, p, div, span, label, input, button, select { font-family: 'Arial', sans-serif !important; }
    .card-madre { background-color: #E8F5E9; padding: 12px; border-radius: 6px 6px 0px 0px; border: 1px solid #C8E6C9; color: #2E7D32; }
    .card-esqueje { background-color: #E3F2FD; padding: 12px; border-radius: 0px 0px 6px 6px; border: 1px solid #BBDEFB; color: #0D47A1; }
    .header-banner { background-color: #FAFAFA; padding: 10px; border-radius: 6px; text-align: center; border: 1px solid #E0E0E0; font-weight: bold; color: #333; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

if not st.session_state.ver_calendario:
    st.markdown("### 🪴 Configuración del Cultivo (Alpha 5.0)")
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
            col_g1, col_g2 = st.columns(2)
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
    st.markdown(f"<div class='header-banner'>🧬 {st.session_state.config['raza'].upper()}</div>", unsafe_allow_html=True)
    if st.button("🏠 INICIO", use_container_width=True):
        st.session_state.ver_calendario = False; st.rerun()
    st.write("---")
    # CORREGIDO: Botones transformados a IMPRENTA MAYÚSCULA
    if st.button("✏️ PLANIFICAR TAREA", use_container_width=True):
        st.session_state.menu_action = "planificar"
    if st.button("📝 EDITAR TAREA", use_container_width=True):
        st.session_state.menu_action = "editar"; st.session_state.idx_tarea_editar = None
    if st.button("📊 REGISTRO", use_container_width=True):
        st.session_state.menu_action = "mediciones"
    if st.button("📖 INFO RAZA", use_container_width=True):
        st.session_state.menu_action = "info"
    st.write("---")
    st.markdown(f"**FASE:** {st.session_state.fase.upper()}")
    if st.button("⏱️ ALTERNAR VEG/FLORA", use_container_width=True):
        st.session_state.fase = "Floración" if st.session_state.fase == "Vegetativo" else "Vegetativo"
        guardar_datos(); st.rerun()
    if st.session_state.fase == "Vegetativo": st.code("18 hs LUZ / 6 hs OFF")
    else: st.code("12 hs LUZ / 12 hs OFF")
    now_utc = datetime.datetime.utcnow()
    now = now_utc - datetime.timedelta(hours=3)
    st.caption(f"🕒 {now.strftime('%H:%M')} ART")

with col_main:
    if st.session_state.menu_action == "info":
        st.markdown("### 📖 MANUAL TÉCNICO: PARAMETROS Y CLIMA")
        raza_act = st.session_state.config["raza"]
        if raza_act == "Tangie": st.write("**VARIEDAD:** TANGIE | **CICLO:** 9 SEMANAS")
        else: st.write("**VARIEDAD:** GORILLA GHOST | **CICLO:** 8 SEMANAS")
        
        litros_num = float(st.session_state.config["maceta"].replace("L", ""))
        agua_veg, agua_flo1, agua_flo2 = litros_num * 0.10, litros_num * 0.10, litros_num * 0.15
        t_luz = st.session_state.config.get("tipo_luz", "Led")
        pot = int(st.session_state.config.get("potencia", "350"))
        if t_luz == "Led": dist_lamp = "30 a 40 cm" if pot >= 300 else "25 a 30 cm"
        elif t_luz == "Sodio": dist_lamp = "40 a 50 cm" if pot >= 300 else "30 a 40 cm"
        else: dist_lamp = "45 a 55 cm" if pot >= 300 else "35 a 45 cm"
        
        tab_veg, tab_flo = st.tabs(["🌱 VEGETATIVO", "🟣 FLORACIÓN"])
        with tab_veg:
            st.write("**CLIMA:** TEMP: 24°C-28°C | HUMEDAD: 55%-70%")
            st.write(f"- **DISTANCIA LUZ ({t_luz.upper()} {pot}W):** A {dist_lamp} DE LAS PUNTAS.")
            st.write(f"- **AGUA (10%):** {agua_veg:.1f}L\n- **pH:** 6.0-6.2 | **EC:** 1.0-1.4\n- **NUTRIENTES:** N + MICROVIDA + MELAZA.")
        with tab_flo:
            sem_f = "1-4"
            sem_e = "5-9" if raza_act == "Tangie" else "5-8"
            st.write(f"**SEMANAS {sem_f} (STRETCH):**\n- **CLIMA:** TEMP: 23°C-27°C | HUMEDAD: 50%-60%\n- **AGUA (10%):** {agua_flo1:.1f}L\n- **pH:** 6.2 | **EC:** 1.1-1.3\n- **NUTRIENTES:** MÍNIMO N + P + K + MELAZA.")
            st.write(f"**SEMANAS {sem_e} (ENGORDE):**\n- **CLIMA:** TEMP: 20°C-25°C | HUMEDAD: 40%-50%")
            st.write(f"- **DISTANCIA LUZ:** A {dist_lamp} DE LAS PUNTAS.\n- **AGUA (15%):** {agua_flo2:.1f}L\n- **pH:** 6.3-6.5 | **EC:** 1.3-1.6\n- **NUTRIENTES:** MÁXIMO P + K + MELAZA.")
        if st.button("❌ CERRAR INFO", use_container_width=True):
            st.session_state.menu_action = None; st.rerun()

    elif st.session_state.menu_action == "mediciones":
        st.markdown("### 📊 REGISTRO DE MEDICIONES (MODO BITÁCORA)")
        # CORREGIDO: Se elimina la caja de fecha horizontal, se usa texto limpio
        st.markdown(f"**SECCIÓN SELECCIONADA:** {st.session_state.selected_date.strftime('%d/%m/%Y')}")
        fecha_med = st.session_state.selected_date
        
        med_existente = fecha_med in st.session_state.bitacora and "ph_in" in st.session_state.bitacora[fecha_med]
        med = st.session_state.bitacora[fecha_med] if fecha_med in st.session_state.bitacora else {}
        
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            ph_in = st.number_input("pH de Entrada:", value=float(med.get("ph_in", 6.2)), step=0.1)
            ec_in = st.number_input("EC de Entrada (Entero):", value=int(med.get("ec_in", 330)), step=10)
        with col_m2:
            ph_out = st.number_input("pH de Salida (Drenaje):", value=float(med.get("ph_out", 6.2)), step=0.1)
            ec_out = st.number_input("EC de Salida (Drenaje Entero):", value=int(med.get("ec_out", 700)), step=10)
            
        col_sm1, col_sm2 = st.columns(2)
        with col_sm1:
            if st.button("💾 GUARDAR MEDICIONES", use_container_width=True):
                if fecha_med not in st.session_state.bitacora:
                    st.session_state.bitacora[fecha_med] = {"tareas_madre": [], "tareas_esqueje": [], "done_m": [], "done_e": []}
                st.session_state.bitacora[fecha_med]["ph_in"] = ph_in; st.session_state.bitacora[fecha_med]["ph_out"] = ph_out
                st.session_state.bitacora[fecha_med]["ec_in"] = ec_in; st.session_state.bitacora[fecha_med]["ec_out"] = ec_out
                guardar_datos(); st.success("¡Mediciones guardadas!"); st.rerun()
        with col_sm2:
            if med_existente:
                if st.button("💥 ELIMINAR REGISTRO", use_container_width=True):
                    for k in ["ph_in", "ph_out", "ec_in", "ec_out"]:
                        if k in st.session_state.bitacora[fecha_med]: del st.session_state.bitacora[fecha_med][k]
                    if not st.session_state.bitacora[fecha_med].get("tareas_madre") and not st.session_state.bitacora[fecha_med].get("tareas_esqueje"):
                        del st.session_state.bitacora[fecha_med]
                    guardar_datos(); st.success("¡Mediciones eliminadas!"); st.rerun()
            else:
                if st.button("❌ CERRAR", key="c_med", use_container_width=True):
                    st.session_state.menu_action = None; st.rerun()
        st.write("---")

    elif st.session_state.menu_action == "planificar":
        st.markdown("### ✏️ PLANIFICAR NUEVA TAREA")
        # CORREGIDO: Texto limpio de fecha sin barra horizontal
        st.markdown(f"**SECCIÓN SELECCIONADA:** {st.session_state.selected_date.strftime('%d/%m/%Y')}")
        fecha_ingresada = st.session_state.selected_date
        
        # CORREGIDO: Unificación estética usando botones circulares (radio) en vez de selectbox
        secciones_disp = ["Plantas Grandes", "Esquejes"] if st.session_state.config["usar_esquejes"] else ["Plantas Grandes"]
        tipo_tarea = st.radio("Sección a planificar:", secciones_disp, horizontal=True)
        nueva_tarea = st.text_input("Descripción de la tarea:")
        
        cb1, cb2 = st.columns(2)
        with cb1:
            if st.button("💾 GUARDAR TAREA", use_container_width=True):
                if fecha_ingresada not in st.session_state.bitacora:
                    st.session_state.bitacora[fecha_ingresada] = {"tareas_madre": [], "tareas_esqueje": [], "done_m": [], "done_e": []}
                if tipo_tarea == "Plantas Grandes":
                    st.session_state.bitacora[fecha_ingresada]["tareas_madre"].append(nueva_tarea)
                    st.session_state.bitacora[fecha_ingresada]["done_m"].append(False)
                else:
                    st.session_state.bitacora[fecha_ingresada]["tareas_esqueje"].append(nueva_tarea)
                    st.session_state.bitacora[fecha_ingresada]["done_e"].append(False)
                guardar_datos(); st.session_state.menu_action = None; st.rerun() # CORREGIDO: Cierra la opción automáticamente al guardar
        with cb2:
            if st.button("❌ CERRAR", use_container_width=True): st.session_state.menu_action = None; st.rerun()
        st.write("---")

    elif st.session_state.menu_action == "editar":
        st.markdown("### 📝 MODIFICAR O ELIMINAR TAREA")
        st.markdown(f"**SECCIÓN SELECCIONADA:** {st.session_state.selected_date.strftime('%d/%m/%Y')}")
        fecha_edit = st.session_state.selected_date
        
        if fecha_edit in st.session_state.bitacora:
            secciones_disp = ["Plantas Grandes", "Esquejes"] if st.session_state.config["usar_esquejes"] else ["Plantas Grandes"]
            tipo = st.radio("Sección a modificar:", secciones_disp, horizontal=True)
            lista_target = "tareas_madre" if tipo == "Plantas Grandes" else "tareas_esqueje"
            done_target = "done_m" if tipo == "Plantas Grandes" else "done_e"
            
            tareas_lista = st.session_state.bitacora[fecha_edit][lista_target]
            if tareas_lista:
                st.markdown("**Selecciona la tarea haciendo clic en su botón:**")
                # CORREGIDO: Se quita la barra desplegable, se lista como botones directos con tilde verde ✔️
                for idx, t_text in enumerate(tareas_lista):
                    label_boton = f"✔️ {t_text}" if st.session_state.idx_tarea_editar == idx else t_text
                    if st.button(label_boton, key=f"btn_list_{idx}", use_container_width=True):
                        st.session_state.idx_tarea_editar = idx
                
                if st.session_state.idx_tarea_editar is not None and st.session_state.idx_tarea_editar < len(tareas_lista):
                    idx_sel = st.session_state.idx_tarea_editar
                    texto_nuevo = st.text_input("Modifica el texto seleccionado (vacío para eliminar):", value=tareas_lista[idx_sel])
                    col_e1, col_e2 = st.columns(2)
                    with col_e1:
                        if st.button("💾 ACTUALIZAR", use_container_width=True):
                            if texto_nuevo.strip() == "":
                                st.session_state.bitacora[fecha_edit][lista_target].pop(idx_sel)
                                st.session_state.bitacora[fecha_edit][done_target].pop(idx_sel)
                                if not st.session_state.bitacora[fecha_edit].get("tareas_madre") and not st.session_state.bitacora[fecha_edit].get("tareas_esqueje") and "ph_in" not in st.session_state.bitacora[fecha_edit]:
                                    del st.session_state.bitacora[fecha_edit]
                            else: st.session_state.bitacora[fecha_edit][lista_target][idx_sel] = texto_nuevo
                            st.session_state.idx_tarea_editar = None; guardar_datos(); st.rerun()
                    with col_e2:
                        if st.button("❌ CANCELAR", use_container_width=True): st.session_state.menu_action = None; st.rerun()
            else: st.warning("No hay tareas en esta sección.")
        else: st.info("No hay tareas.")
        st.write("---")

    hoy = datetime.date.today()
    meses_nombres = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    st.markdown(f"<h2 style='text-align: center; color: #333;'>📅 {meses_nombres[hoy.month - 1].upper()} {hoy.year}</h2>", unsafe_allow_html=True)
    
    cal = calendar.Calendar(firstweekday=0)
    semanas_mes = cal.monthdatescalendar(hoy.year, hoy.month)
    
    cols_header = st.columns(7)
    dias_semana = ["LUN", "MAR", "MIÉ", "JUE", "VIE", "SÁB", "DOM"]
    for idx, nombre_dia in enumerate(dias_semana):
        cols_header[idx].markdown(f"<p style='text-align:center; font-weight:600; margin-bottom:5px;'>{nombre_dia}</p>", unsafe_allow_html=True)
    
    for b_semana in semanas_mes:
        cols_dias = st.columns(7)
        for idx, fecha in enumerate(b_semana):
            col_target = cols_dias[idx]
            if fecha.month == hoy.month:
                # CORREGIDO: Lógica del semáforo inteligente de colores (Verde=Grandes, Azul=Esquejes, 50/50=Ambos)
                tiene_m = fecha in st.session_state.bitacora and len(st.session_state.bitacora[fecha].get("tareas_madre", [])) > 0
                tiene_e = fecha in st.session_state.bitacora and (len(st.session_state.bitacora[fecha].get("tareas_esqueje", [])) > 0 or "ph_in" in st.session_state.bitacora[fecha])
                with col_target:
                    if st.button(f"{fecha.day}", key=f"day_{fecha.day}_{fecha.month}_{idx}", use_container_width=True):
                        st.session_state.selected_date = fecha
                    if tiene_m and tiene_e:
                        st.markdown("<div style='display:flex; height:5px; border-radius:2px; margin-top:-5px; margin-bottom:10px;'><div style='background-color:#A5D6A7; flex:1;'></div><div style='background-color:#BBDEFB; flex:1;'></div></div>", unsafe_allow_html=True)
                    elif tiene_m: st.markdown("<div style='background-color:#A5D6A7; height:5px; border-radius:2px; margin-top:-5px; margin-bottom:10px;'></div>", unsafe_allow_html=True)
                    elif tiene_e: st.markdown("<div style='background-color:#BBDEFB; height:5px; border-radius:2px; margin-top:-5px; margin-bottom:10px;'></div>", unsafe_allow_html=True)
                    else: st.markdown("<div style='height:5px; margin-top:-5px; margin-bottom:10px;'></div>", unsafe_allow_html=True)
            else:
                with col_target: st.write("")

    if st.session_state.selected_date:
        fecha_sel = st.session_state.selected_date
        st.write("---")
        st.markdown(f"### 📋 REGISTROS DEL DÍA: {fecha_sel.strftime('%d/%m/%Y')}")
        if fecha_sel in st.session_state.bitacora:
            data_dia = st.session_state.bitacora[fecha_sel]
            if "ph_in" in data_dia:
                st.markdown(f"📊 **MEDICIONES:** Entrada: pH {data_dia['ph_in']} / EC {data_dia['ec_in']} | Salida: pH {data_dia['ph_out']} / EC {data_dia['ec_out']}")
            if st.session_state.config["usar_esquejes"]:
                col_madres, col_clones = st.columns(2)
                with col_madres:
                    st.markdown(f"<div class='card-madre'><b>🌿 MACETAS ({st.session_state.config['maceta']})</b></div>", unsafe_allow_html=True)
                    if data_dia.get("tareas_madre"):
                        for i, t in enumerate(data_dia["tareas_madre"]): data_dia["done_m"][i] = st.checkbox(t, value=data_dia["done_m"][i], key=f"m_{fecha_sel}_{i}")
                    else: st.caption("Sin tareas.")
                with col_clones:
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
        else: st.info("Día sin registros.")
        if st.button("❌ CERRAR TARJETA", use_container_width=True):
            st.session_state.selected_date = datetime.date.today(); st.rerun()

