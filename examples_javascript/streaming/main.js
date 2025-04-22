// @ts-check

const bodyParser = require("body-parser");
const express = require("express");

const apiKey = ""; // please set your API key

const app = express();

app.use(bodyParser.json());

app.use(express.static("public"));

/**
 * This endpoint assumes following request.
 * POST /api/tts-stream
 * Content-Type: text/plain
 * 
 * TTS text message in body
 */
app.post("/api/tts-stream", async (req, res) => {
  // 1. validation
  // 2. call koemotion API to get stream
  // 3. pipe stream to response
  const text = req.body.text;
  if (typeof text !== "string") {
    res.status(400).json({ error: "invalid request" });
    return;
  }

  const response = await fetch("https://api.rinna.co.jp/koemotion/infer", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Ocp-Apim-Subscription-Key": apiKey,
    },
    body: JSON.stringify({
      // please modify request body as needed
      text: text,
      speaker_x: 0.0,
      speaker_y: 0.0,
      output_format: "wav",
      streaming: true,
      trim_leading_silence: true,
    }),
  });

  if (!response.ok || response.body == null) {
    res.status(response.status).json({ error: "API request failed" });
    console.error(response.statusText);
    console.error(await response.text());
    return;
  } else {
    // if you use node-fetch, you can simply use `pipe` method.
    // await response.body.pipe(res)

    // if you use fetch in v17.5+ nodejs feature,
    // needs to do following instead of the `pipe`.
    const reader = response.body.getReader();
    while (true) {
      const result = await reader.read();
      if (result.done) {
        res.end();
        return
      }

      res.write(result.value)
    }
  }
});

app.listen(3000);
