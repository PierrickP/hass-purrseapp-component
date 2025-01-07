"""Constants for the Purrse.app integration."""

from datetime import timedelta

DOMAIN = "purrseapp"
PURRSE_API_BASE_URL = "https://purrse.app/api/v1{path}"
COORDINATOR_UPDATE_INTERVAL = timedelta(hours=1)
