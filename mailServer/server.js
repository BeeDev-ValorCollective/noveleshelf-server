const express = require("express")
const cors = require("cors")
const cookieParser = require("cookie-parser")
const app = express()
require("dotenv").config()

app.use(
    cookieParser(),
    express.json(),
    express.urlencoded({ extended: true }),
    cors({
        credentials: true,
        origin: process.env.NODE_ENV === 'development'
            ? process.env.FRONTEND_DEV_ORIGIN
            : process.env.FRONTEND_PROD_ORIGIN
    })
)

const mailRoutes = require("./routes/mail.routes")
app.use('/api', mailRoutes)

app.listen(process.env.SERVER_PORT, () => {
    console.log(`Server is Running on port: ${process.env.SERVER_PORT}`)
})