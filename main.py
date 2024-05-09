from flet import (
    app,
    Page,
    Row,
    Column,
    Text,
    TextField,
    ElevatedButton,
    ButtonStyle,
    RoundedRectangleBorder,
    Container,
    Checkbox,
    Dropdown,
    dropdown,
    MainAxisAlignment,
    CrossAxisAlignment,
    colors,
    TextThemeStyle,
    Border,
    BorderSide,
)

from asyncio import sleep
from app_cola import simulacion


def main(page: Page):

    async def change_metodo_simulacion(event):
        metodo = metodo_simulacion.value

        tf_metodo.value = ""
        tf_metodo.label = "Número de clientes a simular"
        if metodo == "Por tiempo":
            tf_metodo.label = "Tiempo de simulación"

        tf_metodo.visible = True
        ejecutar_simulacion.visible = True

        await page.update_async()

    async def campo_entero(event):
        text = event.control.value
        print(text)
        if not text.isdigit():
            event.control.value = text[:-1]  # Eliminar último carácter no válido

        await page.update_async()

    async def ejecutar_simulacion(event):
        metodo_seleccionado = metodo_simulacion.value
        try:
            valor = int(tf_metodo.value)
            nodos = int(tf_nodos.value)
            pantalla.value = ""
            simulacion(pantalla, metodo_seleccionado, nodos, valor)

        except ValueError:
            pantalla.value = "Los campos no pueden quedar vacíos"
            pantalla.color = colors.RED_200
            await pantalla.update_async()
            await sleep(2)
            pantalla.value = ""
            pantalla.color = colors.WHITE

        await page.update_async()

    page.title = "Redes de Colas: Simulación"
    page.vertical_alignment = MainAxisAlignment.START
    page.horizontal_alignment = CrossAxisAlignment.CENTER
    page.adaptive = True
    page.auto_scroll = True
    page.bgcolor = colors.INDIGO

    # Text
    pantalla = Text(value="", size=16)

    # TextFields
    tf_nodos = TextField(
        label="Cantidad de nodos",
        width=300,
        on_change=campo_entero,
    )
    tf_metodo = TextField(
        width=300,
        visible=False,
        on_change=campo_entero,
    )

    # Buttons
    ejecutar_simulacion = ElevatedButton(
        text="Ejecutar simulación",
        style=ButtonStyle(
            shape=RoundedRectangleBorder(radius=10),
        ),
        width=200,
        height=45,
        visible=False,
        on_click=ejecutar_simulacion,
    )

    # Dropdowns
    metodo_simulacion = Dropdown(
        width=300,
        label="Método de simulación",
        options=[
            dropdown.Option("Por tiempo"),
            dropdown.Option("Por clientes"),
        ],
        on_change=change_metodo_simulacion,
    )

    page.add(
        Container(
            height=350,
            padding=15,
            content=Column(
                controls=[
                    Text(
                        value="Aplicación: Simulación de Redes de Cola",
                        style=TextThemeStyle.TITLE_LARGE,
                    ),
                    tf_nodos,
                    metodo_simulacion,
                    tf_metodo,
                    ejecutar_simulacion,
                ],
                spacing=20,
                horizontal_alignment=CrossAxisAlignment.CENTER,
            ),
        ),
        Text(
            value="Pantalla de Simulación",
            style=TextThemeStyle.TITLE_LARGE,
        ),
        Container(
            padding=15,
            width=700,
            height=500,
            border=Border(
                BorderSide(1, colors.AMBER_100),
                BorderSide(1, colors.AMBER_100),
                BorderSide(1, colors.AMBER_100),
                BorderSide(1, colors.AMBER_100),
            ),
            content=Column(
                controls=[pantalla],
                scroll=True,
                horizontal_alignment=CrossAxisAlignment.START,
            ),
        ),
    )

    page.update()


app(target=main)
