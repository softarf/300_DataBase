
--      Домашнее задание по теме 4 «Продвинутая выборка данных»


-- 4.1 Находит количество исполнителей в каждом жанре.
SELECT g.name AS genre_name,
       COUNT(g.name) AS singers_count
    FROM genres AS g
    LEFT JOIN genres_singers AS gs ON gs.genre_id = g.genre_id
    GROUP BY g.name
;


-- 4.2.1 Находит количество треков, вошедших в альбомы 2019–2020 годов. (Реализация: вложенные запросы).
--SELECT an.name,
--       an.year,
--       COUNT(t.name) AS tracks_count
--    FROM
--        (SELECT a.name,
--                a.year,
--                a.album_id
--            FROM albums AS a
--            WHERE year BETWEEN 2019 AND 2020) AS an
--    LEFT JOIN tracks AS t ON t.album_id = an.album_id
--    GROUP BY an.name, an.year;

-- 4.2.2 Находит количество треков, вошедших в альбомы 2019–2020 годов. (Реализация по лекции, CTE).
--WITH an AS (
--    SELECT a.name,
--           a.year,
--           a.album_id
--        FROM albums AS a
--        WHERE year BETWEEN 2019 AND 2020)
--SELECT an.name,
--       an.year,
--       COUNT(t.name) AS tracks_count
--    FROM an
--    LEFT JOIN tracks AS t ON t.album_id = an.album_id
--    GROUP BY an.name, an.year;

-- 4.2                                                               Исправлено после проверки.
SELECT a.name,
       a.year,
       COUNT(t.name) AS tracks_count
    FROM  albums AS a
    LEFT JOIN tracks AS t ON t.album_id = a.album_id
    WHERE year BETWEEN 2019 AND 2020
    GROUP BY a.name, a.YEAR
;


-- 4.3 Находит среднюю продолжительность треков по каждому альбому.
SELECT a.name AS album_name,
       AVG(t.duration) AS avg_length
    FROM albums AS a
    LEFT JOIN tracks AS t ON t.album_id = a.album_id
    GROUP BY a.name
;


-- 4.4 Находит всех исполнителей, которые не выпустили альбомы в 2020 году.
--                 Не понял как реализовать через WITH двойную вложенность.
--SELECT s.nickname AS not_2020
--    FROM singers AS s
--    WHERE s.nickname NOT IN
--        (WITH an AS (
--            SELECT a.name,
--                   a.album_id
--                FROM albums AS a
--                WHERE year = 2020)
--        SELECT nickname
--                FROM an
--                LEFT JOIN singers_albums USING(album_id)
--                LEFT JOIN singers USING(singer_id));

-- 4.4                                                               Исправлено после проверки.
WITH an AS (
    SELECT s.nickname,
           s.singer_id
        FROM singers AS s
        LEFT JOIN singers_albums USING(singer_id)
        LEFT JOIN albums AS a USING(album_id)
        WHERE a.year = 2020)
SELECT s.nickname AS not_2020
    FROM an
    RIGHT JOIN singers AS s USING(singer_id)
    WHERE an.nickname IS NULL
;


-- 4.5 Находит названия сборников, в которых присутствует конкретный исполнитель (выберите его сами).
--SELECT DISTINCT s.nickname,
--       c.name AS collection_name
--    FROM
--        (SELECT singer_id, nickname
--        FROM singers
--        WHERE nickname = 'Тимати') AS s  -- 'Burito' 'Бьянка' 'Григорий Лепс' 'Лариса Долина' 'Мот' 'Стас Михаилов'
----    LEFT JOIN singers_albums AS sa ON sa.singer_id = s.singer_id    -- Без USING(singer_id)
--    LEFT JOIN singers_albums USING(singer_id)
--    LEFT JOIN albums USING(album_id)
--    LEFT JOIN tracks USING(album_id)
--    LEFT JOIN tracks_collections USING(track_id)
--    LEFT JOIN collections AS c USING(collection_id)
--    ORDER BY c.name;

-- 4.5                                                               Исправлено после проверки.
--                                Не считается ресурсозатратным присоединить 5 таблиц, а только потом выделить одного исполнителя?
SELECT DISTINCT s.nickname,
                c.name AS collection_name
    FROM singers AS s
    LEFT JOIN singers_albums USING(singer_id)
    LEFT JOIN albums USING(album_id)
    LEFT JOIN tracks USING(album_id)
    LEFT JOIN tracks_collections USING(track_id)
    LEFT JOIN collections AS c USING(collection_id)
    WHERE nickname = 'Тимати'
    ORDER BY c.name
;


-- 4.6 Находит названия альбомов, в которых присутствуют исполнители более чем одного жанра. (Реализация по лекции, CTE).
--WITH g AS (
--    SELECT s.nickname,
--           s.singer_id,
--           COUNT(gs.singer_id) AS genres_count    -- Для проверки.
--        FROM singers AS s
--        LEFT JOIN genres_singers AS gs ON gs.singer_id = s.singer_id
--        GROUP BY s.nickname, s.singer_id
--        HAVING COUNT(gs.singer_id) > 1)
--SELECT a.name AS album_name,
--       g.nickname
--    FROM g
--    LEFT JOIN singers_albums USING(singer_id)
--    LEFT JOIN albums AS a USING(album_id);

-- 4.6                                                               Исправлено после проверки.
--                                     Ресурсозатратность приемлемая?
SELECT a.name AS album_name,
       s.nickname
    FROM genres
    LEFT JOIN genres_singers AS gs USING(genre_id)
    LEFT JOIN singers AS s USING(singer_id)
    LEFT JOIN singers_albums USING(singer_id)
    LEFT JOIN albums AS a USING(album_id)
    GROUP BY a.name, s.nickname
    HAVING COUNT(gs.singer_id) > 1
;


-- 4.7 Находит наименования треков, которые не входят в сборники.
--WITH t AS (
--    SELECT name,
--           track_id,
--           collection_id
--        FROM tracks
--        LEFT JOIN tracks_collections USING(track_id))
--SELECT t.track_id, t.name AS track_name
--    FROM t
--    WHERE t.collection_id IS NULL;

-- 4.7                                                               Исправлено после проверки.
SELECT t.track_id,
       t.name AS track_name
    FROM tracks AS t
    LEFT JOIN tracks_collections AS tc USING(track_id)
    WHERE tc.collection_id IS NULL
;


-- 4.8 Находит исполнителя или исполнителей, написавших самый короткий по продолжительности трек, — теоретически таких треков может быть несколько.
WITH t AS (
    SELECT name,
           duration,
           album_id
        FROM tracks
        WHERE duration = (SELECT MIN(duration) FROM tracks))
SELECT s.nickname AS singer_nickname,
       t.name AS track_name,
       t.duration AS min_duration
    FROM t
    LEFT JOIN albums USING(album_id)
    LEFT JOIN singers_albums USING(album_id)
    LEFT JOIN singers AS s USING(singer_id);

-- Рекомендация от преподавателя по заданию 8. (Остальные задания приняты 21.03.23).
SELECT Artist.Name AS Artist FROM ArtistAlbum
    JOIN Artist ON ArtistAlbum.ArtistId = Artist.Id
    JOIN Album ON ArtistAlbum.AlbumId = Album.Id
    JOIN Track ON Album.Id = Track.AlbumId
    WHERE Track.Duration = (SELECT MIN(Duration) FROM Track);
-- "Перефразировал..."
SELECT s.nickname AS singer_nickname,
       t.name AS track_name,
       t.duration AS min_duration
    FROM singers AS s
    LEFT JOIN singers_albums USING(singer_id)
    LEFT JOIN albums USING(album_id)
    LEFT JOIN tracks AS t USING(album_id)
    WHERE t.duration = (SELECT MIN(duration) FROM tracks)
;


-- 4.9 Находит названия альбомов, содержащих наименьшее количество треков.
WITH tc AS (
    SELECT a.name AS album_name,
           COUNT(t.name) AS tracks_count
        FROM albums AS a
        LEFT JOIN tracks AS t ON t.album_id = a.album_id
        GROUP BY a.name)
SELECT tc.album_name,
       tc.tracks_count
    FROM tc
    WHERE tc.tracks_count = (SELECT MIN(tc.tracks_count) FROM tc);
