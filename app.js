const express = require("express");
const axios = require("axios");
const app = express();
const port = 4321;
const path = require("node:path");
const fs = require("node:fs");

app.use(express.json());

app.get("/", (req, res) => {
    res.send("paivaa!");
});

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});

const RAG_FIlE_PATH = path.join(__dirname, "rag.txt");

const SYSTEM_PROMPT = `You're friendly robot named Nao. \n History: \n`;

app.post("/api", async (req, res) => {
    let history = "";
    try {
        history = await fs.promises.readFile(RAG_FIlE_PATH, "utf8");
    } catch (err) {
        console.error(err);
        return res.status(500).send("Error reading history file");
    }

    try {
        await fs.promises.appendFile(
            RAG_FIlE_PATH,
            `\nUser: ${req.body.content}\n`
        );
    } catch (err) {
        console.error(err);
        return res.status(500).send("Error writing to history file");
    }

    try {
        const response = await axios.post(
            "http://localhost:11434/api/chat",
            {
                model: "qwen2.5:14b",
                stream: false,
                messages: [
                    {
                        role: "system",
                        content: SYSTEM_PROMPT + history,
                    },
                    { role: "user", content: req.body.content },
                ],
            },
            {
                headers: {
                    "Content-Type": "application/json",
                },
            }
        );

        const botResponse = response.data.message.content;

        await fs.promises.appendFile(RAG_FIlE_PATH, `System: ${botResponse}\n`);

        res.json(response.data);
    } catch (error) {
        console.error("Virhe API pyynnössä:", error);
        res.status(500).send(":(");
    }
});

app.post("/delete", async (req, res) => {
    try {
        await fs.promises.writeFile(RAG_FIlE_PATH, "");
        res.send("History cleared");
    } catch (err) {
        console.error(err);
        res.status(500).send("Error clearing history file");
    }
});
