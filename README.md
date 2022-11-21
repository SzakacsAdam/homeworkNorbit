# Web developer Homework for Norbit 09.01.2022.

## Overview

-   CoordintaeMockApp:

    -   provides coordinates in json via socket
    -   parse csv files into dict
    -   handling multiple connections
    -   AppDetails:

        -   app.py:
            -   add RESOURCE_PATH directory path
            -   OPTIONAL: choose between InMemory or DirectReader Collection
            -   OPTIONAL: change http server
        -   HTTP socket on port 25_000
        -   example ouput:

            ```json
            [
                {
                    "lat": 48.21339894,
                    "lon": 20.73998593,
                    "heading": 3.470315226,
                    "name": "filename"
                }
            ]
            ```

-   expressServer:
    -   reads CoordintaeMockApp socket
    -   CRUD database
    -   provide REST API routes for frontend
    -   provides socket-io for frontend
    -   API Routes:
        -   GET /api/recordings
        -   GET /api/recordings/:recordName
        -   POST /api/recordings/start
        -   POST /api/recordings/stop
    -   socketIO:
        -   connection
        -   (positively extensible)

## Installation guide

-   CoordintaeMockApp

    ```bash
        pip install . && python3 app.py
    ```

-   expressServer
    ```bash
         npm install && npm start
    ```
-   postgresql datababase
    -   "db_schema.sql": table creation
