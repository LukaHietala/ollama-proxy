const express = require("express");
const axios = require("axios");
const app = express();
const port = 4321;

app.use(express.json());

app.get("/", (req, res) => {
    res.send("paivaa!");
});

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});

app.post("/api", async (req, res) => {
    try {
        const response = await axios.post(
            "http://localhost:11434/api/chat",
            {
                model: "qwen2.5:14b",
                stream: false,
                messages: [{ role: "user", content: req.body.content }],
            },
            {
                headers: {
                    "Content-Type": "application/json",
                },
            }
        );

        res.json(response.data);
    } catch (error) {
        console.error("Virhe API pyynnössä:", error);
        res.status(500).send(":(");
    }
});
