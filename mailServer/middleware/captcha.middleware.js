const { verifyCaptcha } = require('../utils/captchaStore')

function captchaMiddleware(req, res, next) {
  const {
    captchaId,
    captchaAnswer,
    website,
  } = req.body

  if (website) {
    return res.status(400).json({
      success: false,
      message: 'Spam detected.',
    })
  }

  if (!verifyCaptcha(captchaId, captchaAnswer)) {
    return res.status(400).json({
      success: false,
      message: 'Captcha failed. Please try again.',
    })
  }

  next()
}

module.exports = captchaMiddleware