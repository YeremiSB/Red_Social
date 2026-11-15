import base64
from datetime import datetime
from pathlib import Path

import flet as feet
import flet_camera as paw

VERDE = "#43D17A"
FONDO = "#0A0E0A"
FOTOS = "https://yeremisb.com/Fotos/Gato_Calle.webp"
CARPETA_FOTOS = Path(__file__).resolve().parent.parent / "fotos"


PLATAFORMAS_CON_CAMARA = (
    feet.PagePlatform.ANDROID,
    feet.PagePlatform.IOS,
)


def describir_error(ex: Exception) -> str:
    texto = str(ex).lower()
    if "accessdenied" in texto or "access denied" in texto:
        return (
            "Permiso de cámara denegado. Revisa el candado de la barra de "
            "direcciones y los permisos de cámara del sistema."
        )
    if "notreadable" in texto:
        return (
            "La cámara no responde: puede estar ocupada por otra app o "
            "pestaña, o desconectada."
        )
    if "notfound" in texto:
        return "No se encontró ninguna cámara conectada."
    return f"Error de cámara: {ex}"


def es_virtual(desc: paw.CameraDescription) -> bool:
    nombre = desc.name.lower()
    return any(
        pista in nombre
        for pista in ("virtual", "obs", "manycam", "snap camera", "droidcam", "ivcam")
    )


def guardar_foto(datos: bytes) -> Path:
    CARPETA_FOTOS.mkdir(parents=True, exist_ok=True)
    ruta = CARPETA_FOTOS / f"foto_{datetime.now():%Y%m%d_%H%M%S_%f}.jpg"
    ruta.write_bytes(datos)
    return ruta


def main(page: feet.Page):
    page.assets_dir = "assets"
    page.fonts = {
        "Space_Grotesk": "fonts/SpaceGrotesk-Regular.ttf",
        "Space_Grotesk_Bold": "fonts/SpaceGrotesk-Bold.ttf",
    }
    page.bgcolor = "black"
    page.theme = feet.Theme(font_family="Space_Grotesk")
    page.title = "Yeremi Social"
    page.adaptive = True
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

    barra_principal = feet.AppBar(
        elevation=5,
        shadow_color=VERDE,
        shape=feet.RoundedRectangleBorder(
            radius=feet.BorderRadius.only(bottom_left=15, bottom_right=15)
        ),
        bgcolor=FONDO,
        title=feet.Text(
            value="Bast Social",
            size=20,
            weight="BOLD",
            color=VERDE,
        ),
        actions=[
            feet.IconButton(feet.Icons.ACCOUNT_CIRCLE),
            feet.IconButton(feet.Icons.ADD),
            feet.IconButton(feet.Icons.MORE_VERT),
        ],
    )

    foto = feet.Image(
        src=FOTOS,
        fit=feet.BoxFit.COVER,
        width=float("inf"),
        height=float("inf"),
    )
    capa_foto = feet.Container(expand=True, bgcolor=FONDO, content=foto)

    soporta_camara = page.web or page.platform in PLATAFORMAS_CON_CAMARA
    camara = paw.Camera(expand=True) if soporta_camara else None

    inicializada = False
    en_camara = False
    desc_actual = None
    ocupado = False

    def aviso(texto: str, error: bool = False):
        page.show_dialog(
            feet.SnackBar(
                content=feet.Text(texto, color="white"),
                bgcolor="#5A1B1B" if error else "#1E2B1E",
                duration=4000,
            )
        )

    boton_disparo = feet.IconButton(
        icon = feet.Icons.CAMERA,
        icon_size = 40,
        icon_color = FONDO,
        bgcolor = VERDE,
        tooltip = "Tomar foto",
        visible = False,
    )
    boton_like = feet.IconButton(
        icon = feet.Icons.FAVORITE_BORDER ,
        icon_size = 20,
        icon_color = VERDE,
        tooltip = "Like"
    )
    boton_camara = feet.IconButton(
        icon = feet.Icons.ADD_A_PHOTO,
        icon_size = 40,
        icon_color = VERDE,
        tooltip = "Abrir cámara",
    )

    async def abrir_camara(e=None):
        nonlocal inicializada, en_camara, desc_actual, ocupado

        if camara is None:
            aviso("La cámara solo funciona en Web, Android o iOS.", True)
            return
        if ocupado:
            return
        if en_camara:
            await cerrar_camara()
            return

        ocupado = True
        boton_camara.disabled = True
        page.update()
        try:
            if not inicializada:
                try:
                    candidatas = await camara.get_available_cameras()
                except Exception as ex:
                    aviso(describir_error(ex), True)
                    return
                candidatas.sort(key=es_virtual)
                if not candidatas:
                    aviso("No se encontró ninguna cámara disponible.", True)
                    return

                ultimo_error = ""
                for desc in candidatas:
                    try:
                        await camara.initialize(
                            desc,
                            paw.ResolutionPreset.HIGH,
                            enable_audio=False,
                        )
                    except Exception as ex:
                        ultimo_error = describir_error(ex)
                        continue
                    inicializada = True
                    desc_actual = desc
                    break

                if not inicializada:
                    aviso(f"No se pudo abrir la cámara. {ultimo_error}", True)
                    return
            else:
                try:
                    await camara.resume_preview()
                except Exception:
                    pass
        finally:
            ocupado = False
            boton_camara.disabled = False
            page.update()

        capa_foto.visible = False
        boton_disparo.visible = True
        boton_camara.icon = feet.Icons.CLOSE
        en_camara = True
        page.update()

    async def cerrar_camara():
        nonlocal en_camara
        if camara is not None and inicializada:
            try:
                await camara.pause_preview()
            except Exception:
                pass
        capa_foto.visible = True
        boton_disparo.visible = False
        boton_camara.icon = feet.Icons.ADD_A_PHOTO
        en_camara = False
        page.update()

    async def tomar_foto(e=None):
        if camara is None or not inicializada:
            return
        try:
            datos = await camara.take_picture()
        except Exception as ex:
            aviso(f"No se pudo tomar la foto. {describir_error(ex)}", True)
            return
        if isinstance(datos, str):
            datos = base64.b64decode(datos)
        if not datos:
            aviso("La cámara no devolvió ninguna imagen.", True)
            return

        ruta = guardar_foto(datos)
        foto.src = datos
        await cerrar_camara()
        aviso(f"Foto guardada en fotos/{ruta.name}")

    async def al_cambiar_estado(e: feet.AppLifecycleStateChangeEvent):
        nonlocal inicializada, en_camara

        if camara is None:
            return
        if e.state in (feet.AppLifecycleState.HIDE, feet.AppLifecycleState.PAUSE):
            if inicializada:
                try:
                    await camara.pause_preview()
                except Exception:
                    pass
            return
        if e.state not in (feet.AppLifecycleState.RESUME, feet.AppLifecycleState.SHOW):
            return
        if not inicializada or desc_actual is None:
            return
        try:
            await camara.resume_preview()
            return
        except Exception:
            pass

        try:
            await camara.initialize(
                desc_actual,
                paw.ResolutionPreset.HIGH,
                enable_audio=False,
            )
        except Exception as ex:
            inicializada = False
            en_camara = False
            capa_foto.visible = True
            boton_disparo.visible = False
            boton_camara.icon = feet.Icons.ADD_A_PHOTO
            aviso(
                describir_error(ex) + " Pulsa el botón de cámara para reintentar.",
                True,
            )
            page.update()

    boton_camara.on_click = abrir_camara
    boton_disparo.on_click = tomar_foto
    page.on_app_lifecycle_state_change = al_cambiar_estado

    vista = feet.Stack(
        controls=([camara] if camara is not None else []) + [capa_foto],
        fit=feet.StackFit.EXPAND,
        expand=True,
    )

    imagenes = feet.Container(
        expand=True,
        alignment=feet.Alignment.CENTER,
        border_radius=20,
        bgcolor=FONDO,
        shadow=feet.BoxShadow(
            spread_radius=0,
            blur_radius=10,
            color=VERDE,
            offset=feet.Offset(0, 5),
        ),
        content=vista,
    )

    contenedor = feet.ResponsiveRow(
        alignment=feet.MainAxisAlignment.CENTER,
        vertical_alignment=feet.CrossAxisAlignment.CENTER,
        controls=[
            feet.Container(
                col={"xs": 12, "md": 6, "lg": 3},
                padding=30,
                alignment=feet.Alignment.CENTER,
                border_radius=20,
                bgcolor=FONDO,
                shadow=feet.BoxShadow(
                    spread_radius=0,
                    blur_radius=10,
                    color=VERDE,
                    offset=feet.Offset(0, 5),
                ),
                aspect_ratio=0.5625,
                content=feet.Column(
                    alignment=feet.MainAxisAlignment.START,
                    horizontal_alignment=feet.CrossAxisAlignment.CENTER,
                    controls=[
                        imagenes,
                        feet.Row(
                            alignment=feet.MainAxisAlignment.CENTER,
                            controls=[boton_like, boton_camara, boton_disparo],
                        ),
                    ],
                ),
            )
        ],
    )

    page.appbar = barra_principal
    page.add(contenedor)
