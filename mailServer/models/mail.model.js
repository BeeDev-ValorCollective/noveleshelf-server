

class MailModel {
    constructor({ userName, contact, subject, message, contactType }) {
        this.userName = userName
        this.contact = contact
        this.subject = subject
        this.message = message
        this.contactType = contactType
    }
}
module.exports = MailModel