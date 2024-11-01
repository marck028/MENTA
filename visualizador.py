import streamlit as st
import pandas as pd
import plotly.express as px
import calendar

# Cargar el archivo de Excel predeterminado
ruta_archivo = "C:\\Users\\Marco\\Documents\\UNIVERSIDAD\\MENTA\\DATOS CBBA.xlsx"
df = pd.read_excel(ruta_archivo)

# Limpiar nombres de columnas
df.columns = df.columns.str.strip()  # Eliminar espacios en blanco

# Convertir la columna 'FECHA' a tipo datetime
df['FECHA'] = pd.to_datetime(df['FECHA'], format='%d/%m/%Y', errors='coerce')

# Definir el diccionario de menú con categorías y productos
menu = {
        "BURGERS": [
            "QUINOA BURGER", "CAÑAHUA BURGER", "CHICKPEA BURGER", "MORENA BURGER",
            "LENTEJA BURGER", "GREEN FILETE", "MINI BURGER", "TARWI BURGUER"
        ],
        "ENSALADAS": [
            "FALAFEL BOWL", "JALISCO BOWL", "MEDITERRANEA BOWL", "BUDDHA BOWL",
            "FALAFEL BOWL PEQUEÑO", "JALISCO BOWL PEQUEÑO", "BUDDHA BOWL PEQUEÑO", "MEDITERRANEA BOWL PEQUEÑO"
        ],
        "ESPECIALES": [
            "PIQUE MACHO", "VEGANCUCHO", "VEGAN FRIED CHICKEN", "VEGGIE WINGS", "SILPANCHO VEGGIE",
            "NO TUNA SANDWICH", "TRANCAPECHO", "CHAMPIÑON SANDWICH", "PANCHITO VEGGIE"
        ],
        "ALMUERZOS DIARIOS": [
            "ALMUERZO COMPLETO", "SOPA", "SEGUNDO", "ENTRADA", "BUFFET DE ENSALADAS",
            "ALMUERZO + BUFFET DE ENSALADAS", "SAB. ALMUERZO ESPECIAL COMPLETO", "SAB. ALMUERZO ESPECIAL SEGUNDO",
            "SAB. ALMUERZO ESPECIAL SOPA", "CONSUMO PENSIONADO COMPLETO SAB.", "CONSUMO PENSIONADO SEGUNDO SAB."
        ],
        "BEBIDAS FRIAS": [
            "CITRUS FRESA", "SKINNY", "PANAMA", "PIMENTA", "MENTA", "JUGO DE TEMPORADA", "FULL CITRUS"
        ],
        "OTRAS BEBIDAS": [
            "AGUA SIN GAS", "AGUA CON GAS", "AGUA CON GAS CON LIMON", "INFUSION DE HIERBAS",
            "CERVEZA PROST LAGER 500 ML", "CERVEZA PROST WIESSBIER 500 ML", "CHUFLAY O MOJITO VAS"
        ],
        "HELADOS": [
            "BROWNIES", "PASTEL DE ZANAHORIA", "TIRAMISU", "HELADO ARTESANAL", "POSTRE ESPECIAL"
        ],
        "PLANES": [
            "ALMUERZO SEMANAL", "SEGUNDO SEMANAL", "ALMUERZO MENSUAL", "SEGUNDO MENSUAL",
            "PLAN FIT SEMANAL", "PLAN FIT MENSUAL", "FULL GREEN", "PLAN MENSUAL 400"
        ],
        "COMBOS PROMOCIONES": [
            "COMBO HAMBURGUESA DOBLE LENTEJA", "COMBO HAMBURGUESA DOBLE GARBANZO", "COMBO HAMBURGUESA DOBLE QUINUA",
            "COMBO HAMBURGUESA DOBLE MORENA", "COMBO HAMBURGUESA DOBLE CAÑAHUA", "COMBO BURGER 2X1 (SIN PAPAS)",
            "COMBO HAMBURGUESA 3X2", "BURGUER + JUGO", "COMBO VEGGIE WING 2X49", "SOLO BURGUER QUINUA",
            "BURGUER QUINUA+PAPA GOURMET", "BURGUER QUINUA+PAPAS FRITAS", "BURGUER QUINUA+PAPA GOURMET+JUGO",
            "BURGUER QUINUA+PAPA FRITA+JUGO", "BURGUER CAÑAHUA+PAPA GOURMET", "BURGUER CAÑAHUA+PAPAS FRITAS",
            "BURGUER CAÑAHUA+PAPA GOURMET+JUGO", "BURGUER CAÑAHUA+PAPA FRITA+JUGO", "SOLO BURGUER CHICKPEA",
            "BURGUER CHICKPEA+PAPA GOURMET", "BURGUER CHICKPEA+PAPA FRITA", "BURGUER CHICKPEA+PAPA GOURMET+JUGO",
            "BURGUER CHICKPEA+PAPA FRITA+JUGO", "SOLO BURGUER MORENA", "BURGUER MORENA+PAPA GOURMET",
            "BURGUER MORENA+PAPA FRITA", "BURGUER MORENA+PAPA GOURMET+JUGO", "BURGUER MORENA+PAPA FRITA+JUGO",
            "SOLO BURGUER LENTEJA", "BURGUER LENTEJA+PAPA GOURMET", "BURGUER LENTEJA+PAPA FRITA",
            "BURGUER LENTEJA+PAPA GOURMET+JUGO", "BURGUER LENTEJA+PAPA FRITA+JUGO", "SOLO BURGUER TARWI",
            "BURGUER TARWI+PAPA GOURMET", "BURGUER TARWI+PAPA FRITA", "BURGUER TARWI+PAPA GOURMET+JUGO",
            "BURGUER TARWI+PAPA FRITA+JUGO"
        ],
        "OTROS": [
            "PORCION EXTRA-FALAFEL", "PAPITAS C/SALSA BLANCA", "PAPAS FRITAS", "PORCION HUEVO",
            "PORCION HAMBURGUESA", "DESECHABLE 1Bs", "DESECHABLE 3Bs", "DESECHABLE 5Bs"
        ]
    }

# Crear una barra lateral para la selección de filtros
st.sidebar.title("Filtros")

# Selección de sucursales (permite seleccionar varias)
sucursales = df['Sucursal'].unique()  # Obtener las sucursales únicas del archivo
sucursales_seleccionadas = st.sidebar.multiselect("Selecciona una o más sucursales:", sucursales)

# Selección de categorías
categorias_seleccionadas = st.sidebar.multiselect("Selecciona una o más categorías:", list(menu.keys()))

# Inicializar un diccionario para almacenar los productos seleccionados por categoría
productos_seleccionados_dict = {}

# Crear un multiselect para cada categoría seleccionada
for categoria in categorias_seleccionadas:
    productos = menu[categoria]  # Obtener productos de la categoría seleccionada
    productos_seleccionados_dict[categoria] = st.sidebar.multiselect(f"Selecciona uno o más productos de la categoría {categoria}:", productos)

# Aplanar la lista de productos seleccionados
productos_seleccionados_final = [producto for productos in productos_seleccionados_dict.values() for producto in productos]

# Selector de meses
meses = df['FECHA'].dt.strftime('%B').unique()  # Obtener nombres de meses únicos
meses_seleccionados = st.sidebar.multiselect("Selecciona uno o más meses:", meses)

# Selector de día de la semana
dias_semana = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
dias_seleccionados = st.sidebar.multiselect("Selecciona uno o más días de la semana:", dias_semana)

# Aplicar filtros seleccionados
if sucursales_seleccionadas and meses_seleccionados and productos_seleccionados_final:
    # Filtrar el DataFrame por las sucursales, meses, productos, y días seleccionados
    df_filtrado = df[
        (df['Sucursal'].isin(sucursales_seleccionadas)) &
        (df['FECHA'].dt.strftime('%B').isin(meses_seleccionados)) &
        (df['Producto'].isin(productos_seleccionados_final))
    ]

    if dias_seleccionados:
        df_filtrado = df_filtrado[df_filtrado['FECHA'].dt.day_name().isin(dias_seleccionados)]

    # Mostrar los datos filtrados
    st.write(f"Datos filtrados para las sucursales: {', '.join(sucursales_seleccionadas)}, "
             f"meses: {', '.join(meses_seleccionados)}, "
             f"productos: {', '.join(productos_seleccionados_final)} y días: {', '.join(dias_seleccionados)}")
    st.write(df_filtrado)


    # Gráfico de barras de ventas por fecha
    st.write("#### Gráfico de barras - Ventas por fecha")
    ventas_por_fecha = df_filtrado.groupby(['FECHA', 'Sucursal'])['VALOR'].sum().reset_index()
    fig_bar_ventas = px.bar(ventas_por_fecha, x='FECHA', y='VALOR', color='Sucursal', title='Ventas por Fecha',
                            labels={'FECHA': 'Fecha', 'VALOR': 'Total Vendido', 'Sucursal': 'Sucursal'})
    fig_bar_ventas.update_layout(dragmode='zoom')
    st.plotly_chart(fig_bar_ventas, use_container_width=True)

    # Gráfico de líneas de cantidad de productos vendidos por fecha, separados por producto y sucursal
    st.write("#### Gráfico de líneas - Cantidad de productos vendidos por fecha y sucursal")
    cantidad_por_fecha_producto = df_filtrado.groupby(['FECHA', 'Producto', 'Sucursal'])['CANTIDAD'].sum().reset_index()
    fig_lineas_cantidad = px.line(cantidad_por_fecha_producto, x='FECHA', y='CANTIDAD', color='Producto', line_dash='Sucursal',
                                  title='Cantidad de Productos Vendidos por Fecha',
                                  labels={'FECHA': 'Fecha', 'CANTIDAD': 'Cantidad Vendida', 'Producto': 'Producto', 'Sucursal': 'Sucursal'})
    fig_lineas_cantidad.update_layout(dragmode='zoom')
    st.plotly_chart(fig_lineas_cantidad, use_container_width=True)

    # Gráfico circular de ventas por producto y sucursal
    st.write("#### Gráficos circulares - Ventas por producto y sucursal")

    # Verificar que haya al menos una sucursal seleccionada
    if sucursales_seleccionadas:
        for sucursal in sucursales_seleccionadas:
            # Filtrar las ventas por la sucursal actual
            ventas_por_producto_sucursal = df_filtrado[df_filtrado['Sucursal'] == sucursal].groupby('Producto')['VALOR'].sum().reset_index()
            
            # Verificar que haya datos para esta sucursal
            if not ventas_por_producto_sucursal.empty:
                fig_pie_ventas = px.pie(ventas_por_producto_sucursal, names='Producto', values='VALOR', 
                                        title=f'Porcentaje de Ventas por Producto en {sucursal}')
                st.plotly_chart(fig_pie_ventas, use_container_width=True)
            else:
                st.write(f"No hay datos de ventas para la sucursal {sucursal}.")
    else:
        st.write("Por favor, seleccione al menos una sucursal para mostrar los gráficos.")

    # Gráfico de barras agrupado por producto, mes y sucursal
    st.write("#### Gráfico de barras - Valor total generado por producto, mes y sucursal")
    df_filtrado['Mes'] = df_filtrado['FECHA'].dt.strftime('%B')
    valor_por_producto_mes = df_filtrado.groupby(['Mes', 'Producto', 'Sucursal'])['VALOR'].sum().reset_index()
    fig_bar_producto_mes = px.bar(valor_por_producto_mes, x='Mes', y='VALOR', color='Producto', facet_col='Sucursal',
                                  barmode='group', title='Valor Total por Producto por Mes y Sucursal',
                                  labels={'Mes': 'Mes', 'VALOR': 'Total Vendido', 'Producto': 'Producto'})
    fig_bar_producto_mes.update_layout(dragmode='zoom')
    st.plotly_chart(fig_bar_producto_mes, use_container_width=True)

# Filtros de sucursal y mes
sucursales_seleccionadas = st.multiselect("Seleccione las sucursales", options=df['Sucursal'].unique())

# Asegúrate de que la columna 'FECHA' esté en formato datetime
df['FECHA'] = pd.to_datetime(df['FECHA'], errors='coerce')

# Extraer el nombre del mes en texto y crear una nueva columna llamada 'Mes'
df['Mes'] = df['FECHA'].dt.month_name()

# Seleccionar los meses con nombres literales
meses_seleccionados = st.multiselect("Seleccione los meses", options=df['Mes'].unique())

# Filtrar los datos según sucursal y mes seleccionados
df_filtrado = df[df['Sucursal'].isin(sucursales_seleccionadas) & df['Mes'].isin(meses_seleccionados)]

# Verificar que haya datos después del filtrado
if df_filtrado.empty:
    st.write("No hay datos disponibles para las sucursales y meses seleccionados.")
else:
    # Graficar los 10 platos más vendidos por cada sucursal seleccionada
    for sucursal in sucursales_seleccionadas:
        st.write(f"### Sucursal: {sucursal}")

        # Filtrar los datos por sucursal
        ventas_sucursal = df_filtrado[df_filtrado['Sucursal'] == sucursal]

        # Agrupar y ordenar por cantidad para obtener los 10 platos más vendidos
        platos_mas_vendidos = ventas_sucursal.groupby('Producto')['CANTIDAD'].sum().nlargest(10).reset_index()
        fig_mas_vendidos = px.bar(platos_mas_vendidos, x='Producto', y='CANTIDAD',
                                  title=f"10 Platos Más Vendidos en {sucursal}",
                                  labels={'CANTIDAD': 'Cantidad Vendida'}, color='Producto')
        st.plotly_chart(fig_mas_vendidos, use_container_width=True)

        # Agrupar y ordenar por cantidad para obtener los 10 platos menos vendidos
        platos_menos_vendidos = ventas_sucursal.groupby('Producto')['CANTIDAD'].sum().nsmallest(10).reset_index()
        fig_menos_vendidos = px.bar(platos_menos_vendidos, x='Producto', y='CANTIDAD',
                                    title=f"10 Platos Menos Vendidos en {sucursal}",
                                    labels={'CANTIDAD': 'Cantidad Vendida'}, color='Producto')
        st.plotly_chart(fig_menos_vendidos, use_container_width=True)
        
# Limpiar nombres de columnas
df.columns = df.columns.str.strip()  # Eliminar espacios en blanco

# Convertir la columna 'FECHA' a tipo datetime
df['FECHA'] = pd.to_datetime(df['FECHA'], format='%d/%m/%Y', errors='coerce')

# Crear una nueva columna para el mes en formato 'YYYY-MM'
df['Mes'] = df['FECHA'].dt.to_period('M').astype(str)

# Agrupar por mes y sucursal para calcular el valor total
valores_por_sucursal = df.groupby(['Mes', 'Sucursal'])['VALOR'].sum().reset_index()

# Crear el gráfico de líneas
fig = px.line(
    valores_por_sucursal,
    x='Mes',
    y='VALOR',
    color='Sucursal',
    title='Valor Generado por Sucursal según el Mes',
    labels={'VALOR': 'Valor Total', 'Mes': 'Mes'},
    markers=True
)

# Mostrar el gráfico en Streamlit
st.plotly_chart(fig)

df['Categoría'] = df['Producto'].apply(lambda x: next((cat for cat, productos in menu.items() if x in productos), 'OTROS'))

# Filtros de mes y sucursal
st.sidebar.header("Filtros")

# Obtener los nombres de los meses
meses = list(calendar.month_name)[1:]  # Excluir el primer elemento que es una cadena vacía

# Selección de mes
mes_nombre = st.sidebar.selectbox("Seleccionar Mes", meses)
mes = meses.index(mes_nombre) + 1  # Convertir el nombre del mes a su número correspondiente

# Selección de sucursal
sucursal = st.sidebar.selectbox("Seleccionar Sucursal", df['Sucursal'].unique())

# Filtrar el DataFrame según los filtros seleccionados
df_filtrado = df[(df['FECHA'].dt.month == mes) & (df['Sucursal'] == sucursal)]

# Calcular la cantidad total por categoría y el total general
totales_por_categoria = df_filtrado.groupby('Categoría')['CANTIDAD'].sum()
total_general = totales_por_categoria.sum()

# Calcular el porcentaje de cada categoría en comparación con el total
porcentajes_por_categoria = (totales_por_categoria / total_general) * 100

# Gráficos de torta para cada categoría vs. todas las categorías
for categoria in porcentajes_por_categoria.index:
    fig = px.pie(
        names=["Otras Categorías", categoria],
        values=[100 - porcentajes_por_categoria[categoria], porcentajes_por_categoria[categoria]],
        title=f"{categoria} vs Todas las Categorías - Sucursal {sucursal}",
        hole=0.3
    )
    st.plotly_chart(fig)