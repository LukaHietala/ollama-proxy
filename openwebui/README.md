## Ympäristö

1. Luo virtuaali ympäristö

2. Täytä .env tiedosto ympäristömuuttujilla

```bash
OPENWEBUI_BASE_URL=
OPENWEBUI_API_KEY=
OPENWEBUI_MODEL=
PORT=
```

3. Asenna ja käynnistä

```sh
pip install -r requirements.txt
python app.py
```

## API Endpointit

Tarkistaa yhteyden tekoäly palvelimeen

```
GET /api/health
```

Hakee mallit

```
GET /api/models
```

Lähettää viestin mallille

```
POST /api/chat
Content-Type: application/json
{
  "message": "Hei nao!"
}
```

Tyhjentää keskustelun historian

```
POST /api/chat/clear
```

## Vastaus formaatti

Success response

```json
{
  "success": true,
  "data": { ... },
  "message": "Valinnainen viesti"
}
```

Error response

```json
{
    "success": false,
    "error": "Virhe viesti"
}
```

> Endpointit voi testata test.py skriptillä

## OpenWebUI Palvelin

Valmistele Arch tai Debian pohjainen Linux, esim. KVM virtuaali koneessa

Tarvittavat ohjelmistot:

-   Ollama
-   Docker

Docker ympäristön starttaminen

```bash
docker run -d --network=host -v open-webui:/app/backend/data -e OLLAMA_BASE_URL=http://127.0.0.1:11434 --name open-webui --restart always ghcr.io/open-webui/open-webui:main
```
