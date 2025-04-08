require("dotenv").config();

const express = require("express");
const axios = require("axios");
const path = require("node:path");
const fs = require("node:fs");

const app = express();

const PORT = process.env.PORT;
const LLM_MODEL = process.env.LLM_MODEL;
const OLLAMA_URL = process.env.OLLAMA_URL;
const RAG_FILE_PATH = path.join(__dirname, "rag.txt");
const SYSTEM_PROMPT = `You're friendly robot named Nao. \n History: \n`;

app.use(express.json());

app.get("/", (req, res) => {
    res.send(
        "<h1>OLama Proxy</h1><img src='https://media.tenor.com/9wFwCf2i5_cAAAAi/pepe-band-pepe.gif' alt='band' />"
    );
});

app.post("/api", async (req, res) => {
    let history = "";

    try {
        history = await fs.promises.readFile(RAG_FILE_PATH, "utf8");
    } catch (err) {
        console.error("Failed to read rag file:", err);
        return res.status(500).send("Error reading conversation history");
    }

    try {
        await fs.promises.appendFile(
            RAG_FILE_PATH,
            `\nUser: ${req.body.content}\n`
        );
    } catch (err) {
        console.error("Failed to append user message to rag file:", err);
        return res.status(500).send("Error saving your message");
    }

    try {
        const response = await axios.post(
            OLLAMA_URL,
            {
                model: LLM_MODEL,
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

        const responseMessage = response.data.message.content;

        await fs.promises.appendFile(
            RAG_FILE_PATH,
            `System: ${responseMessage}\n`
        );

        res.json(response.data);
    } catch (error) {
        console.error("API req failed:", error);
        res.status(500).send("Failed to get response from ollama server");
    }
});

app.post("/delete", async (req, res) => {
    try {
        await fs.promises.writeFile(RAG_FILE_PATH, "");
        res.send("Rag file cleared");
    } catch (err) {
        console.error("Failed to clear rag file:", err);
        res.status(500).send("Error clearing conversation history");
    }
});

app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
