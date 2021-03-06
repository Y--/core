"""An abstract class common to all Bond entities."""
from abc import abstractmethod
from typing import Any, Dict, Optional

from homeassistant.const import ATTR_NAME
from homeassistant.helpers.entity import Entity

from .const import DOMAIN
from .utils import BondDevice, BondHub


class BondEntity(Entity):
    """Generic Bond entity encapsulating common features of any Bond controlled device."""

    def __init__(self, hub: BondHub, device: BondDevice):
        """Initialize entity with API and device info."""
        self._hub = hub
        self._device = device

    @property
    def unique_id(self) -> Optional[str]:
        """Get unique ID for the entity."""
        return self._device.device_id

    @property
    def name(self) -> Optional[str]:
        """Get entity name."""
        return self._device.name

    @property
    def device_info(self) -> Optional[Dict[str, Any]]:
        """Get a an HA device representing this Bond controlled device."""
        return {
            ATTR_NAME: self.name,
            "identifiers": {(DOMAIN, self._device.device_id)},
            "via_device": (DOMAIN, self._hub.bond_id),
        }

    @property
    def assumed_state(self) -> bool:
        """Let HA know this entity relies on an assumed state tracked by Bond."""
        return True

    async def async_update(self):
        """Fetch assumed state of the cover from the hub using API."""
        state: dict = await self._hub.bond.device_state(self._device.device_id)
        self._apply_state(state)

    @abstractmethod
    def _apply_state(self, state: dict):
        raise NotImplementedError
