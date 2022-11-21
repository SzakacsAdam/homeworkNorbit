import Map from "https://cdn.skypack.dev/ol/Map.js";
import View from "https://cdn.skypack.dev/ol/View.js";
import TileLayer from "https://cdn.skypack.dev/ol/layer/Tile.js";
import OSM from "https://cdn.skypack.dev/ol/source/OSM.js";

const init = () => {
    const map = new Map({
        target: "map",
        layers: [
            new TileLayer({
                source: new OSM(),
            }),
        ],
        view: new View({
            center: [0, 0],
            zoom: 2,
        }),
    });
};
const socket = io();

socket.on("newCoord", (coord) => {
    console.log(coord);
});
socket.on("currRecordingHistory", (currRecordingHistory) => {
    console.log(currRecordingHistory);
});

window.onload = init;
