## Ympäristö

1. Luo virtuaaliympäristö

```sh
python -m venv venv
source venv/bin/activate
```

2. Kopioi `.env.example` tiedosto nimellä `.env` ja täytä siihen oikeat arvot:

```env
OPENWEBUI_BASE_URL=
OPENWEBUI_API_KEY=
OPENWEBUI_MODEL=
PORT=
```

3. Asenna riippuvuudet ja käynnistä palvelin

```sh
pip install -r requirements.txt
python app.py
```

## API endpointit

Tarkista palvelimen tila

```
GET /api/health
```

Hae käytettävissä olevat mallit

```
GET /api/models
```

Lähetä viesti mallille

```
POST /api/chat
Content-Type: application/json

{
  "message": "Hei nao!"
}
```

Tyhjennä keskusteluhistoria

```
POST /api/chat/clear
```

## Vastausmuodot

Onnistunut vastaus

```json
{
  "success": true,
  "data": { ... },
  "message": "Valinnainen viesti"
}
```

Virhevastaus

```json
{
    "success": false,
    "error": "Virheviesti"
}
```

> Rajapintoja voi testata ajamalla `python test.py` tai testata niiden nopeutta `python perftest.py` skriptillä.

## OpenWebUI palvelin

Valmistele Arch tai Debian pohjanen Linux (esim. VM).

Tarvittavat ohjelmistot:

-   Ollama
-   Docker

Käynnistä OpenWebUI Dockerilla:

```sh
docker run -d --network=host -v open-webui:/app/backend/data -e OLLAMA_BASE_URL=http://127.0.0.1:11434 --name open-webui --restart always ghcr.io/open-webui/open-webui:main
```

> Elää portilla `8080`

Ja käynnistä Ollama:

```sh
OLLAMA_HOST=127.0.0.1:3000 ollama serve
```

> Ollamassa on bugi minkä vuoksi `OLLAMA_HOST` on asetettava, https://github.com/ollama/ollama/issues/707
