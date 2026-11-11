from flet.canvas import Shadow
import flet as ft

def main(page: ft.Page):
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
            "md": 12,  
            "lg": 12 , 
            } ,
            padding = 30,
            alignment = ft.Alignment.CENTER ,
            border_radius = 20 ,
            bgcolor = "#0A0E0A",
            
            shadow=ft.BoxShadow(
                    spread_radius = 15,
                    blur_radius= 0 ,
                    color= "#43D17A",
                    offset=ft.Offset(0, 5)),
      
            aspect_ratio = 0.5625 ,
            content = ft.Column(alignment = ft.MainAxisAlignment.START, horizontal_alignment= ft.CrossAxisAlignment.CENTER ,
            controls = [ft.Text("HelloWorld"), ft.IconButton(icon = ft.Icons.ADD_A_PHOTO, icon_size = 40)]
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