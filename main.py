import flet as ft

def main(page: ft.Page):
    campo_email = ft.Container(ft.Column(controls = [ft.Text(value = "Correo Electronico", size = 20 , weight = "BOLD", color = "#43D17A"), ft.TextField(hint_text= 'Correo electronico',border ='underline',color ="#8EDAAB")]))
    campo_contraseña = ft.Container(ft.Column(controls = [ft.Text(value = "Contraseña", size = 20 , weight = "BOLD", color = "#43D17A"), ft.TextField(password = True, hint_text= 'Contraseña',border ='underline',color ="#8EDAAB")]))
    mensaje_bienvenida = ft.Container(padding = 30, content = ft.Text(value = "Bienvenido", size = 45 , weight = "BOLD", color = "#43D17A"))
    def cambiar_tamaño(e):
        if page.width < 700:
         mensaje_bienvenida.size = 35
        else:
         mensaje_bienvenida.size = 45
    
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
            "lg": 4 , 
            } ,
            padding = 30,
            alignment = ft.Alignment.CENTER ,
            border_radius = 20 ,
            bgcolor = "#0A0E0A",
            aspect_ratio = 0.667 ,
            content = ft.Column(alignment = ft.MainAxisAlignment.START, horizontal_alignment= ft.CrossAxisAlignment.CENTER ,
            controls = [mensaje_bienvenida, campo_email, campo_contraseña]
            )
    )
   ],      
)
 
    page.fonts = {"Space_Grotesk": "https://github.com/floriankarsten/space-grotesk/raw/refs/heads/master/fonts/ttf/SpaceGrotesk%5Bwght%5D.ttf",}
    page.bgcolor = "black"
    page.theme = ft.Theme(font_family="Space_Grotesk")
    page.title = "Yeremi Social"
    page.adaptive = True
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.add(contenedor)




ft.run(main)