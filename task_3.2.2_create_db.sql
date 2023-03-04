
CREATE TABLE IF NOT EXISTS genres (
    genre_id SERIAL PRIMARY KEY,
    name VARCHAR(60) NOT NULL
);

CREATE TABLE IF NOT EXISTS singers (
    singer_id SERIAL PRIMARY KEY,
    nickname VARCHAR(60) NOT NULL
);

CREATE TABLE IF NOT EXISTS genres_singers (
    genre_singer_id SERIAL PRIMARY KEY,
    genre_id INTEGER REFERENCES genres,
    singer_id INTEGER REFERENCES singers
);

CREATE TABLE IF NOT EXISTS albums (
    album_id SERIAL PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    year INTEGER CHECK (year > 1900)
);

CREATE TABLE IF NOT EXISTS singers_albums (
    singer_album_id SERIAL PRIMARY KEY,                   -- Первичный ключ, допускающий повторение комбинации. --
    singer_id INTEGER REFERENCES singers,
    album_id INTEGER REFERENCES albums
);

CREATE TABLE IF NOT EXISTS tracks (
    track_id SERIAL PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    duration INTEGER CHECK (duration > 0),
    album_id INTEGER REFERENCES albums
);

CREATE TABLE IF NOT EXISTS collections (
    collection_id SERIAL PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    year INTEGER CHECK (year > 1900)
);

CREATE TABLE IF NOT EXISTS tracks_collections (
    track_id INTEGER REFERENCES tracks,
    collection_id INTEGER REFERENCES collections,
    CONSTRAINT pk PRIMARY KEY (track_id, collection_id)   -- Составной первичный ключ, исключающий повторение комбинации. --
);
