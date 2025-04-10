document.addEventListener('DOMContentLoaded', function() {
    const ctx = document.getElementById('chart');
    if (!ctx) return;

    // Get forecast data from the DOM
    const forecastItems = document.querySelectorAll('.forecast-item');
    const temps = [];
    const times = [];

    forecastItems.forEach(item => {
        const time = item.querySelector('.time').textContent;
        const temp = parseFloat(item.querySelector('.temp').textContent);
        if (time && !isNaN(temp)) {
            times.push(time);
            temps.push(temp);
        }
    });

    // Create gradient
    const gradient = ctx.getContext('2d').createLinearGradient(0, 0, 0, 200);
    gradient.addColorStop(0, 'rgba(255, 255, 255, 0.5)');
    gradient.addColorStop(1, 'rgba(255, 255, 255, 0)');

    // Create chart
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: times,
            datasets: [{
                label: 'Temperature',
                data: temps,
                borderColor: 'white',
                borderWidth: 2,
                backgroundColor: gradient,
                fill: true,
                tension: 0.4,
                pointBackgroundColor: 'white',
                pointRadius: 4,
                pointHoverRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        color: 'rgba(255, 255, 255, 0.7)',
                        font: {
                            size: 12
                        }
                    }
                },
                y: {
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    ticks: {
                        color: 'rgba(255, 255, 255, 0.7)',
                        font: {
                            size: 12
                        }
                    }
                }
            },
            interaction: {
                intersect: false,
                mode: 'index'
            },
            animation: {
                duration: 1000,
                easing: 'easeInOutQuart'
            }
        }
    });
});
