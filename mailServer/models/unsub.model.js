class UnsubModel {
    constructor({ firstName, lastName, userName, contact, reason }) {
        this.firstName = firstName || null
        this.lastName = lastName || null
        this.userName = userName || null
        this.contact = contact
        this.reason = reason
    }
}

module.exports = UnsubModel