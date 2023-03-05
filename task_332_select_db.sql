
--      Домашнее задание по теме 3 «SELECT-запросы, выборки из одной таблицы».


-- 3.1 Находит название и год выхода альбомов, вышедших в 2018 году.
SELECT name, year FROM albums
WHERE year = 2018;

-- 3.2 Находит название и продолжительность самого длительного трека.
SELECT name, duration FROM tracks
WHERE duration = (SELECT MAX(duration) FROM tracks);

-- 3.3 Находит названия треков, продолжительность которых не менее 3,5 минут.
SELECT name FROM tracks
WHERE duration >= 210;

-- 3.4 Находит названия сборников, вышедших в период с 2018 по 2020 год включительно.
SELECT name FROM collections
WHERE year >= 2018 AND year <= 2020;

-- 3.5 Находит исполнителей, чьё имя состоит из одного слова.
SELECT nickname FROM singers
WHERE NOT (nickname LIKE '% %' OR nickname LIKE '%-%');
--WHERE nickname NOT LIKE '% %' AND nickname NOT LIKE '%-%';

-- 3.6 Находит названия треков, которые содержат слово «мой» или «my».
SELECT name FROM tracks
WHERE name LIKE '%мой%' OR name LIKE '%my%';
