# Cisco Intersight UCS X-Series Mock API

A lightweight [FastAPI](https://fastapi.tiangolo.com/) emulator that mimics a subset of the Cisco Intersight REST API for **UCS X-Series** infrastructure. It serves static, in-memory datasets (chassis, blades, IO cards, fabric interconnects, power/cooling, CPU/memory/storage, firmware, ports, alarms and telemetry) so you can develop and test Intersight integrations, collectors, dashboards or monitoring extensions without access to a real Intersight tenant or physical hardware.

## Features

- Single-file server: [intersight_emulator.py](intersight_emulator.py)
- Intersight-style paths under `/api/v1/<namespace>/<Resource>`
- Responses shaped like Intersight list results: `{"Count": <n>, "Results": [...]}`
- Basic OData query support: `$top`, `$skip`, `$filter` (`eq` only), `$select`
- Accepts (and ignores) the Intersight `Signature` header, so clients that sign requests work unchanged. **No authentication is performed.**
- Interactive Swagger UI at `/docs` and OpenAPI schema at `/openapi.json`

## Requirements

- Python 3.9+
- `fastapi` and `uvicorn`

```bash
pip install fastapi uvicorn
```

## Run locally

```bash
python -m venv venv
# Linux/macOS: source venv/bin/activate
# Windows:     venv\Scripts\activate
pip install fastapi uvicorn
python intersight_emulator.py
```

Running the script directly starts the server on `http://127.0.0.1:8080` with auto-reload (local access only). Open <http://127.0.0.1:8080/docs> to explore the API.

Quick test:

```bash
curl "http://127.0.0.1:8080/api/v1/compute/Blades?\$top=1"
```

## API endpoints

All endpoints are `GET` and accept the same query parameters (see [OData support](#odata-query-support)).

| Endpoint | Intersight object type | Dataset contents |
|---|---|---|
| `/api/v1/equipment/Chassis` | `equipment.Chassis` | 1 × UCSX-9508 chassis (8 slots, 10 kW capacity) |
| `/api/v1/compute/Blades` | `compute.Blade` | 2 × UCSX-210C-M7 blades (2 CPUs, 64 cores, 1 TB RAM each), linked to the chassis |
| `/api/v1/equipment/IoCards` | `equipment.IoCard` | 1 × UCSX-IOM-9108 IO module |
| `/api/v1/network/Elements` | `network.Element` | 1 × UCS-FI-6536 fabric interconnect (firmware 4.3(2.2d)) |
| `/api/v1/equipment/PowerSupplies` | `equipment.PowerSupply` | 2 × UCSX-PAC-2500W PSUs (input voltage, output power) |
| `/api/v1/equipment/Fans` | `equipment.Fan` | 1 × fan module (RPM speed) |
| `/api/v1/equipment/Boards` | `equipment.Board` | 1 × blade motherboard, linked to blade 1 |
| `/api/v1/processor/Units` | `processor.Unit` | 1 × Intel Xeon Platinum 8480+ (32 cores / 64 threads) |
| `/api/v1/memory/Units` | `memory.Unit` | 1 × 64 GB DDR5-4800 DIMM |
| `/api/v1/storage/Controllers` | `storage.Controller` | 1 × UCS-MRAID-12G RAID controller |
| `/api/v1/storage/PhysicalDisks` | `storage.PhysicalDisk` | 1 × 1.92 TB NVMe SSD, linked to the controller |
| `/api/v1/firmware/RunningFirmwares` | `firmware.RunningFirmware` | BIOS running firmware entry |
| `/api/v1/ether/PhysicalPorts` | `ether.PhysicalPort` | 1 × 25G Ethernet port on the fabric interconnect |
| `/api/v1/fc/PhysicalPorts` | `fc.PhysicalPort` | 1 × 32G Fibre Channel port |
| `/api/v1/cond/Alarms` | `cond.Alarm` | 1 × Warning alarm (F0529, elevated fan RPM) |
| `/api/v1/telemetry/TimeSeries` | *(telemetry)* | 2 data points: `ChassisPowerUsageWatt` (1450.5) and `ChassisInletTemperatureCelsius` (23.0) |

Built-in FastAPI routes: `/docs` (Swagger UI), `/redoc`, `/openapi.json`.

### Datasets

Datasets are plain Python lists defined at the top of [intersight_emulator.py](intersight_emulator.py) (`CHASSIS_DATA`, `BLADES_DATA`, `IOCARDS_DATA`, `NETWORK_ELEMENTS_DATA`, `POWER_SUPPLIES_DATA`, `FANS_DATA`, `BOARDS_DATA`, `PROCESSOR_UNITS_DATA`, `MEMORY_UNITS_DATA`, `STORAGE_CONTROLLERS_DATA`, `PHYSICAL_DISKS_DATA`, `FIRMWARE_RUNNING_DATA`, `ETHER_PHYSICAL_PORTS_DATA`, `FC_PHYSICAL_PORTS_DATA`, `ALARMS_DATA`, `TIME_SERIES_DATA`). Every record has a `Moid` and (except telemetry) an `ObjectType`. Child objects reference their parent through a relationship stub such as `{"Moid": "...", "ObjectType": "equipment.Chassis"}`.

The data is static and read-only; to change what the emulator returns, edit these lists and restart. Add more entries to simulate larger environments.

### OData query support

| Parameter | Behaviour |
|---|---|
| `$top=N` | Return at most N results |
| `$skip=N` | Skip the first N results |
| `$filter=<Field> eq '<value>'` | Exact string-equality match on a single top-level field. Other operators, `and`/`or`, and nested fields are **not** supported; an unparseable filter is ignored and returns the unfiltered set. Values containing spaces are not supported. |
| `$select=A,B` | Return only the listed fields (`Moid` is always included) |

Order of evaluation: `$filter` → `$skip` → `$top` → `$select`. `Count` reflects the number of returned results, not the total dataset size.

Examples:

```bash
curl "http://<host>:8080/api/v1/equipment/Chassis"
curl "http://<host>:8080/api/v1/compute/Blades?\$filter=OperState%20eq%20'Operable'&\$select=Name,Serial"
curl "http://<host>:8080/api/v1/cond/Alarms?\$filter=Severity%20eq%20'Warning'"
curl "http://<host>:8080/api/v1/telemetry/TimeSeries?\$top=1"
```

Sample response:

```json
{
  "Count": 1,
  "Results": [
    {
      "Moid": "64a2b1007564612d3001234a",
      "ObjectType": "equipment.Chassis",
      "Serial": "FOX264500AB",
      "Model": "UCSX-9508",
      "Name": "Chassis-1",
      "OperState": "Operable",
      "NumSlots": 8,
      "TotalPowerCapacity": 10000,
      "ScaledMode": "NotSupported"
    }
  ]
}
```

## Deploying on a cloud VM

The script binds to `127.0.0.1` by default, which is unreachable from outside the VM. On a cloud VM, **start it with the `uvicorn` CLI and `--host 0.0.0.0`** instead of `python intersight_emulator.py`:

```bash
uvicorn intersight_emulator:app --host 0.0.0.0 --port 8080
```

> **Security note:** the emulator has no authentication or TLS. Restrict inbound access to trusted IP ranges (your own IP or corporate CIDR), never `0.0.0.0/0`, and don't load real data into it. For production-like exposure, put it behind a reverse proxy with TLS.

### Common setup (Ubuntu 22.04/24.04 on either cloud)

```bash
sudo apt update && sudo apt install -y python3 python3-venv python3-pip git
git clone <your-repo-url> intersight-emulator
cd intersight-emulator
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt     # or: pip install fastapi uvicorn
uvicorn intersight_emulator:app --host 0.0.0.0 --port 8080
```

#### Run as a service (systemd)

Create `/etc/systemd/system/intersight-emulator.service` (adjust `User` and paths — `ubuntu` on EC2, your admin username on Azure):

```ini
[Unit]
Description=Cisco Intersight Mock API
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/intersight-emulator
ExecStart=/home/ubuntu/intersight-emulator/venv/bin/uvicorn intersight_emulator:app --host 0.0.0.0 --port 8080
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now intersight-emulator
sudo systemctl status intersight-emulator
```

### AWS EC2

1. **Launch an instance** — Ubuntu 22.04/24.04 LTS, `t3.micro` (or `t4g.micro`) is plenty. Create or select a key pair.
2. **Security group** — add an inbound rule: *Custom TCP*, port **8080**, source **My IP** (or your trusted CIDR). Keep SSH (22) restricted too.
3. **Connect:**
   ```bash
   ssh -i your-key.pem ubuntu@<ec2-public-ip>
   ```
   (Use `ec2-user` and `sudo dnf install -y python3 git` on Amazon Linux 2023.)
4. Follow the [common setup](#common-setup-ubuntu-22042404-on-either-cloud) above, optionally with the systemd service.
5. **Test:** `http://<ec2-public-ip>:8080/docs` or
   ```bash
   curl "http://<ec2-public-ip>:8080/api/v1/equipment/Chassis"
   ```

AWS CLI alternative for opening the port:

```bash
aws ec2 authorize-security-group-ingress --group-id <sg-id> \
  --protocol tcp --port 8080 --cidr <your-ip>/32
```

### Azure VM

1. **Create a VM** — Ubuntu Server 22.04/24.04 LTS, size `Standard_B1s` or larger, SSH public key authentication.
2. **Network security group** — add an inbound security rule: destination port **8080**, protocol TCP, source = your IP / trusted CIDR.
3. **Connect:**
   ```bash
   ssh azureuser@<vm-public-ip>
   ```
4. Follow the [common setup](#common-setup-ubuntu-22042404-on-either-cloud) above, optionally with the systemd service (`User=azureuser`).
5. **Test:** `http://<vm-public-ip>:8080/docs` or
   ```bash
   curl "http://<vm-public-ip>:8080/api/v1/equipment/Chassis"
   ```

Azure CLI alternative for opening the port:

```bash
az vm open-port --resource-group <rg> --name <vm-name> --port 8080 --priority 1010
```

(`az vm open-port` allows traffic from any source; tighten the source on the generated NSG rule afterwards.)

### Optional: Docker

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY intersight_emulator.py requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8080
CMD ["uvicorn", "intersight_emulator:app", "--host", "0.0.0.0", "--port", "8080"]
```

```bash
docker build -t intersight-emulator .
docker run -d -p 8080:8080 --restart unless-stopped intersight-emulator
```

## Pointing a client at the emulator

Set your Intersight client's base URL to `http://<host>:8080` instead of `https://intersight.com`. Clients that sign requests will still work because the `Signature` header is accepted and ignored. Note that real Intersight uses HTTPS; clients that enforce TLS will need a TLS-terminating proxy in front of the emulator.

## Limitations

- Read-only (`GET` only); no `POST`/`PATCH`/`DELETE`.
- Small, static datasets; no persistence.
- Minimal OData: single `eq` filter, no `$orderby`, `$expand`, `$count`, or `$apply`.
- No authentication or request signature validation.
