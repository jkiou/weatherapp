document.addEventListener('DOMContentLoaded', () => {
    const chartElement = document.getElementById('chart');
    if (!chartElement) {
        console.error('No chart element found');
        return;
    }

    const ctx = chartElement.getContext('2d');
    const gradient = ctx.createLinearGradient(0, 0, 0, 100);
    gradient.addColorStop(0, 'rgba(255, 0, 0, 1)');
    gradient.addColorStop(1, 'rgba(136, 255, 0, 1)');

    // Hardcoded data for testing
    const times = ["15:18", "16:18", "17:18", "18:18", "19:18"];
    const temps = [33.1, 25.1, 20.1, 16.6, 14.4];

    try {
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: times,
                datasets: [
                    {
                        label: 'Celsius Degrees',
                        data: temps,
                        borderColor: gradient,
                        borderWidth: 2,
                        tension: 0.4,
                        pointRadius: 2,
                    },
                ],
            },
            options: {
                plugins: {
                    legend: {
                        display: false,
                    },
                },
                scales: {
                    x: {
                        display: false,
                        grid: {
                            drawOnChartArea: false,
                        },
                    },
                    y: {
                        display: false,
                        grid: {
                            drawOnChartArea: false,
                        },
                    },
                },
                animation: {
                    duration: 750,
                },
            },
        });
        console.log('Chart created successfully with hardcoded data');
    } catch (error) {
        console.error('Error creating chart with hardcoded data:', error);
    }
});