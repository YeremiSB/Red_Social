import base64
from datetime import datetime
from pathlib import Path

import flet as ft
import flet_camera as fc

CARPETA_FOTOS = Path(__file__).resolve().parent / "fotos"


def describir_error(ex: Exception) -> str:
    texto = str(ex).lower()
    if "accessdenied" in texto or "access denied" in texto:
        return (
            "Permiso denegado. Revisa el candado de la barra de direcciones "
            "y los permisos de cámara de Windows."
        )
    if "notreadable" in texto:
        return (
            "La cámara no responde: está ocupada por otra app o pestaña, "
            "o el driver no la expone bien."
        )
    if "notfound" in texto:
        return "No se encontró esa cámara."
    return f"Error de cámara: {ex}"


def etiqueta(desc: fc.CameraDescription) -> str:
    return desc.name.strip() or "(cámara sin nombre)"


def es_virtual(desc: fc.CameraDescription) -> bool:
    nombre = desc.name.lower()
    return any(
        pista in nombre
        for pista in ("virtual", "obs", "manycam", "snap camera", "droidcam", "ivcam")
    )


async def main(page: ft.Page):
    page.title = "Prueba de cámara"
    page.padding = 20

    soporta_camara = page.web or page.platform in (
        ft.PagePlatform.ANDROID,
        ft.PagePlatform.IOS,
    )
    camara = fc.Camera(width=320, height=240) if soporta_camara else None
    foto = ft.Image(
        src="https://yeremisb.com/Fotos/Gato_Calle.webp",
        width=200,
        height=200,
        fit=ft.BoxFit.COVER,
    )
    estado = ft.Text(
        "Pulsa «Buscar cámaras» para ver qué detecta el navegador.",
        size=13,
    )
    selector = ft.Dropdown(
        label="Cámara",
        width=320,
        disabled=True,
        options=[],
    )
    boton_buscar = ft.Button("Buscar cámaras", disabled=camara is None)
    boton_abrir = ft.Button("Abrir cámara", disabled=True)
    boton_foto = ft.Button("Tomar foto", disabled=True)

    camaras: list[fc.CameraDescription] = []
    inicializada = False

    async def buscar(e=None):
        nonlocal camaras
        if camara is None:
            estado.value = "La cámara solo funciona en Web, Android o iOS."
            page.update()
            return
        estado.value = "Buscando cámaras..."
        page.update()
        try:
            camaras = await camara.get_available_cameras()
        except Exception as ex:
            camaras = []
            estado.value = (
                describir_error(ex)
                + " Si tienes OBS Virtual Camera (u otra cámara virtual), "
                "desactívala en el Administrador de dispositivos: rompe la "
                "detección de cámaras."
            )
            page.update()
            return

        if not camaras:
            selector.options = []
            selector.value = None
            selector.disabled = True
            boton_abrir.disabled = True
            estado.value = (
                "El navegador no expone ninguna cámara. Si conectaste una, "
                "revisa el Administrador de dispositivos."
            )
            page.update()
            return

        # Las virtuales (OBS, ManyCam...) suelen fallar si su app no está abierta.
        camaras.sort(key=lambda c: es_virtual(c))

        selector.options = [
            ft.DropdownOption(key=str(i), text=etiqueta(c))
            for i, c in enumerate(camaras)
        ]
        selector.value = "0"
        selector.disabled = False
        boton_abrir.disabled = False
        estado.value = (
            f"{len(camaras)} cámara(s) detectada(s): "
            + ", ".join(etiqueta(c) for c in camaras)
        )
        page.update()

    async def abrir(e):
        nonlocal inicializada
        if camara is None:
            estado.value = "La cámara solo funciona en Web, Android o iOS."
            page.update()
            return
        if inicializada:
            estado.value = "La cámara ya está abierta."
            page.update()
            return
        if not camaras:
            await buscar()
            if not camaras:
                return

        indice = int(selector.value or "0")
        if not (0 <= indice < len(camaras)):
            estado.value = "Elige una cámara en la lista."
            page.update()
            return

        indice = int(selector.value or "0")
        if not (0 <= indice < len(camaras)):
            estado.value = "Elige una cámara en la lista."
            page.update()
            return

        # Si la elegida falla, se prueban las demás automáticamente.
        orden = [indice] + [i for i in range(len(camaras)) if i != indice]
        ultimo_error = ""
        boton_abrir.disabled = True
        try:
            for i in orden:
                desc = camaras[i]
                estado.value = f"Abriendo: {etiqueta(desc)}"
                page.update()
                try:
                    await camara.initialize(
                        desc,
                        fc.ResolutionPreset.HIGH,
                        enable_audio=False,
                    )
                except Exception as ex:
                    ultimo_error = f"{etiqueta(desc)}: {describir_error(ex)}"
                    continue

                inicializada = True
                boton_foto.disabled = False
                selector.disabled = True
                selector.value = str(i)
                estado.value = f"Cámara lista: {etiqueta(desc)}"
                page.update()
                return
        finally:
            boton_abrir.disabled = inicializada
            page.update()

        estado.value = (
            "No se pudo abrir ninguna cámara. Último error: " + ultimo_error
        )
        page.update()

    async def capturar(e):
        if not inicializada or camara is None:
            estado.value = "Abre la cámara primero."
            page.update()
            return
        try:
            datos = await camara.take_picture()
        except Exception as ex:
            estado.value = describir_error(ex)
            page.update()
            return
        if isinstance(datos, str):
            datos = base64.b64decode(datos)
        if not datos:
            estado.value = "La cámara no devolvió ninguna imagen."
            page.update()
            return

        CARPETA_FOTOS.mkdir(exist_ok=True)
        ruta = CARPETA_FOTOS / f"prueba_{datetime.now():%Y%m%d_%H%M%S_%f}.jpg"
        ruta.write_bytes(datos)
        foto.src = datos
        estado.value = f"Foto guardada en fotos/{ruta.name}"
        page.update()

    boton_buscar.on_click = buscar
    boton_abrir.on_click = abrir
    boton_foto.on_click = capturar

    page.add(
        *([camara] if camara is not None else []),
        selector,
        ft.Row([boton_buscar, boton_abrir, boton_foto], wrap=True),
        estado,
        foto,
    )

    if camara is not None:
        await buscar()


if __name__ == "__main__":
    ft.run(main)
