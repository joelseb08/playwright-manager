# PlaywrightManager

Clase para automatización de [Playwright](https://playwright.dev/) usando el patrón _Template Method_.

## Uso

Se usa creando una _**clase personalizada**_, esta debe heredar de `PlaywrightManager` y se debe sobreescribir el método `task()`, de esta manera al usar `run()` se ejecuta lo que hayas escrito.

## Ejemplo

Puedes ver el ejemplo a continuación, también puedes copiear y pegar el código para verificar si funcionalidad:

```py
from playwright_manager import PlaywrightManager

### --- Clase de ejemplo --- ###
class MiTask(PlaywrightManager):
    def task(self) -> None:
        self.page.goto("https://google.com")
        print(self.page.title())

### --- Ejecución --- ###
if __name__ == "__main__":
    kwargs = {
        "browser_args": {
            "headless": False,
            "args": ["--start-maximized"]
        },
        "context_args": {
            "no_viewport": True
        }
    }
    
    manager = MiTask(**kwargs)
    manager.run()
```

El código anterior abre una ventana maximizada, abre en una ventana nueva la página del buscador de [_Google_](https://google.com) e imprime en la terminal el título de la misma, que en este caso solo es "Google".

> [!NOTE]
> Este paquete sigue en desarrollo, por lo que habrá modificaciones y se añadirá una versión _**asíncrona**_ posteriormente, pero por el momento es suficiente con este código para que funcione alguna automatización.
