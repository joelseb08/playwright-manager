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