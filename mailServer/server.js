const express = require("express")
const cors = require("cors")
const cookieParser = require("cookie-parser")
const app = express()
require("dotenv").config()

app.use(cors({
    credentials: true,
    origin: [
    process.env.FRONTEND_DEV_ORIGIN,
    process.env.FRONTEND_PROD_ORIGIN,
    process.env.FRONTEND_PREVIEW_ORIGIN
].filter(Boolean)
}));

app.use(cookieParser());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

const mailRoutes = require("./routes/mail.routes")
app.use('/api', mailRoutes)

app.listen(process.env.SERVER_PORT, () => {
    console.log(`Server is Running on port: ${process.env.SERVER_PORT}`)
})