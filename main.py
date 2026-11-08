import flet as ft
contenedor = ft.Container(
              padding = 30,
              alignment = ft.Alignment.CENTER ,
              border_radius = 20 ,
              bgcolor = "#23bf66",
              width = 900,
              height = 1500, 
              content = ft.Column(
              alignment = ft.MainAxisAlignment.START,
              horizontal_alignment= ft.CrossAxisAlignment.CENTER ,
              controls = [ft.Text(
                value = "Bienvenido", size = 80, weight = "BOLD" )]
    )
)
def main(page: ft.Page):
   # def button_clicked(e: ft.Event[ft.Button]):
    #    if campo.value.strip() == "":
     #       error.value = f"ingrese un nombre valido"
     #   else:
     #       mensaje.value = f"¡Bienvenido a Yeremi Social!, {campo.value}."
    page.title = "Yeremi Social"
    page.adaptive = True
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.add(contenedor)

ft.run(main)