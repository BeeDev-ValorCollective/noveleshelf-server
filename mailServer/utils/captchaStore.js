
const { randomUUID } = require('crypto')

const captchaStore = new Map();
const CAPTCHA_TTL = 10 * 60 * 1000; // 10 minutes

function createCaptcha() {
  const a = Math.floor(Math.random() * 9) + 1 // 1–9
  const b = Math.floor(Math.random() * 9) + 1 // 1–9
  const answer = a + b

  const id = randomUUID()
  const expiresAt = Date.now() + CAPTCHA_TTL

  captchaStore.set(id, { answer, expiresAt })

  return {
    id,
    question: `What is ${a} + ${b}?`,
  }
}

function verifyCaptcha(id, userAnswer) {
  const entry = captchaStore.get(id)
  if (!entry) return false

  if (entry.expiresAt < Date.now()) {
    captchaStore.delete(id)
    return false
  }

  captchaStore.delete(id)

  const parsed = parseInt(userAnswer, 10)
  if (Number.isNaN(parsed)) return false

  return parsed === entry.answer
}

module.exports = { createCaptcha, verifyCaptcha }