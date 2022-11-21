const router = require("express").Router();

// /api/recordings/
router.get("/", (req, res) => {
    const db = req.app.get("db");
    db.getAllRecordings()
        .then((e) => {
            res.json({ recodrings: e.rows });
        })
        .catch((e) => {
            res.json({ recodrings: [] });
        });
});

// /api/recordings/:recordName
router.get("/:name", (req, res) => {
    const name = req.params.name;
    const db = req.app.get("db");
    db.getRecordingByName(name)
        .then((e) => {
            const matches = e.rows;
            res.json({ matches: matches });
        })
        .catch((e) => {
            res.json({ matches: "no match found" });
        });
});

// /api/recordings/start
router.post("/start", (req, res) => {
    const db = req.app.get("db");
    const currRecording = req.app.get("currRecording");
    const name = req.body.name;
    if (currRecording === null) {
        db.checkRecordingExists(name).then((e) => {
            if (e === false) {
                db.insertRecording(name).then((e) => {
                    const recordingId = e.rows[0].id;
                    req.app.set("currRecording", recordingId);
                    res.json({ startRecording: recordingId });
                });
            } else {
                res.json({ startRecording: "name already exists" });
            }
        });
        return;
    }
    res.json({ currRecording: currRecording });
});

// /api/recordings/stop
router.post("/stop", (req, res) => {
    const currRecording = req.app.get("currRecording");
    if (currRecording === null) {
        res.json({ stopRecording: "not recording" });
        return;
    }
    res.json({ stopRecording: `${currRecording} recording stopped` });
    req.app.set("currRecording", null);
});

module.exports = router;
