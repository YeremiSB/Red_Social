import flet as ft

def main(page: ft.Page):
    def button_clicked(e: ft.Event[ft.Button]):
        message.value = f"¡Bienvenido a Yeremi Social!"
    page.title = "Yeremi Social"
    page.add(
        message := ft.Text("Bienvenido a mi red social", size=30) ,
        button := ft.Button(content = "Comenzar", on_click = button_clicked)
    )

ft.run(main)