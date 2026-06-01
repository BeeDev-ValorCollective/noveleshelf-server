const express = require('express')
const { sendContactMail } = require('../controllers/mail.controller')
const { sendUnsubMail } = require('../controllers/unsub.controller')
const captchaMiddleware = require('../middleware/captcha.middleware')
const { createCaptcha } = require('../utils/captchaStore')
const router = express.Router()

router.get('/captcha', (req, res) => {
    const captcha = createCaptcha()
    res.json(captcha)
})


router.post('/sendContactMail', captchaMiddleware, sendContactMail)

router.post('/sendUnsubMail', sendUnsubMail)

module.exports = router
