const { Pool, Client } = require("pg");

const credentials = {
    user: process.env.POSTGRE_USER || "postgres",
    host: process.env.POSTGRE_HOST || "localhost",
    database: process.env.POSTGRE_DB || "yourdatabase",
    password: process.env.POSTGRE_PASSWD || "yourpassword",
    port: process.env.POSTGRE_PORT || 5432,
};
const pool = new Pool(credentials);

const getBoatByName = async (boatName) => {
    const query = `
        SELECT id, name 
        FROM boats 
        WHERE name = $1
    `;
    const vals = [boatName];
    return await pool.query(query, vals);
};

const insertBoat = async (boatName) => {
    const query = `
        INSERT INTO boats(name)
        VALUES($1)
        RETURNING *
    `;
    const vals = [boatName];
    return await pool.query(query, vals);
};

const checkBoatExists = async (boatName) => {
    const query = `
        SELECT EXISTS(
            SELECT 1 
            FROM boats
            WHERE name = $1
        )
    `;
    const vals = [boatName];
    const result = await pool.query(query, vals);
    return result.rows[0].exists;
};

const getAllRecordings = async () => {
    const query = `
        SELECT name, create_at
        FROM recordings;
    `;
    return await pool.query(query);
};

const checkRecordingExists = async (recordName) => {
    const query = `
        SELECT EXISTS(
            SELECT 1 
            FROM recordings
            WHERE name = $1
        )
    `;
    const vals = [recordName];
    const result = await pool.query(query, vals);
    return result.rows[0].exists;
};

const getRecordingByName = async (recordName) => {
    const query = `
        SELECT name, create_at
        FROM recordings 
        WHERE name = $1;
    `;
    const vals = [recordName];
    return await pool.query(query, vals);
};

const getRecordingById = async (recordId) => {
    const query = `
        SELECT name, create_at
        FROM recordings 
        WHERE id = $1;
    `;
    const vals = [recordId];
    return await pool.query(query, vals);
};
const insertRecording = async (recordName) => {
    const query = `
        INSERT INTO recordings(name)
        VALUES($1)
        RETURNING id;
    `;
    const vals = [recordName];
    return await pool.query(query, vals);
};

const getCoordinatesByRecordId = async (recordId) => {
    const query = `
        SELECT c.lat, c.lon, c.heading, c.create_at, b.name
        FROM coordinates c
        INNER JOIN boats b
            ON c.boat_id = b.id
        WHERE record_id = $1;
    `;
    const vals = [recordId];
    return await pool.query(query, vals);
};

const insertCoordinate = async (coordRecord) => {
    const isBoatExists = await checkBoatExists(coordRecord.boatName);
    let boatIdResult;
    if (isBoatExists === true) {
        boatIdResult = await getBoatByName(coordRecord.boatName);
    } else {
        boatIdResult = await insertBoat(coordRecord.boatName);
    }

    const boatId = boatIdResult.rows[0].id;
    const query = `
        INSERT INTO coordinates(lat, lon, heading, boat_id, record_id)
        VALUES($1, $2, $3, $4, $5)
        RETURNING *
    `;
    const vals = [
        coordRecord.lat, // 1
        coordRecord.lon, // 2
        coordRecord.heading, // 3
        boatId, // 4
        coordRecord.recordId, // 5
    ];
    return await pool.query(query, vals);
};

module.exports = {
    getBoatByName,
    insertBoat,
    checkBoatExists,
    getAllRecordings,
    checkRecordingExists,
    getRecordingByName,
    getRecordingById,
    insertRecording,
    insertCoordinate,
    getCoordinatesByRecordId,
};
