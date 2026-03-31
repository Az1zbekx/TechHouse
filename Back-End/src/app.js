import express from "express";
import cors from "cors";
import authRouters from "./routes/authRoutes.js";

const app = express();

app.use(cors());
app.use(express.json());

app.use("/api/auth", authRouters)

app.get("/", (req, res) => {
    res.json({message: "Api is running"});
});

export default app;

