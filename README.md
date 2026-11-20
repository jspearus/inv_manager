# Hardware Store

A small Django inventory app for tracking electronic components by name, value, description, quantity, and location. It includes a web interface and a REST API suitable for future integrations.

## Requirements

- Python 3.10+

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to manage components.

## Access from another device on your LAN

On the computer running Django, find its LAN address with:

```bash
ip -4 -o addr show scope global
```

Set `DJANGO_ALLOWED_HOSTS` to include that address, then start the development server so it listens for connections from other devices:

```bash
export DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,192.168.1.xx
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

Replace `192.168.1.30` with the computer's current LAN address. From another device on the same network, open `http://192.168.1.30:8000/`. If the address changes, update the allowlist and URL. Your firewall must also allow inbound connections on port 8000.

This development server and API have no authentication: anyone who can reach them on the network can view, add, change, or delete inventory. Use only on a trusted private network; do not port-forward it or expose it to the internet.

## REST API

- `GET /api/components/` — list components
- `POST /api/components/` — add a component
- `GET /api/components/{id}/` — retrieve a component
- `PUT` or `PATCH /api/components/{id}/` — update a component
- `DELETE /api/components/{id}/` — remove a component
- `GET /api/components/?search=resist` — search by partial text in name, value, description, or location

Example:

```json
{
  "name": "Resistor",
  "value": "10kΩ",
  "description": "Carbon film, 1/4 watt",
  "quantity": 25,
  "location": "Drawer A3"
}
```

The inventory page also has a search box for finding components by partial text in name, value, description, or location. Existing components keep their current names; value and description start blank and can be filled in when edited.

The API currently has no authentication. Add authentication and set a production secret key, `DJANGO_DEBUG=false`, and `DJANGO_ALLOWED_HOSTS` before using it outside a trusted local network or connecting an external agent.

Run tests with `python manage.py test`.
