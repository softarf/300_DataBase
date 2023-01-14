
CREATE TABLE IF NOT EXISTS genres (
	genre_id sereal PRIMARY KEY,
	name varchar(60) NOT NULL
);

CREATE TABLE IF NOT EXISTS singers (
	singer_id sereal PRIMARY KEY,
	nickname varchar(60) NOT NULL
);

CREATE TABLE IF NOT EXISTS genres_singers (
	genre_singer_id sereal PRIMARY KEY,
	genre_id integer NOT NULL REFERENCES genres,
	singer_id integer NOT NULL REFERENCES singers
);

CREATE TABLE IF NOT EXISTS albums (
	album_id sereal PRIMARY KEY,
	name varchar(120) NOT NULL,
	year integer CHECK (year > 1900)
);

CREATE TABLE IF NOT EXISTS singers_albums (
	singer_album_id sereal PRIMARY KEY,
	singer_id integer NOT NULL REFERENCES singers,
	album_id integer NOT NULL REFERENCES albums
);

CREATE TABLE IF NOT EXISTS tracks (
	track_id sereal PRIMARY KEY,
	name varchar(120) NOT NULL,
	duration integer CHECK (duration > 0),
	album_id integer NOT NULL REFERENCES albums
);

CREATE TABLE IF NOT EXISTS collections (
	collection_id sereal PRIMARY KEY,
	name varchar(120) NOT NULL,
	year integer CHECK (year > 1900)
);

CREATE TABLE IF NOT EXISTS tracks_collections (
	track_id integer REFERENCES tracks,
	collection_id integer REFERENCES collections,
	CONSTRAINT pk PRIMARY KEY (track_id, collection_id)
);
