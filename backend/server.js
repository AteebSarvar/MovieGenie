const express = require("express");
const bodyParser = require("body-parser");
const cors = require("cors");
const { spawn } = require("child_process");

const app = express();
const PORT = 5000;

app.use(cors());
app.use(bodyParser.json());

app.post("/recommend", (req, res) => {
  const movie = req.body.movie;

  if (!movie) {
    return res.status(400).json({ error: "No movie provided" });
  }

  const python = spawn("python", ["recommender.py", movie]);

  let dataToSend = "";
  python.stdout.on("data", (data) => {
    dataToSend += data.toString();
  });

  python.stderr.on("data", (data) => {
    console.error(`stderr: ${data}`);
  });

  python.on("close", (code) => {
    if (code !== 0) {
      return res.status(500).json({ error: "Python script error" });
    }

    try {
      const recommendations = JSON.parse(dataToSend);
      if (recommendations.length === 0) {
        return res.status(404).json({ error: "Movie not found" });
      }

      res.json({ recommendations });
    } catch (err) {
      res.status(500).json({ error: "Failed to parse recommendations" });
    }
  });
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
