import json
import logging
import sys
from typing import Any, Dict

from app.core.config import settings



class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: Dict[str, Any] = {
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "time": self.formatTime(record, self.datefmt),
        }

        # اگر extra گذاشته باشیم (مثل request_id)، وارد لاگ شود
        for key in ("request_id", "path", "method", "status_code", "duration_ms"):
            if hasattr(record, key):
                payload[key] = getattr(record, key)

        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)

        return json.dumps(payload, ensure_ascii=False)


def setup_logging() -> None:
    level_name = (settings.LOG_LEVEL or "INFO").upper()
    level = getattr(logging, level_name, logging.INFO)

    root = logging.getLogger()
    root.setLevel(level)

    handler = logging.StreamHandler(sys.stdout)

    if (settings.LOG_FORMAT or "console").lower() == "json":
        handler.setFormatter(JsonFormatter())
    else:
        handler.setFormatter(
            logging.Formatter(
                fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        )

    # هندلرهای قبلی را پاک کنیم تا دوباره‌کاری/تکرار لاگ نداشته باشیم
    root.handlers.clear()
    root.addHandler(handler)

    # لاگ‌های خیلی پر سر و صدای sqlalchemy را کنترل می‌کنیم
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
