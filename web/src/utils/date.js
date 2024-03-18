function getMonthFirstAndLastDay(date) {
    const year = date.getFullYear();
    const month = date.getMonth();

    // 获取第一天
    const firstDay = new Date(year, month, 1);

    // 获取下个月的第一天
    const nextMonthFirstDay = new Date(year, month + 1, 1);

    // 获取最后一天
    const lastDay = new Date(nextMonthFirstDay - 1);

    // 格式化日期字符串
    const formatDate = (date) => {
        const year = date.getFullYear();
        const month = date.getMonth() + 1;
        const day = date.getDate();
        return `${year}-${month.toString().padStart(2, '0')}-${day.toString().padStart(2, '0')}`;
    };

    return [formatDate(firstDay), formatDate(lastDay)];
}

function formatDate(date) {
    const year = date.getFullYear();
    const month = date.getMonth() + 1;
    const day = date.getDate();
    return `${year}-${month.toString().padStart(2, '0')}-${day.toString().padStart(2, '0')}`;
}

function formatTime(date) {
    const year = date.getFullYear();
    const month = date.getMonth() + 1;
    const day = date.getDate();
    const hour = date.getHours();
    const minute = date.getMinutes();
    const second = date.getSeconds();
    return `${year}-${month.toString().padStart(2, '0')}-${day.toString().padStart(2, '0')} ${hour.toString().padStart(2, '0')}:${minute.toString().padStart(2, '0')}:${second.toString().padStart(2, '0')}`;
}

export {getMonthFirstAndLastDay, formatDate, formatTime}
