import flet as ft

def main(page: ft.Page):
    def cambiar_tamaño(e):
        if page.width < 700:
          pass
       #   mensaje_bienvenida.content.size = 35
        else:
         pass
         #mensaje_bienvenida.content.size = 45
        page.update()
    page.on_resize = cambiar_tamaño
    barra_principal = ft.AppBar(
    bgcolor = "#0A0E0A",
    title=ft.Text(value = "Bast Social", 
                  size = 20 , 
                  weight = "BOLD", 
                  color = "#43D17A"),
    actions=[
        ft.IconButton(ft.Icons.ACCOUNT_CIRCLE),
        ft.IconButton(ft.Icons.ADD),
        ft.IconButton(ft.Icons.MORE_VERT),
    ],
    )
    # def button_clicked(e: ft.Event[ft.Button]):
    #    if campo.value.strip() == "":
     #       error.value = f"ingrese un nombre valido"
     #   else:
     #       mensaje.value = f"¡Bienvenido a Yeremi Social!, {campo.value}."
    contenedor = ft.ResponsiveRow(
            alignment = ft.MainAxisAlignment.CENTER ,
            vertical_alignment = ft.CrossAxisAlignment.CENTER ,
            controls = [ft.Container(
            col={
            "xs": 12, 
            "md": 12,  
            "lg": 12 , 
            } ,
            padding = 30,
            alignment = ft.Alignment.CENTER ,
            border_radius = 20 ,
            bgcolor = "#0A0E0A",
            aspect_ratio = 0.5625 ,
            content = ft.Column(alignment = ft.MainAxisAlignment.START, horizontal_alignment= ft.CrossAxisAlignment.CENTER ,
            controls = [ft.Text("HelloWorld")]
            )
    )
   ],      
)
    page.assets_dir = "assets" 
    page.fonts = {"Space_Grotesk": "fonts/SpaceGrotesk-Regular.ttf",
                 "Space_Grotesk_Bold": "fonts/SpaceGrotesk-Bold.ttf"
                 }
    page.bgcolor = "black"
    page.theme = ft.Theme(font_family="Space_Grotesk")
    page.title = "Yeremi Social"
    page.adaptive = True
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.add(barra_principal, contenedor)
    cambiar_tamaño(None)
ft.run(main)