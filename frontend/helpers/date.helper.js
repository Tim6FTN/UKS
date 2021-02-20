export function convertUnixTimestampToDate(timestamp) {
    const dateStr = timestamp.split("T")[0];
    return dateStr;
}

Date.prototype.addDays = function (days) {
    let date = new Date(this.valueOf());
    date.setDate(date.getDate() + days);
    return date;
}

export function getDates(startDate, stopDate) {
    let dateArray = [];
    let currentDate = startDate;
    while (currentDate <= stopDate) {
        dateArray.push({time: new Date(currentDate), value: []});
        currentDate = currentDate.addDays(1);
    }
    return dateArray;
}

export function getDatesBarChart(startDate, stopDate) {
    let dateArray = [];
    let currentDate = startDate;
    while (currentDate <= stopDate) {
        dateArray.push({label: (new Date(currentDate)).toISOString().split('T')[0], value: []});
        currentDate = currentDate.addDays(1);
    }
    return dateArray;
}