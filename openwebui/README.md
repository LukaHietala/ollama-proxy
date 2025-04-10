## API Endpoints

Hakee mallit

```
GET /api/models
```

Lähetä viesti mallille. Palauttaa vastauksen

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
