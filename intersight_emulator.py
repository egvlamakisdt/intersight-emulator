from typing import Any, Dict, List, Optional
import uvicorn
from fastapi import FastAPI, Header, HTTPException, Query, Response

app = FastAPI(
    title="Cisco Intersight UCS X-Series Comprehensive Mock API",
    version="2.0.0",
    description=(
        "Local FastAPI emulator mimicking the complete Cisco Intersight REST API"
        " surface for X-Series chassis, compute nodes, IO cards, fabric"
        " interconnects, environmental sensors, firmware, and telemetry."
    ),
)


# ==========================================
# Comprehensive UCS X-Series Mock Datasets
# ==========================================

CHASSIS_DATA = [
    {
        "Moid": "64a2b1007564612d3001234a",
        "ObjectType": "equipment.Chassis",
        "Serial": "FOX264500AB",
        "Model": "UCSX-9508",
        "Name": "Chassis-1",
        "OperState": "Operable",
        "NumSlots": 8,
        "TotalPowerCapacity": 10000,
        "ScaledMode": "NotSupported",
    }
]

BLADES_DATA = [
    {
        "Moid": "64a2b2f87564612d3001234b",
        "ObjectType": "compute.Blade",
        "Serial": "FCH264801XY",
        "Model": "UCSX-210C-M7",
        "Name": "Chassis-1-Slot-1",
        "OperState": "Operable",
        "SlotId": 1,
        "NumCpus": 2,
        "NumCores": 64,
        "TotalMemory": 1048576,  # 1 TB in MB
        "Chassis": {
            "Moid": "64a2b1007564612d3001234a",
            "ObjectType": "equipment.Chassis",
        },
    },
    {
        "Moid": "64a2b2f97564612d3001234c",
        "ObjectType": "compute.Blade",
        "Serial": "FCH264801XZ",
        "Model": "UCSX-210C-M7",
        "Name": "Chassis-1-Slot-2",
        "OperState": "Operable",
        "SlotId": 2,
        "NumCpus": 2,
        "NumCores": 64,
        "TotalMemory": 1048576,
        "Chassis": {
            "Moid": "64a2b1007564612d3001234a",
            "ObjectType": "equipment.Chassis",
        },
    },
]

IOCARDS_DATA = [
    {
        "Moid": "64a2b3007564612d30012350",
        "ObjectType": "equipment.IoCard",
        "Serial": "QCI26400099",
        "Model": "UCSX-IOM-9108",
        "Name": "Chassis-1-IOM-A",
        "OperState": "Operable",
        "HardwareId": "9108-25G",
    }
]

NETWORK_ELEMENTS_DATA = [
    {
        "Moid": "64a2b4007564612d30012355",
        "ObjectType": "network.Element",
        "Serial": "FOC264200EF",
        "Model": "UCS-FI-6536",
        "Name": "FI-A-Cluster",
        "OperState": "Operable",
        "Version": "4.3(2.2d)",
        "Mode": "Switch",
    }
]

POWER_SUPPLIES_DATA = [
    {
        "Moid": "64a2b5007564612d30012360",
        "ObjectType": "equipment.PowerSupply",
        "Serial": "LIT264501AA",
        "Model": "UCSX-PAC-2500W",
        "Name": "Chassis-1-PSU-1",
        "OperState": "Operable",
        "InputVoltage": 208.0,
        "OutputPower": 620.0,
    },
    {
        "Moid": "64a2b5007564612d30012361",
        "ObjectType": "equipment.PowerSupply",
        "Serial": "LIT264501AB",
        "Model": "UCSX-PAC-2500W",
        "Name": "Chassis-1-PSU-2",
        "OperState": "Operable",
        "InputVoltage": 208.0,
        "OutputPower": 615.0,
    },
]

FANS_DATA = [
    {
        "Moid": "64a2b6007564612d30012365",
        "ObjectType": "equipment.Fan",
        "Serial": "FAN2640001",
        "Model": "UCSX-FAN-VAL",
        "Name": "Chassis-1-Fan-1",
        "OperState": "Operable",
        "Speed": 8400,
    }
]

BOARDS_DATA = [
    {
        "Moid": "64a2b7007564612d3001236a",
        "ObjectType": "equipment.Board",
        "Serial": "BRD2648001",
        "Model": "UCSX-210C-M7-MB",
        "Name": "Blade-1-Motherboard",
        "OperState": "Operable",
        "ComputeBlade": {
            "Moid": "64a2b2f87564612d3001234b",
            "ObjectType": "compute.Blade",
        },
    }
]

PROCESSOR_UNITS_DATA = [
    {
        "Moid": "64a2b8007564612d30012370",
        "ObjectType": "processor.Unit",
        "Model": "Intel Xeon Platinum 8480+",
        "Speed": 2000,
        "NumCores": 32,
        "NumThreads": 64,
        "OperState": "Operable",
        "SocketDesignation": "CPU1",
        "ComputeBlade": {
            "Moid": "64a2b2f87564612d3001234b",
            "ObjectType": "compute.Blade",
        },
    }
]

MEMORY_UNITS_DATA = [
    {
        "Moid": "64a2b9007564612d30012375",
        "ObjectType": "memory.Unit",
        "Capacity": 64000,  # 64 GB
        "Speed": 4800,
        "Type": "DDR5",
        "OperState": "Operable",
        "SocketId": 1,
        "ComputeBlade": {
            "Moid": "64a2b2f87564612d3001234b",
            "ObjectType": "compute.Blade",
        },
    }
]

STORAGE_CONTROLLERS_DATA = [
    {
        "Moid": "64a2ba007564612d30012380",
        "ObjectType": "storage.Controller",
        "Model": "UCS-MRAID-12G",
        "Type": "RAID",
        "OperState": "Operable",
        "ComputeBlade": {
            "Moid": "64a2b2f87564612d3001234b",
            "ObjectType": "compute.Blade",
        },
    }
]

PHYSICAL_DISKS_DATA = [
    {
        "Moid": "64a2bb007564612d30012385",
        "ObjectType": "storage.PhysicalDisk",
        "Capacity": 1920,  # GB SSD
        "Model": "MZVLB1T9HBLT",
        "OperState": "Operable",
        "Protocol": "NVMe",
        "StorageController": {
            "Moid": "64a2ba007564612d30012380",
            "ObjectType": "storage.Controller",
        },
    }
]

FIRMWARE_RUNNING_DATA = [
    {
        "Moid": "64a2bc007564612d30012390",
        "ObjectType": "firmware.RunningFirmware",
        "Component": "BIOS",
        "Version": "5.2.1.node7.0",
        "PackageVersion": "4.3(2.2d)",
        "Type": "BIOS",
    }
]

ETHER_PHYSICAL_PORTS_DATA = [
    {
        "Moid": "64a2bd007564612d30012395",
        "ObjectType": "ether.PhysicalPort",
        "PortId": 1,
        "SlotId": 1,
        "Speed": "25000",
        "OperState": "Up",
        "AdminState": "Enabled",
        "NetworkElement": {
            "Moid": "64a2b4007564612d30012355",
            "ObjectType": "network.Element",
        },
    }
]

FC_PHYSICAL_PORTS_DATA = [
    {
        "Moid": "64a2be007564612d300123a0",
        "ObjectType": "fc.PhysicalPort",
        "PortId": 33,
        "Speed": "32G",
        "OperState": "Up",
        "AdminState": "Enabled",
    }
]

ALARMS_DATA = [
    {
        "Moid": "64a2bf007564612d300123a5",
        "ObjectType": "cond.Alarm",
        "Code": "F0529",
        "Severity": "Warning",
        "Description": (
            "Fan module Chassis-1-Fan-2 running slightly elevated RPMs."
        ),
        "AffectedObject": (
            "equipment.Fan/64a2b6007564612d30012365"
        ),
        "Acknowledged": "False",
    }
]

TIME_SERIES_DATA = [
    {
        "Timestamp": "2026-11-12T18:00:00Z",
        "Moid": "64a2b1007564612d3001234a",
        "MetricName": "ChassisPowerUsageWatt",
        "Value": 1450.5,
    },
    {
        "Timestamp": "2026-11-12T18:00:00Z",
        "Moid": "64a2b1007564612d3001234a",
        "MetricName": "ChassisInletTemperatureCelsius",
        "Value": 23.0,
    },
]


# ==========================================
# OData Query Engine Helper
# ==========================================


def apply_odata_query(
    data: List[Dict[str, Any]],
    top: Optional[int] = None,
    skip: Optional[int] = None,
    filter_expr: Optional[str] = None,
    select_expr: Optional[str] = None,
):
    result = data

    # Simple filter handling (e.g. OperState eq 'Operable')
    if filter_expr:
        try:
            parts = filter_expr.split(" ")
            if len(parts) >= 3:
                field = parts[0].strip()
                op = parts[1].strip()
                val = parts[2].strip().strip("'\"")
                if op.lower() == "eq":
                    result = [
                        item
                        for item in result
                        if str(item.get(field, "")) == val
                    ]
        except Exception:
            pass  # Fallback to unfiltered dataset if expression parsing fails

    # Skip
    if skip and skip > 0:
        result = result[skip:]

    # Top
    if top and top >= 0:
        result = result[:top]

    # Select projection
    if select_expr:
        fields = [f.strip() for f in select_expr.split(",")]
        projected = []
        for item in result:
            proj_item = {
                k: v for k, v in item.items() if k in fields or k == "Moid"
            }
            projected.append(proj_item)
        result = projected

    return {"Count": len(result), "Results": result}


# ==========================================
# FastAPI Endpoints (Full UCS-X Surface)
# ==========================================


@app.get("/api/v1/equipment/Chassis")
def get_chassis(
    top: Optional[int] = Query(None, alias="$top"),
    skip: Optional[int] = Query(None, alias="$skip"),
    filter: Optional[str] = Query(None, alias="$filter"),
    select: Optional[str] = Query(None, alias="$select"),
    signature: Optional[str] = Header(None, alias="Signature"),
):
    return apply_odata_query(CHASSIS_DATA, top, skip, filter, select)


@app.get("/api/v1/compute/Blades")
def get_blades(
    top: Optional[int] = Query(None, alias="$top"),
    skip: Optional[int] = Query(None, alias="$skip"),
    filter: Optional[str] = Query(None, alias="$filter"),
    select: Optional[str] = Query(None, alias="$select"),
    signature: Optional[str] = Header(None, alias="Signature"),
):
    return apply_odata_query(BLADES_DATA, top, skip, filter, select)


@app.get("/api/v1/equipment/IoCards")
def get_iocards(
    top: Optional[int] = Query(None, alias="$top"),
    skip: Optional[int] = Query(None, alias="$skip"),
    filter: Optional[str] = Query(None, alias="$filter"),
    select: Optional[str] = Query(None, alias="$select"),
    signature: Optional[str] = Header(None, alias="Signature"),
):
    return apply_odata_query(IOCARDS_DATA, top, skip, filter, select)


@app.get("/api/v1/network/Elements")
def get_network_elements(
    top: Optional[int] = Query(None, alias="$top"),
    skip: Optional[int] = Query(None, alias="$skip"),
    filter: Optional[str] = Query(None, alias="$filter"),
    select: Optional[str] = Query(None, alias="$select"),
    signature: Optional[str] = Header(None, alias="Signature"),
):
    return apply_odata_query(NETWORK_ELEMENTS_DATA, top, skip, filter, select)


@app.get("/api/v1/equipment/PowerSupplies")
def get_power_supplies(
    top: Optional[int] = Query(None, alias="$top"),
    skip: Optional[int] = Query(None, alias="$skip"),
    filter: Optional[str] = Query(None, alias="$filter"),
    select: Optional[str] = Query(None, alias="$select"),
    signature: Optional[str] = Header(None, alias="Signature"),
):
    return apply_odata_query(POWER_SUPPLIES_DATA, top, skip, filter, select)


@app.get("/api/v1/equipment/Fans")
def get_fans(
    top: Optional[int] = Query(None, alias="$top"),
    skip: Optional[int] = Query(None, alias="$skip"),
    filter: Optional[str] = Query(None, alias="$filter"),
    select: Optional[str] = Query(None, alias="$select"),
    signature: Optional[str] = Header(None, alias="Signature"),
):
    return apply_odata_query(FANS_DATA, top, skip, filter, select)


@app.get("/api/v1/equipment/Boards")
def get_boards(
    top: Optional[int] = Query(None, alias="$top"),
    skip: Optional[int] = Query(None, alias="$skip"),
    filter: Optional[str] = Query(None, alias="$filter"),
    select: Optional[str] = Query(None, alias="$select"),
    signature: Optional[str] = Header(None, alias="Signature"),
):
    return apply_odata_query(BOARDS_DATA, top, skip, filter, select)


@app.get("/api/v1/processor/Units")
def get_processor_units(
    top: Optional[int] = Query(None, alias="$top"),
    skip: Optional[int] = Query(None, alias="$skip"),
    filter: Optional[str] = Query(None, alias="$filter"),
    select: Optional[str] = Query(None, alias="$select"),
    signature: Optional[str] = Header(None, alias="Signature"),
):
    return apply_odata_query(PROCESSOR_UNITS_DATA, top, skip, filter, select)


@app.get("/api/v1/memory/Units")
def get_memory_units(
    top: Optional[int] = Query(None, alias="$top"),
    skip: Optional[int] = Query(None, alias="$skip"),
    filter: Optional[str] = Query(None, alias="$filter"),
    select: Optional[str] = Query(None, alias="$select"),
    signature: Optional[str] = Header(None, alias="Signature"),
):
    return apply_odata_query(MEMORY_UNITS_DATA, top, skip, filter, select)


@app.get("/api/v1/storage/Controllers")
def get_storage_controllers(
    top: Optional[int] = Query(None, alias="$top"),
    skip: Optional[int] = Query(None, alias="$skip"),
    filter: Optional[str] = Query(None, alias="$filter"),
    select: Optional[str] = Query(None, alias="$select"),
    signature: Optional[str] = Header(None, alias="Signature"),
):
    return apply_odata_query(
        STORAGE_CONTROLLERS_DATA, top, skip, filter, select
    )


@app.get("/api/v1/storage/PhysicalDisks")
def get_physical_disks(
    top: Optional[int] = Query(None, alias="$top"),
    skip: Optional[int] = Query(None, alias="$skip"),
    filter: Optional[str] = Query(None, alias="$filter"),
    select: Optional[str] = Query(None, alias="$select"),
    signature: Optional[str] = Header(None, alias="Signature"),
):
    return apply_odata_query(PHYSICAL_DISKS_DATA, top, skip, filter, select)


@app.get("/api/v1/firmware/RunningFirmwares")
def get_running_firmware(
    top: Optional[int] = Query(None, alias="$top"),
    skip: Optional[int] = Query(None, alias="$skip"),
    filter: Optional[str] = Query(None, alias="$filter"),
    select: Optional[str] = Query(None, alias="$select"),
    signature: Optional[str] = Header(None, alias="Signature"),
):
    return apply_odata_query(FIRMWARE_RUNNING_DATA, top, skip, filter, select)


@app.get("/api/v1/ether/PhysicalPorts")
def get_ether_ports(
    top: Optional[int] = Query(None, alias="$top"),
    skip: Optional[int] = Query(None, alias="$skip"),
    filter: Optional[str] = Query(None, alias="$filter"),
    select: Optional[str] = Query(None, alias="$select"),
    signature: Optional[str] = Header(None, alias="Signature"),
):
    return apply_odata_query(
        ETHER_PHYSICAL_PORTS_DATA, top, skip, filter, select
    )


@app.get("/api/v1/fc/PhysicalPorts")
def get_fc_ports(
    top: Optional[int] = Query(None, alias="$top"),
    skip: Optional[int] = Query(None, alias="$skip"),
    filter: Optional[str] = Query(None, alias="$filter"),
    select: Optional[str] = Query(None, alias="$select"),
    signature: Optional[str] = Header(None, alias="Signature"),
):
    return apply_odata_query(FC_PHYSICAL_PORTS_DATA, top, skip, filter, select)


@app.get("/api/v1/cond/Alarms")
def get_alarms(
    top: Optional[int] = Query(None, alias="$top"),
    skip: Optional[int] = Query(None, alias="$skip"),
    filter: Optional[str] = Query(None, alias="$filter"),
    select: Optional[str] = Query(None, alias="$select"),
    signature: Optional[str] = Header(None, alias="Signature"),
):
    return apply_odata_query(ALARMS_DATA, top, skip, filter, select)


@app.get("/api/v1/telemetry/TimeSeries")
def get_timeseries(
    top: Optional[int] = Query(None, alias="$top"),
    skip: Optional[int] = Query(None, alias="$skip"),
    filter: Optional[str] = Query(None, alias="$filter"),
    select: Optional[str] = Query(None, alias="$select"),
    signature: Optional[str] = Header(None, alias="Signature"),
):
    return apply_odata_query(TIME_SERIES_DATA, top, skip, filter, select)


if __name__ == "__main__":
    uvicorn.run(
        "intersight_emulator:app", host="127.0.0.1", port=8080, reload=True
    )