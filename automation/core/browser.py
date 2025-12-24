# core/browser.py
from playwright.sync_api import sync_playwright, BrowserContext, Playwright


class BrowserManager:
    def __init__(
        self,
        user_data_dir: str,
        download_dir: str,
        headless: bool = False
    ):
        """
        user_data_dir:
            用來保存瀏覽器完整登入狀態（Google / Uber Eats）
        download_dir:
            所有報表下載的預設資料夾
        """
        self.user_data_dir = user_data_dir
        self.download_dir = download_dir
        self.headless = headless

        self._playwright: Playwright | None = None
        self._context: BrowserContext | None = None

    def start(self) -> BrowserContext:
        if self._playwright:
            raise RuntimeError("Browser already started")

        self._playwright = sync_playwright().start()

        self._context = self._playwright.chromium.launch_persistent_context(
            user_data_dir=self.user_data_dir,
            headless=self.headless,
            accept_downloads=True,
            downloads_path=self.download_dir,
            args=[
                "--disable-blink-features=AutomationControlled"
            ]
        )

        return self._context

    def stop(self) -> None:
        if self._context:
            self._context.close()
            self._context = None

        if self._playwright:
            self._playwright.stop()
            self._playwright = None
