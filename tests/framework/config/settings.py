from typing import Any, Literal

from pydantic import Field
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)
from pytest import Config


class PlaywrightConfig(BaseSettings):
    """Playwright test configuration managed via Pydantic settings.

    Settings priority: OS env variables (PW_*) > .env file > pytest.ini > defaults.

    Supported environment variables:
        PW_BROWSER, PW_HEADLESS, PW_BASE_URL, PW_BROWSER_CHANNEL,
        PW_TRACING, PW_SCREENSHOT, PW_VIDEO, PW_SLOWMO,
        PW_VIEWPORT_WIDTH, PW_VIEWPORT_HEIGHT, PW_TIMEOUT,
        PW_OUTPUT_DIR, PW_FULL_PAGE_SCREENSHOT, PW_FULLSCREEN
    """

    browser: Literal["chromium", "firefox", "webkit"] = "chromium"
    headless: bool = True
    base_url: str = "https://demoqa.com"
    browser_channel: str | None = None
    tracing: str = "retain-on-failure"
    screenshot: str = "only-on-failure"
    video: str = "retain-on-failure"
    slowmo: int = Field(default=0, ge=0)
    viewport_width: int = Field(default=1280, ge=320, le=3840)
    viewport_height: int = Field(default=720, ge=240, le=2160)
    timeout: int = Field(default=30000, gt=0)
    output_dir: str = "test-results"
    full_page_screenshot: bool = False
    fullscreen: bool = True

    model_config = SettingsConfigDict(
        env_prefix="PW_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        # Priority: OS Env > .env > pytest.ini (init_settings) > Defaults
        return (
            env_settings,
            dotenv_settings,
            init_settings,
            file_secret_settings,
        )

    @classmethod
    def from_pytest(cls, config: Config) -> PlaywrightConfig:
        """Extract settings from pytest_addoption and pass as init kwargs.

        settings_customise_sources ensures OS env vars override these.
        """
        ini_kwargs: dict[str, Any] = {}

        for field_name in cls.model_fields.keys():
            try:
                val = config.getini(f"pw_{field_name}")
                if val not in ("", [], None):
                    ini_kwargs[field_name] = val
            except ValueError:
                pass  # Option was not registered in pytest

        return cls(**ini_kwargs)
