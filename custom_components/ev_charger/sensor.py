"""Sensor platform for EV Charger integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfPower,
    UnitOfEnergy,
    UnitOfTemperature,
    PERCENTAGE,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .api import EVChargerAPI

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up EV Charger sensors based on a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    
    sensors = []
    
    # Hardware sensors
    sensors.extend([
        EVChargerHardwareSensor(coordinator, entry, "online", "Online", None, None),
        EVChargerHardwareSensor(coordinator, entry, "charging", "Charging", None, None),
        EVChargerHardwareSensor(coordinator, entry, "hardware_name", "Hardware Name", None, None),
    ])
    
    # Bluetooth sensors
    sensors.extend([
        EVChargerBluetoothSensor(coordinator, entry, "status", "Status", None, None),
        EVChargerBluetoothSensor(coordinator, entry, "voltage_l1", "Voltage L1", UnitOfElectricPotential.VOLT, SensorDeviceClass.VOLTAGE),
        EVChargerBluetoothSensor(coordinator, entry, "amperage_l1", "Amperage L1", UnitOfElectricCurrent.AMPERE, SensorDeviceClass.CURRENT),
        EVChargerBluetoothSensor(coordinator, entry, "imax", "Max Current", UnitOfElectricCurrent.AMPERE, SensorDeviceClass.CURRENT),
        EVChargerBluetoothSensor(coordinator, entry, "iset", "Set Current", UnitOfElectricCurrent.AMPERE, SensorDeviceClass.CURRENT),
        EVChargerBluetoothSensor(coordinator, entry, "charge_power", "Charge Power", UnitOfPower.KILO_WATT, SensorDeviceClass.POWER),
        EVChargerBluetoothSensor(coordinator, entry, "charged_energy", "Charged Energy", UnitOfEnergy.KILO_WATT_HOUR, SensorDeviceClass.ENERGY),
        EVChargerBluetoothSensor(coordinator, entry, "history_charged_energy", "History Charged Energy", UnitOfEnergy.KILO_WATT_HOUR, SensorDeviceClass.ENERGY),
        EVChargerBluetoothSensor(coordinator, entry, "charge_hours", "Charge Hours", "h", None),
        EVChargerBluetoothSensor(coordinator, entry, "charge_minutes", "Charge Minutes", "min", None),
        EVChargerBluetoothSensor(coordinator, entry, "motherboard_temp", "Motherboard Temperature", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE),
        EVChargerBluetoothSensor(coordinator, entry, "plug_temp", "Plug Temperature", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE),
        EVChargerBluetoothSensor(coordinator, entry, "phases_number", "Phases Number", None, None),
        EVChargerBluetoothSensor(coordinator, entry, "fault_code", "Fault Code", None, None),
        EVChargerBluetoothSensor(coordinator, entry, "cp_signal", "CP Signal", None, None),
        EVChargerBluetoothSensor(coordinator, entry, "pe_signal", "PE Signal", None, None),
        EVChargerBluetoothSensor(coordinator, entry, "is_wifi", "WiFi Connected", None, None),
        EVChargerBluetoothSensor(coordinator, entry, "is_bluetooth", "Bluetooth Connected", None, None),
        EVChargerBluetoothSensor(coordinator, entry, "ip_address", "IP Address", None, None),
        EVChargerBluetoothSensor(coordinator, entry, "update_time", "Last Update", None, SensorDeviceClass.TIMESTAMP),
    ])
    
    async_add_entities(sensors)


class EVChargerSensor(CoordinatorEntity, SensorEntity):
    """Representation of an EV Charger sensor."""
    
    def __init__(
        self,
        coordinator,
        entry: ConfigEntry,
        sensor_type: str,
        name: str,
        unit: str | None,
        device_class: str | None,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._entry = entry
        self._sensor_type = sensor_type
        self._attr_name = f"EV Charger {name}"
        self._attr_unique_id = f"{entry.entry_id}_{sensor_type}"
        self._attr_native_unit_of_measurement = unit
        self._attr_device_class = device_class


class EVChargerHardwareSensor(EVChargerSensor):
    """Representation of a hardware sensor."""
    
    @property
    def native_value(self) -> Any:
        """Return the state of the sensor."""
        if self.coordinator.data and "hardware" in self.coordinator.data:
            hardware_data = self.coordinator.data["hardware"]
            if hardware_data:
                device = hardware_data[0]  # First device
                
                if self._sensor_type == "online":
                    return device.get("isOnline", False)
                elif self._sensor_type == "charging":
                    return device.get("isCharging", False)
                elif self._sensor_type == "hardware_name":
                    return device.get("hardwareName", "Unknown")
        
        return None


class EVChargerBluetoothSensor(EVChargerSensor):
    """Representation of a bluetooth sensor."""
    
    @property
    def native_value(self) -> Any:
        """Return the state of the sensor."""
        if self.coordinator.data and "bluetooth" in self.coordinator.data:
            bluetooth_data = self.coordinator.data["bluetooth"]
            
            if self._sensor_type == "status":
                status = bluetooth_data.get("status", 0)
                return self._get_status_text(status)
            elif self._sensor_type == "voltage_l1":
                return bluetooth_data.get("voltagel1")
            elif self._sensor_type == "amperage_l1":
                return bluetooth_data.get("amperel1")
            elif self._sensor_type == "imax":
                return bluetooth_data.get("imax")
            elif self._sensor_type == "iset":
                return bluetooth_data.get("iset")
            elif self._sensor_type == "charge_power":
                return bluetooth_data.get("chargePower")
            elif self._sensor_type == "charged_energy":
                return bluetooth_data.get("chargedEle")
            elif self._sensor_type == "history_charged_energy":
                return bluetooth_data.get("historyChargeEle")
            elif self._sensor_type == "charge_hours":
                return bluetooth_data.get("chargeHour")
            elif self._sensor_type == "charge_minutes":
                return bluetooth_data.get("chargeMinute")
            elif self._sensor_type == "motherboard_temp":
                return bluetooth_data.get("motherboardTemp")
            elif self._sensor_type == "plug_temp":
                return bluetooth_data.get("plugTemp")
            elif self._sensor_type == "phases_number":
                return bluetooth_data.get("phasesNumber")
            elif self._sensor_type == "fault_code":
                return bluetooth_data.get("faultCode")
            elif self._sensor_type == "cp_signal":
                return bluetooth_data.get("cpSignal")
            elif self._sensor_type == "pe_signal":
                return bluetooth_data.get("peSignal")
            elif self._sensor_type == "is_wifi":
                return bluetooth_data.get("isWifi", False)
            elif self._sensor_type == "is_bluetooth":
                return bluetooth_data.get("isBluetooth", False)
            elif self._sensor_type == "ip_address":
                return bluetooth_data.get("ipAddress")
            elif self._sensor_type == "update_time":
                return bluetooth_data.get("updateTime")
        
        return None
    
    def _get_status_text(self, status: int) -> str:
        """Convert status code to text."""
        status_map = {
            0: "Unknown",
            1: "Ready", 
            2: "Charging",
            3: "Error",
            4: "Waiting"
        }
        return status_map.get(status, f"Unknown ({status})")