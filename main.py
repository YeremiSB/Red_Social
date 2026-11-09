import flet as ft

def main(page: ft.Page):
    
    def cambiar_tamaño(e):
        if page.width < 600:
         return 80
        else:
         return 60
    
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
            content = ft.Column(alignment = ft.MainAxisAlignment.START, horizontal_alignment= ft.CrossAxisAlignment.CENTER ,
            controls = [ft.Text(value = "Bienvenido", size = cambiar_tamaño() , weight = "BOLD", color = "#43D17A" )]
            
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