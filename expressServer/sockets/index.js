const getCurrentRecording = (socket, app) => {
    const currRecording = app.get("currRecording");
    const db = app.get("db");
    if (currRecording === null) {
        return;
    }
    db.getCoordinatesByRecordId(currRecording)
        .then((e) => {
            const currRecordingHistory = e.rows;
            socket.emit("currRecordingHistory", currRecordingHistory);
        })
        .catch((e) => {
            socket.emit("currRecordingHistory", null);
        });
};

module.exports = { getCurrentRecording };
