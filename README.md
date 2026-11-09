# Song

A website for searching and exploring music.

Users can browse songs and artists, search for songs by title, artist, or genre. Each song has its own page with information and a link to listen to it.

Users can register, log in to their profiles, and add songs to their favorites. Administrators can add, edit, and delete songs and artists.

## API

Base path: `/api/`, data format: JSON.

Error: `{"detail": "..."}`

### Songs and Artists

| Method | URL | Description | Parameters / Body | Response |
|---|---|---|---|---|
| GET | `/songs/` | List of songs | `search`, `genre`, `artist`, `ordering` | `200` [song] |
| GET | `/songs/{id}/` | Get a song | — | `200` song, `404` |
| POST | `/songs/` | Add a song | song data | `201` song, `400` |
| PATCH | `/songs/{id}/` | Update a song | updated fields | `200` song, `400`, `404` |
| DELETE | `/songs/{id}/` | Delete a song | — | `204`, `404` |
| GET | `/artists/` | List of artists | `search` | `200` [artist] |
| GET | `/artists/{id}/` | Get an artist | — | `200` artist, `404` |
| GET | `/artists/{id}/songs/` | Artist's songs | — | `200` [song] |
| POST | `/artists/` | Add an artist | `name` | `201` artist, `400` |
| PATCH | `/artists/{id}/` | Update an artist | `name` | `200` artist, `404` |
| DELETE | `/artists/{id}/` | Delete an artist | — | `204`, `404`, `409` |

### Users and Favorites

| Method | URL | Description | Parameters / Body | Response |
|---|---|---|---|---|
| POST | `/auth/register/` | Register a user | `name`, `email`, `password` | `201`, `400` |
| POST | `/auth/login/` | Log in | `email`, `password` | `200`, `401` |
| GET | `/profile/` | Get my profile | — | `200`, `401` |
| PATCH | `/profile/` | Update my profile | updated fields | `200`, `400` |
| GET | `/favorites/` | List of favorite songs | — | `200` [song] |
| POST | `/favorites/` | Add to favorites | `song_id` | `201`, `400` |
| DELETE | `/favorites/{id}/` | Remove from favorites | — | `204`, `404` |

## JSON Examples

**Song:**

```json
{
  "id": 1,
  "title": "No Surprises",
  "artist": 1,
  "genre": "Rock",
  "listen_url": "https://example.com/song",
  "featured_date": null
}
```

**Artist:**

```json
{
  "id": 1,
  "name": "Radiohead"
}
```

**User:**

```json
{
  "id": 1,
  "name": "Ivan",
  "email": "user@example.com",
  "is_admin": false
}
```

**Favorite:**

```json
{
  "id": 1,
  "song_id": 1,
  "user_id": 1
}
```
