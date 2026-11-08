import flet as ft

def main(page: ft.Page):
    def button_clicked(e: ft.Event[ft.Button]):
        if campo.value.strip() == "":
            error.value = f"ingrese un nombre valido"
        else:
            mensaje.value = f"¡Bienvenido a Yeremi Social!, {campo.value}."
    page.title = "Yeremi Social"
    page.add(
        ft.SafeArea(
        expand=True ,
        content=ft.Column(
            expand=True,
            alignment=ft.Alignment.CENTER,
            controls=[
            mensaje := ft.Text("Bienvenido a mi red social", size=30) ,
            campo := ft.TextField(label="Nombre", hint_text="Papu :v"),
            boton:= ft.Button(content = "Comenzar", on_click = button_clicked),
            error := ft.Text(),
            ],
            
         )
       )     
    )

ft.run(main)