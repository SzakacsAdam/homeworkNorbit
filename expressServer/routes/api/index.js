const router = require("express").Router();

router.use("/recordings", require("./recordings"));

module.exports = router;
