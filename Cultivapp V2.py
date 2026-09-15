import streamlit as st
import datetime

st.set_page_config(layout="wide", page_title="Cultivapp Alpha 2")

if "fase" not in st.session_state:
    st.session_state.fase = "Vegetativo"
if "selected_date" not in st.session_state:
    st.session_state.selected_date = None
if "fuente_gotica" not in st.session_state:
    st.session_state.fuente_gotica = True

if st.session_state.fase == "Vegetativo":
    primary_color = "#E8F5E9"
    accent_color = "#A5D6A7"
else:
    primary_color = "#F3E5F5"
    accent_color = "#CE93D8"

font_class = "gothic-font" if st.session_state.fuente_gotica else "clean-font"

st.markdown(f"""
    <style>
    @import url('https://googleapis.com');
    .gothic-font {{ font-family: 'Cinzel', serif !important; }}
    .clean-font {{ font-family: 'Inter', sans-serif !important; }}
    .card-madre {{ background-color: #E8F5E9; padding: 15px; border-radius: 8px 8px 0px 0px; border: 1px solid #C8E6C9; color: #2E7D32; }}
    .card-esqueje {{ background-color: #E3F2FD; padding: 15px; border-radius: 0px 0px 8px 8px; border: 1px solid #BBDEFB; color: #0D47A1; }}
    </style>
""", unsafe_allow_html=True)

if "bitacora" not in st.session_state:
    st.session_state.bitacora = {
        datetime.date(2026, 9, 11): {"tareas_madre": ["Trasplantar a 10L 🪴", "Regar con Treemix + Under + Melaza 🧪"], "tareas_esqueje": ["Cortar 6 esquejes ✂️", "Aplicar King Clon y domo 🧬"], "done_m": [False, False], "done_e": [False, False]},
        datetime.date(2026, 9, 14): {"tareas_madre": ["Comprar Ph Down Namasté 🛍️"], "tareas_esqueje": ["Controlar humedad del domo 💧"], "done_m": [False], "done_e": [False]},
        datetime.date(2026, 9, 16): {"tareas_madre": ["Riego control (750ml agua sola) 💧", "Ph Down Namasté a 6.2 🧪"], "tareas_esqueje": ["Ventilar botellas 5 min 💨"], "done_m": [False, False], "done_e": [False]},
        datetime.date(2026, 9, 17): {"tareas_madre": ["Tejer Red de hilo de fiambre (5x5) 🕸️", "Guiar ramas horizontalmente 🌿"], "tareas_esqueje": ["Monitorear humedad 🌡️"], "done_m": [False, False], "done_e": [False]},
        datetime.date(2026, 9, 19): {"tareas_madre": ["Verificar turgencia 👀", "Timer directo a 12/12 ⏱️"], "tareas_esqueje": ["Buscar raíces blancas 🔍"], "done_m": [False, False], "done_e": [False]},
        datetime.date(2026, 9, 26): {"tareas_madre": ["Guiar stretch 🕸️"], "tareas_esqueje": ["Trasplantar a maceta chica 🎉"], "done_m": [False], "done_e": [False]}
    }

# CORREGIDO: Se especifica el número 2 para indicar dos columnas principales
col_menu, col_main = st.columns(2)

with col_menu:
    st.markdown(f"<h3 class='{font_class}'>Cultivapp 🍁</h3>", unsafe_allow_html=True)
    st.caption("Alpha v2.0")
    st.write("---")
    if st.button("📝 Editar Tareas", use_container_width=True):
        st.session_state.menu_action = "editar"
    if st.button("✏️ Planificar Día", use_container_width=True):
        st.session_state.menu_action = "planificar"
    if st.button("➕ Parámetros", use_container_width=True):
        st.session_state.menu_action = "parametros"
    st.write("---")
    st.markdown(f"**Fase:** {st.session_state.fase}")
    if st.button("⏱️ Alternar Veg/Flora", use_container_width=True):
        st.session_state.fase = "Floración" if st.session_state.fase == "Vegetativo" else "Vegetativo"
        st.rerun()
    now_utc = datetime.datetime.utcnow()
    now = now_utc - datetime.timedelta(hours=3)
    st.caption(f"🕒 Hora local: {now.strftime('%H:%M')} ART")
    if st.session_state.fase == "Vegetativo":
        st.code("18 hs LUZ / 6 hs OFF")
    else:
        st.code("12 hs LUZ / 12 hs OFF")
    st.write("---")
    if st.button("🔤 Tipografía", use_container_width=True):
        st.session_state.fuente_gotica = not st.session_state.fuente_gotica
        st.rerun()

with col_main:
    if "menu_action" in st.session_state:
        if st.session_state.menu_action == "editar":
            st.markdown(f"<h4 class='{font_class}'>📝 Editar Tareas</h4>", unsafe_allow_html=True)
            fecha_edit = st.date_input("Fecha a modificar:", datetime.date(2026, 9, 11))
            if fecha_edit in st.session_state.bitacora:
                tipo = st.radio("Sección:", ["Plantas Grandes (Madre)", "Esquejes"])
                lista_target = "tareas_madre" if tipo == "Plantas Grandes (Madre)" else "tareas_esqueje"
                if st.session_state.bitacora[fecha_edit][lista_target]:
                    idx_tarea = st.selectbox("Selecciona tarea:", range(len(st.session_state.bitacora[fecha_edit][lista_target])), format_func=lambda x: st.session_state.bitacora[fecha_edit][lista_target][x])
                    texto_nuevo = st.text_input("Nuevo texto:", value=st.session_state.bitacora[fecha_edit][lista_target][idx_tarea])
                    col_e1, col_e2 = st.columns(2)
                    with col_e1:
                        if st.button("💾 Actualizar", use_container_width=True):
                            st.session_state.bitacora[fecha_edit][lista_target][idx_tarea] = texto_nuevo
                            st.success("¡Actualizado!")
                            st.rerun()
                    with col_e2:
                        if st.button("❌ Cerrar Editor", use_container_width=True):
                            del st.session_state.menu_action
                            st.rerun()
                else:
                    st.warning("Sin tareas en esta sección.")
            else:
                st.info("No hay tareas en esta fecha.")
            st.write("---")

        elif st.session_state.menu_action == "planificar":
            st.markdown(f"<h4 class='{font_class}'>✏️ Planificar Nueva</h4>", unsafe_allow_html=True)
            fecha_ingresada = st.date_input("Fecha:", datetime.date(2026, 9, 15))
            tipo_tarea = st.selectbox("Sección:", ["Plantas Grandes (Madre)", "Esquejes"])
            nueva_tarea = st.text_input("Tarea:")
            cb1, cb2 = st.columns(2)
            with cb1:
                if st.button("💾 Guardar", use_container_width=True):
                    if fecha_ingresada not in st.session_state.bitacora:
                        st.session_state.bitacora[fecha_ingresada] = {"tareas_madre": [], "tareas_esqueje": [], "done_m": [], "done_e": []}
                    if tipo_tarea == "Plantas Grandes (Madre)":
                        st.session_state.bitacora[fecha_ingresada]["tareas_madre"].append(nueva_tarea)
                        st.session_state.bitacora[fecha_ingresada]["done_m"].append(False)
                    else:
                        st.session_state.bitacora[fecha_ingresada]["tareas_esqueje"].append(nueva_tarea)
                        st.session_state.bitacora[fecha_ingresada]["done_e"].append(False)
                    st.success("¡Agregado!")
            with cb2:
                if st.button("❌ Cerrar", key="c_plan", use_container_width=True):
                    del st.session_state.menu_action
                    st.rerun()
            st.write("---")

        elif st.session_state.menu_action == "parametros":
            st.markdown(f"<h4 class='{font_class}'>➕ Parámetros actuales</h4>", unsafe_allow_html=True)
            cp1, cp2 = st.columns(2)
            with cp1:
                st.text_input("Raza:", value="Tangie", disabled=True)
                st.text_input("Sustrato:", value="Cultivate Premium", disabled=True)
            with cp2:
                st.text_input("Espacio:", value="0.80 x 0.80 x 1.80 m", disabled=True)
                st.text_input("Luz:", value="LED Full Spectrum 350W", disabled=True)
            if st.button("❌ Cerrar", key="c_param", use_container_width=True):
                del st.session_state.menu_action
                st.rerun()
            st.write("---")

    hoy = datetime.date.today()
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    st.markdown(f"<h2 class='{font_class}' style='text-align: center;'>📅 {meses[hoy.month - 1]} 2026</h2>", unsafe_allow_html=True)
    
    dias_septiembre = [datetime.date(2026, 9, d) for d in range(7, 28)]
    cols_dias = st.columns(7)
    dias_semana = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
    
    for idx, nombre_dia in enumerate(dias_semana):
        cols_dias[idx].markdown(f"<p style='text-align:center; font-weight:600;'>{nombre_dia}</p>", unsafe_allow_html=True)
        
    for idx, fecha in enumerate(dias_septiembre):
        col_target = cols_dias[idx % 7]
        tiene_tarea = fecha in st.session_state.bitacora
        with col_target:
            if st.button(f"{fecha.day}", key=f"day_{fecha.day}_{idx}", use_container_width=True):
                st.session_state.selected_date = fecha
            if tiene_tarea:
                st.markdown(f"<div style='background-color:{accent_color}; height:5px; border-radius:2px; margin-top:-5px; margin-bottom:10px;'></div>", unsafe_allow_html=True)
            else:
                st.markdown("<div style='height:5px; margin-top:-5px; margin-bottom:10px;'></div>", unsafe_allow_html=True)

    if st.session_state.selected_date:
        fecha_sel = st.session_state.selected_date
        st.write("---")
        st.markdown(f"<h3 class='{font_class}'>📋 Tareas del {fecha_sel.strftime('%d/%m/%Y')}</h3>", unsafe_allow_html=True)
        
        if fecha_sel in st.session_state.bitacora:
            data_dia = st.session_state.bitacora[fecha_sel]
            col_madres, col_clones = st.columns(2)
            with col_madres:
                st.markdown("<div class='card-madre'><b>🌿 PLANTAS GRANDES (10L)</b></div>", unsafe_allow_html=True)
                if data_dia["tareas_madre"]:
                    for i, t in enumerate(data_dia["tareas_madre"]):
                        data_dia["done_m"][i] = st.checkbox(t, value=data_dia["done_m"][i], key=f"m_{fecha_sel}_{i}")
                        
                else:
                    st.caption("Sin tareas.")
            with col_clones:
                st.markdown("<div class='card-esqueje'><b>🧬 ESQUEJES (2ª Gen)</b></div>", unsafe_allow_html=True)
                if data_dia["tareas_esqueje"]:
                    for i, t in enumerate(data_dia["tareas_esqueje"]):
                        data_dia["done_e"][i] = st.checkbox(t, value=data_dia["done_e"][i], key=f"e_{fecha_sel}_{i}")
                else:
                    st.caption("Sin tareas.")
            st.session_state.bitacora[fecha_sel] = data_dia
        else:
            st.info("Día sin tareas.")
            
        if st.button("❌ Cerrar Tarjeta", use_container_width=True):
            st.session_state.selected_date = None
            st.rerun()
