import flet as ft

def main(page: ft.Page):
    def button_clicked(e: ft.Event[ft.Button]):
        mensaje.value = f"¡Bienvenido a Yeremi Social!, {campo.value}"
    page.title = "Yeremi Social"
    page.add(
        ft.SafeArea(
        content=ft.Column(
            controls=[
            mensaje := ft.Text("Bienvenido a mi red social", size=30) ,
            campo := ft.TextField(label="Name", hint_text="Jane Doe"),
            boton:= ft.Button(content = "Comenzar", on_click = button_clicked) ,
            ]

         )
       )     
    )

ft.run(main)