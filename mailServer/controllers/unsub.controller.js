const nodemailer = require('nodemailer')
const UnsubModel = require('../models/unsub.model')

const sendUnsubMail = async (req, res) => {
    const { firstName, lastName, userName, contact, reason } = req.body

    const unsubData = new UnsubModel({ firstName, lastName, userName, contact, reason })

    try {
        if (!process.env.EMAIL_HOST || !process.env.NOVELESHELF_EMAIL_USER || !process.env.NOVELESHELF_EMAIL_PASS) {
            return res.status(500).json({ message: "Server email config missing" })
        }

        const displayName = [unsubData.firstName, unsubData.lastName].filter(Boolean).join(' ') || unsubData.userName || unsubData.contact

        const transporter = nodemailer.createTransport({
            host: process.env.EMAIL_HOST,
            port: process.env.EMAIL_PORT,
            secure: process.env.EMAIL_SSL === 'true',
            auth: {
                user: process.env.NOVELESHELF_EMAIL_USER,
                pass: process.env.NOVELESHELF_EMAIL_PASS,
            },
        })

        const mailOptions = {
            from: process.env.NOVELESHELF_EMAIL_USER,
            to: process.env.NOVELESHELF_EMAIL_USER,
            bcc: process.env.BEEDEV_EMAIL_USER,
            subject: 'Unsubscribe Request — Novel eShelf',
            html: `
                <body style="background-color: #1a1a2e; margin: 0; padding: 0;">
                    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background-color: #1a1a2e; border-collapse: collapse; max-width: 1000px; margin: auto;">
                        <tr>
                            <td>
                                <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background-color: #2d1b69;">
                                    <tr>
                                        <td style="padding: 16px;">
                                            <p style="color: #ffffff; font-size: 1.2rem; margin: 0;">Novel eShelf</p>
                                            <p style="color: #ffffffa0; font-size: 0.75rem; margin: 4px 0 0 0;">Unsubscribe Request</p>
                                        </td>
                                        <td style="padding: 16px; text-align: right;">
                                            <a href="${process.env.SITE_LINK}" style="color: #7b5ea7; font-size: 0.85rem;">Visit Novel eShelf</a>
                                        </td>
                                    </tr>
                                </table>
                                <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background-color: #16213e;">
                                    <tr>
                                        <td style="padding: 24px 16px; text-align: center;">
                                            <p style="color: #ffffffa0; font-size: 0.9rem; margin: 0 0 8px 0;">This is an unmonitored mailbox — please do not reply.</p>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 8px 16px;">
                                            <table width="100%">
                                                ${unsubData.firstName || unsubData.lastName ? `
                                                <tr>
                                                    <th style="text-align: left; padding: 6px 0; color: #cfc7e6;">Name:</th>
                                                    <td style="text-align: left; color: #ffffff;">${[unsubData.firstName, unsubData.lastName].filter(Boolean).join(' ')}</td>
                                                </tr>
                                                ` : ''}
                                                ${unsubData.userName ? `
                                                <tr>
                                                    <th style="text-align: left; padding: 6px 0; color: #cfc7e6;">Username:</th>
                                                    <td style="text-align: left; color: #ffffff;">${unsubData.userName}</td>
                                                </tr>
                                                ` : ''}
                                                <tr>
                                                    <th style="text-align: left; padding: 6px 0; color: #cfc7e6;">Email:</th>
                                                    <td style="text-align: left; color: #ffffff;">${unsubData.contact}</td>
                                                </tr>
                                                <tr>
                                                    <th style="text-align: left; padding: 6px 0; color: #cfc7e6;">Reason:</th>
                                                    <td style="text-align: left; color: #ffffff;">${unsubData.reason}</td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 8px 16px;">
                                            <hr style="width: 95%; margin: 8px auto 16px; border: 1px solid #7b5ea7;">
                                            <p style="font-size: 0.8rem; margin: 8px auto; padding: 0 8px; color: #ffffffa0;">
                                                This email was intended for ${displayName} (${unsubData.contact}). 
                                                If you are not the intended recipient please notify the sender immediately.
                                            </p>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                    </table>
                </body>
            `
        }

        await transporter.sendMail(mailOptions)
        console.log("200 - Unsubscribe email sent")
        return res.status(200).json({ message: "Unsubscribe request received" })
    } catch (error) {
        console.error("500 - Failed to send unsubscribe email", error)
        return res.status(500).json({ message: `Failed to send email: ${error.message}` })
    }
}

module.exports = { sendUnsubMail }