const express = require('express');
const multer = require('multer');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

const app = express();
const port = 3000;

const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        const uploadPath = 'public/uploads/';
        if (!fs.existsSync(uploadPath)) fs.mkdirSync(uploadPath, { recursive: true });
        cb(null, uploadPath);
    },
    filename: (req, file, cb) => {
        cb(null, Date.now() + '-' + file.originalname);
    }
});
const upload = multer({ storage: storage });

app.use(express.static('public'));

app.post('/analyze', upload.single('video'), (req, res) => {
    if (!req.file) return res.status(400).json({ error: 'No video uploaded' });

    console.log(`\n--- New Analysis Request: ${req.file.path} ---`);

    const pythonProcess = spawn('python', ['ai_service.py', req.file.path]);

    let dataBuffer = '';

    pythonProcess.stdout.on('data', (data) => {
        dataBuffer += data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`[Python Log]: ${data}`);
    });

    pythonProcess.on('error', (err) => {
        console.error("FAILED TO START PYTHON:", err);
        res.status(500).json({ error: "Failed to start Python. Is Python installed and in your PATH?" });
    });

    pythonProcess.on('close', (code) => {
        console.log(`Python finished with code ${code}`);

        try {
            const startIndex = dataBuffer.indexOf('---JSON_START---');
            const endIndex = dataBuffer.indexOf('---JSON_END---');

            if (startIndex !== -1 && endIndex !== -1) {
                const jsonString = dataBuffer.substring(startIndex + 16, endIndex);
                const result = JSON.parse(jsonString);
                res.json(result);
            } else {
                throw new Error("Could not find JSON markers in Python output.");
            }
        } catch (e) {
            console.error("Parsing Error:", e);
            console.error("Raw Output was:", dataBuffer); 
            res.status(500).json({ 
                error: 'Failed to process video', 
                details: 'Python output was not valid JSON. Check server console for logs.' 
            });
        }
    });
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});