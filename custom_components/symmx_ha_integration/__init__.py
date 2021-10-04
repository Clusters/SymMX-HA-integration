"""The Commend Symphony MX integration."""
from __future__ import annotations

import voluptuous as vol
import json
import asyncio

from homeassistant.components import mqtt
from homeassistant.core import HomeAssistant, ServiceCall, callback
from homeassistant.helpers.typing import ConfigType


from .const import DOMAIN

PLATFORMS = ["sensor"]

CONF_TOPIC = 'topic'
DEFAULT_TOPIC = '+/motion_detection/#'

# Schema to validate the configured MQTT topic
CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Optional(
                    CONF_TOPIC, default=DEFAULT_TOPIC
                ): mqtt.valid_subscribe_topic
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

async def async_unset_motion_detection(hass: HomeAssistant, waiting_time: int = 5):
    print("Unset motion detection")
    await asyncio.sleep(waiting_time)
    print("Unset motion detection after sleep")
    hass.data[DOMAIN] = { 'state': False }
    hass.states.async_set("sensor.smx_motion_detection_sensor", False, force_update=True)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the MQTT async example component."""
    topic = config[DOMAIN][CONF_TOPIC]
    entity_id = 'symmx_ha_integration.last_message'
    hass.data["commend_entities"] = list() if not hass.data.get("commend_entities", None) else \
                                    hass.data["commend_entities"]

    # Listen to a message on MQTT.
    @callback
    def message_received(topic: str, payload: str, qos: int) -> None:
        """A new MQTT message has been received."""
        print(f"MESSAGE RECEIVED: entity_id: {entity_id}, payload: {payload}")
        hass.states.async_set(entity_id, payload)
        hass.data[DOMAIN] = { 'state': payload }
        state = True if payload == "ON" else False
        print(f"state = {state}")
        if state:
            hass.states.async_set("sensor.smx_motion_detection_sensor", state)
            hass.async_run_job(async_unset_motion_detection(hass, 5))
        if DOMAIN not in hass.data["commend_entities"]:
            hass.async_create_task(hass.helpers.discovery.async_load_platform('sensor', DOMAIN, {}, config))
            hass.data["commend_entities"].append(DOMAIN)

    await hass.components.mqtt.async_subscribe(topic, message_received)

    hass.states.async_set(entity_id, 'No messages')

    # Service to publish a message on MQTT.
    @callback
    def set_state_service(call: ServiceCall) -> None:
        """Service to send a message."""
        hass.components.mqtt.async_publish(topic, call.data.get('new_state'))

    # Register our service with Home Assistant.
    hass.services.async_register(DOMAIN, 'set_state', set_state_service)

    # Return boolean to indicate that initialization was successfully.
    return True
