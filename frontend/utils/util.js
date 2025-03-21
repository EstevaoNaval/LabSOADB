export function roundValue(value) {
    return Math.floor(value)
}

export function formatTimestamp(timestamp) {
    const date = new Date(timestamp);

    // Extract date parts
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');

    // Format time with AM/PM
    const time = date.toLocaleString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        hour12: true
    });

    return `${year}-${month}-${day}, ${time}`;
}

export default {
    roundValue,
    formatTimestamp
}