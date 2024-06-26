import React, { lazy, useState, useEffect } from 'react'
import { Select } from 'antd'
import dayjs from 'dayjs'
import ReportUtil from '../helpers/report.utils'
import { CSVLink } from "react-csv";
import { TITLE } from "../messages/main.message";
import { NotificationComponent } from "../components/common/notification.component";
import "./styles/report.page.css"

const PageTitle = lazy(() => import("../components/common/pageTitle.component"))
const Statistic = lazy(() => import("../components/common/statistic.component"))
const DatePicker = lazy(() => import("../components/common/datePicker.component"))
const LineChart = lazy(() => import("../components/common/lineChart.component"))
const Table = lazy(() => import("../components/common/table.component"))
const Button = lazy(() => import("../components/common/button.component"))
const ReportStatus = lazy(() => import("../components/common/reportStatus.component"))

const { getDebtReport } = ReportUtil

const columns = [
  {
    title: "Mã khách hàng",
    dataIndex: "ConsumerId",
    key: "ConsumerId",
  },
  {
    title: "Khách hàng",
    dataIndex: "ConsumerName",
    key: "ConsumerName",
  },
  {
    title: "Nợ đầu",
    dataIndex: "DebtStart",
    key: "DebtStart",
    sorter: (a, b) => a.DebtStart - b.DebtStart,
    render: (text, record, index) => text ? text.toLocaleString() : 0
  },
  {
    title: "Phát sinh thu",
    dataIndex: "PaymentNow",
    key: "PaymentNow",
    sorter: (a, b) => a.PaymentNow - b.PaymentNow,
    render: (text, record, index) => text ? <ReportStatus variant={'add'} data={text.toLocaleString()} /> : 0
  },
  {
    title: "Phát sinh mua",
    dataIndex: "OrderNow",
    key: "OrderNow",
    sorter: (a, b) => a.OrderNow - b.OrderNow,
    render: (text, record, index) => text ? <ReportStatus variant={'subtract'} data={text.toLocaleString()} /> : 0
  },
  {
    title: "Nợ cuối",
    dataIndex: "DebtEnd",
    key: "DebtEnd",
    sorter: (a, b) => a.DebtEnd - b.DebtEnd,
    render: (text, record, index) => text ? text.toLocaleString() : 0
  },
]

const options = [
  {
    label: 'Thống kê',
    value: 'summarize'
  },
  {
    label: 'Chi tiết',
    value: 'detail'
  }
]

const setInitialRangeDate = () => [
  dayjs().set('month', dayjs().get('month') - 1),
  dayjs()
]

const DATE_FORMAT = "YYYY-MM-DD"
const DATE_FORMAT_LOCAL = "DD/MM/YYYY"
const DATE_BINS = 8

const totalReduce = (total, item) => total + item.Debt

const splitDateRange = (startDate, endDate, bins) => {
  if (startDate >= endDate || bins === 0) return

  const interval = (endDate-startDate) / bins

  let dateSplit = []
  dateSplit.push(dayjs(startDate + 0).format(DATE_FORMAT))
  for (let i=1; i <= bins - 1; i++) {
    dateSplit.push(dayjs(startDate + i * interval).format(DATE_FORMAT))
  }
  dateSplit.push(dayjs(endDate + 0).format(DATE_FORMAT))

  return dateSplit
}

const chartOptions = {
  responsive: true,
  plugins: {
    legend: {
      display: false
    },
    title: {
      display: true,
      text: 'Thống kê nợ công qua các ngày',
      font: {
        family: "'Nunito', sans-serif",
        size: 20,
        weight: 'bold',
      },
      color: 'rgb(30, 60, 114)',
      padding: {
        bottom: 30
      }
    },
    datalabels: {
      display: true,
      align: 'top',
      font: {
        family: "'Nunito', sans-serif",
        weight: 'bold',
        size: 14
      },
      formatter: function(value, context) {
        const formatter = Intl.NumberFormat('en-US', { notation:'compact', maximumSignificantDigits: 3})
        return formatter.format(value)
      }
    },
  },
  scales: {
    x: {
      ticks: {
        font: {
          family: "'Nunito', sans-serif",
          weight: 'normal',
        },
      },
      grid: {
        display: true
      }
    },
    y: {
      ticks: {
        font: {
          family: "'Nunito', sans-serif",
          weight: 'normal',
        }
      },
      grid: {
        display: true
      }
    }
  }
};

export default function BookPaymentReportPage () {
  const [mode, setMode] = useState('summarize')
  const [rangeDate, setRangeDate] = useState(setInitialRangeDate)
  const [report, setReport] = useState(null)
  const [statistic, setStatistic] = useState(null)
  const [reportTable, setReportTable] = useState([])
  const [reportChart, setReportChart] = useState(null)

  const onDatePickerChange = (dates, dateStrings) => {
    setRangeDate(dates)
  }

  const getReportData = async () => {
    if (rangeDate === null || rangeDate === undefined) return

    const reportData = await getDebtReport({
      startDate: rangeDate[0].format(DATE_FORMAT),
      endDate: rangeDate[1].format(DATE_FORMAT)
    })

    if(reportData) {
      setReport(reportData)
    }
  }

  useEffect(() => {
    if (rangeDate === null || rangeDate === undefined) return

    getReportData()
  }, [rangeDate])

  useEffect(() => {
    if (report === null || report === undefined) return
    // Summarize data for statistic cards
    setStatistic({
      DebtStart: (report.DebtStart ? Object.values(report.DebtStart) : []).reduce(totalReduce, 0) * -1,
      DebtEnd: (report.DebtEnd ? Object.values(report.DebtEnd) : []).reduce(totalReduce, 0) * -1,
      PaymentNow: (report.PaymentNow ? Object.values(report.PaymentNow) : []).reduce(totalReduce, 0) * -1,
      OrderNow: (report.OrderNow ? Object.values(report.OrderNow) : []).reduce(totalReduce, 0)
    })
    // Summarize data for detailed table
    let consumerObj = {}

    if(report.DebtStart) Object.entries(report.DebtStart).forEach(item => consumerObj[item[0]] = item[1].ConsumerName)
    if(report.DebtEnd) Object.entries(report.DebtEnd).forEach(item => consumerObj[item[0]] = item[1].ConsumerName)
    if(report.PaymentNow) Object.entries(report.PaymentNow).forEach(item => consumerObj[item[0]] = item[1].ConsumerName)
    if(report.OrderNow) Object.entries(report.OrderNow).forEach(item => consumerObj[item[0]] = item[1].ConsumerName) 
      
    
    setReportTable(Object.keys(consumerObj).map(consumerId => ({
      key: consumerId,
      ConsumerId: consumerId,
      ConsumerName: consumerObj[consumerId],
      DebtStart: report?.DebtStart?.[consumerId]?.Debt * -1,
      DebtEnd: report.DebtEnd?.[consumerId]?.Debt * -1,
      PaymentNow: report.PaymentNow?.[consumerId]?.Debt * -1,
      OrderNow: report.OrderNow?.[consumerId]?.Debt * -1
    })))
    // Summarize data for chart
    const dateBins = splitDateRange(dayjs(report.Start, DATE_FORMAT), dayjs(report.End, DATE_FORMAT), DATE_BINS)
    let debtByDate = []

    for (let _ in dateBins) {
      debtByDate.push(statistic?.DebtStart ? statistic?.DebtStart : 0)
    }

    if(report?.PaymentNow) {
      Object.values(report.PaymentNow).forEach(item => {
        for (let idx in debtByDate) {
          if (dayjs(item?.Created).format(DATE_FORMAT) <= dateBins[idx]) debtByDate[idx] -= item.Debt
        }
      })
    }

    if(report?.OrderNow) {
      Object.values(report.OrderNow).forEach(item => {
        for (let idx in debtByDate) {
          if (dayjs(item?.Created).format(DATE_FORMAT) <= dateBins[idx]) debtByDate[idx] -= item.Debt
        }
      })
    }

    setReportChart({
      labels: dateBins.map(date => dayjs(date, DATE_FORMAT).format(DATE_FORMAT_LOCAL)),
      datasets: [
        {
          data: debtByDate,
          borderColor: 'rgba(63, 131, 255, 0.5)',
          backgroundColor: 'rgb(30, 60, 114)',
          borderWidth: 3
        }
      ]
    })

  }, [report])


  return (
    <div className='d-flex flex-column'>
      <PageTitle title="Lập báo cáo nợ công" />
      <div className='report-filter-container mb-3 p-3 d-flex flex-row align-items-center'>
        <DatePicker 
          variant='range' 
          size='large'
          defaultValue={rangeDate}
          onChange={onDatePickerChange}
        />
        <CSVLink
          data={reportTable}
          target="_blank"
          filename={"DebtReport.csv"}
          className="ml-auto mr-3" 
          asyncOnClick={true}
          onClick={() => {
            if(!reportTable || reportTable.length === 0) {
              NotificationComponent("error", TITLE.WARNING, "Dữ liệu đang được chuẩn bị. Vui lòng thử lại sau!")
              return false
            }
            return true
          }}
        >
          <Button buttonCase="download"/>
        </CSVLink>
        <Select 
          options={options}
          defaultValue='summarize'
          size='large'
          onSelect={option=>setMode(option)}
        />
      </div>
      <div className='report-container d-flex flex-row'>
        <div className='statistic-container col-2'>
            <div>
                <Statistic title={"Tổng nợ đầu"} value={statistic?.DebtStart} />
            </div>
            <div className='mt-5'>
                <Statistic title={"Tổng phát sinh thu"} value={statistic?.PaymentNow} variant={"import"}/>
            </div>
            <div className='mt-5'>
                <Statistic title={"Tổng phát sinh mua"} value={statistic?.OrderNow} variant={"export"} />
            </div>
            <div className='mt-5'>
                <Statistic title={"Tổng nợ cuối"} value={statistic?.DebtEnd} />
            </div>
        </div>
        <div className='visualization-container col-10'>
          {
            mode === 'summarize' ?
            (reportChart ? <LineChart data={reportChart} options={chartOptions} /> : null) :
            <Table 
              columns={columns}
              data={reportTable}
              sticky={true}
              disableRowSelection={true}
            />
          }
        </div>
      </div>
    </div>
  );
};
