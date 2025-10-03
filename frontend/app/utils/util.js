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

export function truncateString(string, startLength = 30, endLength = 20) {
    if (string.length <= startLength + endLength + 3) {
        return string; // Retorna o nome original se for curto o suficiente
    }

    const extensionIndex = string.lastIndexOf(".");
    const hasExtension = extensionIndex > 0;

    let baseName = string;
    let extension = "";

    if (hasExtension) {
        baseName = string.substring(0, extensionIndex);
        extension = string.substring(extensionIndex); // Inclui o ponto
    }

    const truncated = baseName.substring(0, startLength) + "..." + baseName.slice(-endLength);
    return truncated + extension;
}

export function replaceStringNumberBySubscript(string) {
    return string.replace(/(\d+)/g, '<sub>$1</sub>');
}

export function decodeHtml(html) {
    var txt = document.createElement("textarea");
    txt.innerHTML = html;
    return txt.value;
}

export default {
    roundValue,
    formatTimestamp,
    truncateString,
    replaceStringNumberBySubscript,
    decodeHtml
}