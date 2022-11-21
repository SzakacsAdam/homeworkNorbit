ALTER TABLE IF EXISTS coordinates
    DROP CONSTRAINT IF EXISTS "fk_boat",
    DROP CONSTRAINT IF EXISTS "fk_record";

DROP TABLE IF EXISTS boats;
DROP TABLE IF EXISTS recordings;
DROP TABLE IF EXISTS coordinates;


CREATE TABLE boats
(
    "id"   SERIAL PRIMARY KEY,
    "name" VARCHAR(255) UNIQUE NOT NULL
);
CREATE TABLE recordings
(
    "id"        SERIAL PRIMARY KEY,
    "name"      VARCHAR(255) UNIQUE NOT NULL,
    "create_at" TIMESTAMPTZ         NOT NULL DEFAULT NOW()
);

CREATE TABLE coordinates
(
    "id"        SERIAL PRIMARY KEY,
    "lat"       float8      NOT NULL,
    "lon"       float8      NOT NULL,
    "heading"   float8      NOT NULL,
    "boat_id"   INT         NOT NULL,
    "create_at" TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    "record_id" INT
);
ALTER TABLE coordinates
    ADD CONSTRAINT fk_boat FOREIGN KEY (boat_id) REFERENCES boats ("id"),
    ADD CONSTRAINT fk_record FOREIGN KEY (record_id) REFERENCES recordings ("id");
