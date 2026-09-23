const ws = new WebSocket("ws://127.0.0.1:8000/ws/traffic");
const statusEl = document.getElementById("conn-status");
const tableBody = document.getElementById("log-table-body");

// Setup Chart.js line graph
const ctx = document.getElementById('trafficChart').getContext('2d');
const trafficChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Packet Size (Bytes)',
            borderColor: '#38bdf8',
            backgroundColor: 'rgba(56, 189, 248, 0.1)',
            data: [],
            fill: true,
            tension: 0.3
        }]
    },
    options: {
        responsive: true,
        scales: {
            x: { ticks: { color: '#94a3b8' } },
            y: { ticks: { color: '#94a3b8' } }
        }
    }
});

ws.onopen = () => {
    statusEl.innerText = "Connected (Live Sniffing)";
    statusEl.style.color = "#4ade80";
};

ws.onclose = () => {
    statusEl.innerText = "Disconnected";
    statusEl.style.color = "#f87171";
};

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);

    // 1. Update Live Chart
    if (trafficChart.data.labels.length > 20) {
        trafficChart.data.labels.shift();
        trafficChart.data.datasets[0].data.shift();
    }
    trafficChart.data.labels.push(data.timestamp);
    trafficChart.data.datasets[0].data.push(data.length);
    trafficChart.update();

    // 2. Prepend Row to Log Table
    const row = document.createElement("tr");
    const statusClass = data.is_anomaly ? "badge-suspicious" : "badge-normal";

    row.innerHTML = `
        <td>${data.timestamp}</td>
        <td>${data.protocol}</td>
        <td>${data.src_ip}</td>
        <td>${data.dst_ip}</td>
        <td>${data.length} B</td>
        <td><span class="${statusClass}">${data.status}</span></td>
    `;

    tableBody.insertBefore(row, tableBody.firstChild);
};