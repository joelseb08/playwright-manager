from playwright.sync_api import Playwright, sync_playwright, Browser, BrowserContext, Page
from time import perf_counter
from typing import Optional

class PlaywrightManager:
    """
    Clase base para automatización con Playwright.

    Subclasifica esta clase y sobreescribe el método `task()` con tu lógica.
    Los parámetros de browser y context se pasan como diccionarios directamente
    a la API de Playwright.

    Ejemplo::

        class MiTask(PlaywrightManager):
            def task(self) -> None:
                self.page.goto("https://ejemplo.com")
                print(self.page.title())

        manager = MiTask(browser_args={"headless": False})
        manager.run()
    """

    def __init__(self, browser_args: Optional[dict] = None, context_args: Optional[dict] = None,) -> None:
        self.browser_args: dict = browser_args or {}
        self.context_args: dict = context_args or {}
        self.browser: Browser = None
        self.context: BrowserContext = None
        self.page: Page = None
        self._timers: dict = {}

    def __repr__(self) -> str:
        status = "running" if self.browser else "idle"
        return f"{self.__class__.__name__}(status={status!r})"

    def _setup(self, pw: Playwright) -> None:
        self.browser = pw.chromium.launch(**self.browser_args)
        self.context = self.browser.new_context(**self.context_args)
        self.page = self.context.new_page()

    def task(self) -> None:
        """Sobreescribe este método con la lógica de tu tarea."""
        raise NotImplementedError("Debes sobreescribir el método task()")

    def run(self) -> None:
        """Inicia Playwright, ejecuta task() y cierra los recursos al terminar."""
        with sync_playwright() as pw:
            self._setup(pw)
            try:
                self.task()
            finally:
                self.context.close()
                self.browser.close()

    def reset(self) -> None:
        """Cierra el contexto actual y abre uno nuevo reutilizando el mismo browser."""
        if self.context:
            self.context.close()
        self.context = self.browser.new_context(**self.context_args)
        self.page = self.context.new_page()

    ### --- Timers --- ##

    def start_timer(self, name: str) -> None:
        """Inicia un timer con el nombre dado."""
        self._timers[name] = {"start": perf_counter(), "elapsed": None}

    def end_timer(self, name: str) -> None:
        """Detiene el timer y guarda el tiempo transcurrido en segundos."""
        if name not in self._timers:
            raise KeyError(f'El timer "{name}" no existe')
        if self._timers[name]["elapsed"] is not None:
            raise RuntimeError(f'El timer "{name}" ya fue detenido')
        self._timers[name]["elapsed"] = int(
            round(perf_counter() - self._timers[name]["start"])
        )

    def elapsed(self, name: str) -> int:
        """
        Devuelve el tiempo transcurrido en segundos de un timer detenido.

        Raises:
            KeyError: Si el timer no existe.
            RuntimeError: Si el timer todavía está corriendo (end_timer no fue llamado).
        """
        if name not in self._timers:
            raise KeyError(f'El timer "{name}" no existe')
        if self._timers[name]["elapsed"] is None:
            raise RuntimeError(
                f'El timer "{name}" sigue corriendo, llama end_timer() primero'
            )
        return self._timers[name]["elapsed"]
