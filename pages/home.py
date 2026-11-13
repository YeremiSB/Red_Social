import flet as ft

def main(page: ft.Page):
    imagen = "https://yeremisb.com/Fotos/Gato_Calle.webp"
    barra_principal = ft.AppBar(
      elevation = 5,
      shadow_color= "#43D17A",
      shape = ft.RoundedRectangleBorder(
    radius = ft.BorderRadius.only(
        bottom_left = 15,
        bottom_right = 15
    )
      ), 
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
    imagenes = ft.Container(
              expand=True,
              alignment = ft.Alignment.CENTER ,
              border_radius = 20 ,
              bgcolor = "#0A0E0A",
              shadow=ft.BoxShadow(
                      spread_radius = 0,
                      blur_radius= 10 ,
                      color= "#43D17A",
                      offset=ft.Offset(0, 5)),
              #aspect_ratio = 0.5625 ,
              content = ft.Image(src = imagen , fit = ft.BoxFit.COVER, width=float("inf"), height=float("inf"),)
              )
    def cambiar_tamaño(e):
        if page.width < 700:
          pass
       #   mensaje_bienvenida.content.size = 35
        else:
         pass
         #mensaje_bienvenida.content.size = 45
        page.update()
    page.on_resize = cambiar_tamaño
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
            "md": 6,  
            "lg": 3 , 
            } ,
            padding = 30,
            alignment = ft.Alignment.CENTER ,
            border_radius = 20 ,
            bgcolor = "#0A0E0A",
            shadow=ft.BoxShadow(
                    spread_radius = 0,
                    blur_radius= 10 ,
                    color= "#43D17A",
                    offset=ft.Offset(0, 5)),
            aspect_ratio = 0.5625 ,
            content = ft.Column(alignment = ft.MainAxisAlignment.START, horizontal_alignment= ft.CrossAxisAlignment.CENTER ,
            controls = [imagenes , ft.IconButton(icon = ft.Icons.ADD_A_PHOTO, icon_size = 40)]
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
    page.appbar = barra_principal
    page.add(contenedor)
    cambiar_tamaño(None)
ft.run(main)