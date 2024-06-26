import ReportAPI from "../api/report.api"

export default class ReportUtil {
    static async getStorageReport(dateData) {
        const response = await ReportAPI.getStorageReport(dateData)

        if (response === null || response === undefined) return

        const reportData = response.data
        return reportData
    }

    static async getDebtReport(dateData) {
        const response = await ReportAPI.getDebtReport(dateData)

        if (response === null || response === undefined) return

        const reportData = response.data
        return reportData
    }
}