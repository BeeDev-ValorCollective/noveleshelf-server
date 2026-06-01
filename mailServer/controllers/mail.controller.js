const nodemailer = require('nodemailer')
const MailModel = require('../models/mail.model')

const Site_Link = process.env.SITE_LINK
const Unsub_Link = process.env.UNSUB_LINK

const getRouting = (contactType) => {
    if (contactType === 'account') {
        return {
            to: process.env.NOVELESHELF_EMAIL_USER,
            from: `Novel eShelf <${process.env.NOVELESHELF_EMAIL_USER}>`,
            emailUser: process.env.NOVELESHELF_EMAIL_USER,
            emailPass: process.env.NOVELESHELF_EMAIL_PASS,
            cc: null,
            subject: 'Account Issue — Novel eShelf',
        }
    }
    if (contactType === 'book_reading') {
        return {
            to: process.env.NOVELESHELF_EMAIL_USER,
            from: `Novel eShelf <${process.env.NOVELESHELF_EMAIL_USER}>`,
            emailUser: process.env.NOVELESHELF_EMAIL_USER,
            emailPass: process.env.NOVELESHELF_EMAIL_PASS,
            cc: null,
            subject: 'Book & Reading Issue — Novel eShelf',
        }
    }
    if (contactType === 'author_support') {
        return {
            to: process.env.NOVELESHELF_EMAIL_USER,
            from: `Novel eShelf <${process.env.NOVELESHELF_EMAIL_USER}>`,
            emailUser: process.env.NOVELESHELF_EMAIL_USER,
            emailPass: process.env.NOVELESHELF_EMAIL_PASS,
            cc: null,
            subject: 'Author Support — Novel eShelf',
        }
    }
    if (contactType === 'other') {
        return {
            to: process.env.NOVELESHELF_EMAIL_USER,
            from: `Novel eShelf <${process.env.NOVELESHELF_EMAIL_USER}>`,
            emailUser: process.env.NOVELESHELF_EMAIL_USER,
            emailPass: process.env.NOVELESHELF_EMAIL_PASS,
            cc: process.env.BEEDEV_EMAIL_USER,
            subject: 'General Inquiry — Novel eShelf',
        }
    }
    if (contactType === 'technical') {
        return {
            to: process.env.BEEDEV_EMAIL_USER,
            from: `BeeDev Services <${process.env.BEEDEV_EMAIL_USER}>`,
            emailUser: process.env.BEEDEV_EMAIL_USER,
            emailPass: process.env.BEEDEV_EMAIL_PASS,
            cc: null,
            subject: 'Technical Issue — Novel eShelf',
        }
    }
    if (contactType === 'partnership' || contactType === 'business') {
        return {
            to: process.env.BEEDEV_EMAIL_USER,
            from: `BeeDev Services <${process.env.BEEDEV_EMAIL_USER}>`,
            emailUser: process.env.BEEDEV_EMAIL_USER,
            emailPass: process.env.BEEDEV_EMAIL_PASS,
            cc: null,
            subject: 'Business Inquiry — Novel eShelf',
        }
    }
    // fallback
    return {
        to: process.env.BEEDEV_EMAIL_USER,
        from: `BeeDev Services <${process.env.BEEDEV_EMAIL_USER}>`,
        emailUser: process.env.BEEDEV_EMAIL_USER,
        emailPass: process.env.BEEDEV_EMAIL_PASS,
        cc: null,
        subject: 'General Inquiry — Novel eShelf',
    }
}

const sendContactMail = async (req, res) => {
    const { userName, contact, subject, message, contactType } = req.body

    const mailData = new MailModel({ userName, contact, subject, message, contactType })

    try {
        const routing = getRouting(mailData.contactType)

        if (!process.env.EMAIL_HOST || !routing.emailUser || !routing.emailPass) {
            return res.status(500).json({ message: "Server email config missing" })
        }

        const transporter = nodemailer.createTransport({
            host: process.env.EMAIL_HOST,
            port: process.env.EMAIL_PORT,
            secure: process.env.EMAIL_SSL === 'true',
            auth: {
                user: routing.emailUser,
                pass: routing.emailPass,
            },
        })

        const bccList = []
        if (mailData.contact && mailData.contact.includes("@")) {
            bccList.push(mailData.contact)
        }

        const mailOptions = {
            from: routing.from,
            to: routing.to,
            cc: routing.cc || undefined,
            bcc: bccList.length ? bccList : undefined,
            subject: routing.subject,
            html: `
                <body style="background-color: #0d0f1a; margin: 0; padding: 0; color: #ffffff;">
                    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="border-collapse: collapse; max-width: 1000px; margin: auto;">
                        <tr style="border-bottom: 1px solid #ffffff20; padding: 5px;">
                            <td>
                                <a href="${Site_Link}">
                                    <h2 style="color: #7b5ea7;">Novel eShelf</h2>
                                </a>
                            </td>
                            <td style="text-align: right;">
                                <a href="${Site_Link}" style="padding: 12px 24px; border-radius: 20px; background-color: #7b5ea7; color: white; font-weight: 700; text-decoration: none;">
                                    Visit us
                                </a>
                            </td>
                        </tr>
                        <tr>
                            <td colspan="2" style="padding: 20px 0;">
                                <table width="100%">
                                    <tr>
                                        <th style="text-align: left; padding: 6px 0; color: #cfc7e6;">Contact Type:</th>
                                        <td style="text-align: left; color: #ffffff;">${mailData.contactType?.replace(/_/g, ' ')}</td>
                                    </tr>
                                    <tr>
                                        <th style="text-align: left; padding: 6px 0; color: #cfc7e6;">From:</th>
                                        <td style="text-align: left; color: #ffffff;">${mailData.userName} at ${mailData.contact}</td>
                                    </tr>
                                    <tr>
                                        <th style="text-align: left; padding: 6px 0; color: #cfc7e6;">Subject:</th>
                                        <td style="text-align: left; color: #ffffff;">${mailData.subject}</td>
                                    </tr>
                                    <tr>
                                        <th style="text-align: left; padding: 6px 0; color: #cfc7e6;">Message:</th>
                                        <td style="text-align: left; color: #ffffff;">${mailData.message}</td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                        <tr>
                            <td colspan="2" style="padding-top: 20px; border-top: 1px solid #ffffff20;">
                                <p style="color: #ffffffa0; font-size: 0.85em;">
                                    To ensure our messages find their way into your inbox, please add 
                                    <a href="#" style="color: #7b5ea7;">${routing.from}</a> to your mailing list.
                                </p>
                            </td>
                        </tr>
                        <tr>
                            <td colspan="2">
                                <p style="color: #ffffffa0; font-size: 0.85em;">
                                    This email was intended for ${mailData.userName} (${mailData.contact}). 
                                    If you are not the intended recipient please notify the sender immediately.
                                </p>
                            </td>
                        </tr>
                        <tr>
                            <td colspan="2">
                                <p style="color: #ffffffa0; font-size: 0.85em;">
                                    If you wish to unsubscribe from future emails please visit 
                                    <a href="${Unsub_Link}" style="color: #7b5ea7;">${Unsub_Link}</a>
                                </p>
                            </td>
                        </tr>
                    </table>
                </body>
            `
        }

        await transporter.sendMail(mailOptions)
        console.log(mailData)
        return res.status(200).json({ message: "Sent", info: mailData })
    } catch (error) {
        console.error("Failed", error)
        return res.status(500).json({ message: "Failed" })
    }
}

module.exports = { sendContactMail }