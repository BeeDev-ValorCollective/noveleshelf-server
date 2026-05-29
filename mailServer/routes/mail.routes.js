const express = require('express')
const { sendContactMail } = require('../controllers/mail.controller')
const captchaMiddleware = require('../middleware/captcha.middleware')
const { createCaptcha } = require('../utils/captchaStore')
const router = express.Router()

router.get('/captcha', (req, res) => {
    const captcha = createCaptcha()
    res.json(captcha)
})


router.post('/sendContactMail', captchaMiddleware, sendContactMail)


module.exports = router