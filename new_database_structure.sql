-- Create table for users
CREATE TABLE "users" (
	"id" SERIAL PRIMARY KEY,
	"email" VARCHAR(256), -- Без NULL, т.к. ниже есть проверка.
	"phone_num" VARCHAR(20), -- Телефон обязательно является строкой. Без NULL, т.к. ниже есть проверка.
	"surname" VARCHAR(254) NOT NULL,
	"name" VARCHAR(254) NOT NULL,
	"patronymic" VARCHAR(254),
	CHECK (email IS NOT NULL OR phone_num IS NOT NULL)	-- Проверка хотя бы одного способа связи.
);

-- Create table for regions
CREATE TABLE "regions" (
	"id" SERIAL PRIMARY KEY,
	"title" VARCHAR(254) NOT NULL
);

-- Create table for coords
CREATE TABLE "coords" (
	"id" SERIAL PRIMARY KEY,
	"latitude" NUMERIC(9, 6) NOT NULL,
	"longitude" NUMERIC(10,6) NOT NULL,
	"height" INTEGER NOT NULL
);

-- Create table for areas
CREATE TABLE "pereval_areas" (
	"id" SERIAL PRIMARY KEY,
	"region" INTEGER REFERENCES regions (id) ON DELETE RESTRICT,
	"title" VARCHAR(254) NOT NULL
);

-- Create table for activities_types
CREATE TABLE "activities_types" (
	"id" SERIAL PRIMARY KEY,
	"title" VARCHAR(254) NOT NULL
);

-- Created ENUM for season difficulty
CREATE TYPE season_difficulty AS ENUM ('1A', '1B', '2A', '2B', '3A', '3B'); -- Создание последовательного типа
-- для сохранения целостности данных.


-- Create table perevals
CREATE TABLE "perevals" (
	"id" SERIAL PRIMARY KEY,
	"pereval_area" INTEGER REFERENCES pereval_areas (id) ON DELETE RESTRICT,
	"beauty_title" VARCHAR(254),
	"title" VARCHAR(254) NOT NULL,
	"other_titles" VARCHAR(254),
	"connects" TEXT NOT NULL,
	"add_time" TIMESTAMPTZ NOT NULL DEFAULT NOW(),
	"user" INTEGER REFERENCES users (id) ON DELETE SET NULL,
	"coords" INTEGER REFERENCES coords (id) ON DELETE RESTRICT,
	"winter" season_difficulty, -- Применение последовательного типа.
	"spring" season_difficulty,
	"summer" season_difficulty,
	"autumn" season_difficulty,
	"activity_type" INTEGER REFERENCES activities_types (id) ON DELETE RESTRICT,
	"status" VARCHAR(20) NOT NULL DEFAULT 'new' -- Обязательное поле для модерации.
);

-- Create table for images
CREATE TABLE "images" (
	"id" SERIAL PRIMARY KEY,
	"pereval" INTEGER REFERENCES perevals (id) ON DELETE CASCADE,
	"image"  TEXT
);