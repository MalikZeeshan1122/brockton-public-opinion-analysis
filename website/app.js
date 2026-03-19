// Function to fetch data and initialize charts
async function initDashboard() {
    try {
        const response = await fetch('dataset.json');
        const data = await response.json();
        
        processData(data);
    } catch (error) {
        console.error('Error loading dataset:', error);
        document.getElementById('total-count').innerText = "Error loading data";
    }
}

function processData(data) {
    // 1. Calculate Stats
    document.getElementById('total-count').innerText = data.length;
    
    const topicCounts = {};
    const sentimentCounts = { Positive: 0, Neutral: 0, Negative: 0 };
    const keywordCounts = {};
    const dateCounts = {};
    const sourceCounts = {};
    
    data.forEach(item => {
        // Topics
        topicCounts[item.topic] = (topicCounts[item.topic] || 0) + 1;
        
        // Sentiments
        sentimentCounts[item.sentiment] = (sentimentCounts[item.sentiment] || 0) + 1;
        
        // Keywords
        item.keywords.forEach(kw => {
            keywordCounts[kw] = (keywordCounts[kw] || 0) + 1;
        });
        
        // Dates (Group by Month for clearer trends)
        const dateObj = new Date(item.date);
        const monthYear = dateObj.toLocaleString('en-US', { month: 'short', year: 'numeric' });
        dateCounts[monthYear] = (dateCounts[monthYear] || 0) + 1;
        
        // Sources
        sourceCounts[item.source] = (sourceCounts[item.source] || 0) + 1;
    });

    // Find top topic
    const topTopic = Object.keys(topicCounts).reduce((a, b) => topicCounts[a] > topicCounts[b] ? a : b);
    document.getElementById('top-topic').innerText = topTopic;
    
    // Find overall sentiment
    const topSentiment = Object.keys(sentimentCounts).reduce((a, b) => sentimentCounts[a] > sentimentCounts[b] ? a : b);
    document.getElementById('overall-sentiment').innerText = topSentiment;
    
    // 2. Render Charts
    renderBarChart(topicCounts);
    renderWordCloud(keywordCounts);
    renderLineChart(dateCounts);
    renderPieChart(sentimentCounts);
    renderSourceChart(sourceCounts);
}

// Chart Configurations
const colors = {
    blue: '#3b82f6',
    green: '#10b981',
    red: '#ef4444',
    yellow: '#f59e0b',
    purple: '#8b5cf6',
    pink: '#ec4899',
    gray: '#64748b'
};

const sentimentColors = [colors.green, colors.gray, colors.red];

function renderBarChart(topicCounts) {
    const ctx = document.getElementById('barChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: Object.keys(topicCounts),
            datasets: [{
                label: 'Mentions',
                data: Object.values(topicCounts),
                backgroundColor: colors.blue,
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false } },
            scales: { y: { beginAtZero: true } }
        }
    });
}

function renderWordCloud(keywordCounts) {
    const ctx = document.getElementById('wordCloudChart').getContext('2d');
    
    // Convert to Chart.js WordCloud array format
    const words = Object.keys(keywordCounts).map(key => ({
        key: key,
        value: keywordCounts[key] * 10 // scale
    }));
    
    if (typeof Chart.registry.getChart('wordCloud') === 'undefined' && typeof Chart.controllers.wordCloud === 'undefined') {
        renderFallbackKeywordChart(ctx, words);
        return;
    }

    try {
        new Chart(ctx, {
            type: 'wordCloud',
            data: {
                labels: words.map(w => w.key),
                datasets: [{
                    label: 'Keywords',
                    data: words.map(w => w.value),
                    color: [colors.blue, colors.green, colors.purple, colors.pink, colors.yellow]
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { display: false } }
            }
        });
    } catch(e) {
        console.error("Word cloud error, falling back", e);
        renderFallbackKeywordChart(ctx, words);
    }
}

function renderFallbackKeywordChart(ctx, words) {
    words.sort((a,b) => b.value - a.value);
    const top10 = words.slice(0, 10);
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: top10.map(w => w.key),
            datasets: [{
                label: 'Frequency',
                data: top10.map(w => w.value),
                backgroundColor: colors.purple,
                borderRadius: 4
            }]
        },
        options: { responsive: true, indexAxis: 'y' }
    });
}

function renderLineChart(dateCounts) {
    const ctx = document.getElementById('lineChart').getContext('2d');
    
    const sortedDates = Object.keys(dateCounts).sort((a, b) => new Date(a) - new Date(b));
    const data = sortedDates.map(date => dateCounts[date]);

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: sortedDates,
            datasets: [{
                label: 'Volume',
                data: data,
                borderColor: colors.blue,
                backgroundColor: 'rgba(59, 130, 246, 0.1)',
                fill: true,
                tension: 0.3
            }]
        },
        options: {
            responsive: true,
            scales: { y: { beginAtZero: true } }
        }
    });
}

function renderPieChart(sentimentCounts) {
    const ctx = document.getElementById('pieChart').getContext('2d');
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Positive', 'Neutral', 'Negative'],
            datasets: [{
                data: [sentimentCounts.Positive, sentimentCounts.Neutral, sentimentCounts.Negative],
                backgroundColor: sentimentColors,
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            cutout: '60%'
        }
    });
}

function renderSourceChart(sourceCounts) {
    const ctx = document.getElementById('sourceChart').getContext('2d');
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: Object.keys(sourceCounts),
            datasets: [{
                data: Object.values(sourceCounts),
                backgroundColor: [colors.blue, '#1877f2', '#E1306C'],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true
        }
    });
}

document.addEventListener('DOMContentLoaded', initDashboard);
