import React from 'react';

class LineChart extends React.Component {
    constructor(props) {
        super(props);
        this.canvasRef = React.createRef();
    }

    componentDidUpdate() {
        this.myChart.data.labels = this.props.data.map(d => d.time);
        this.myChart.data.datasets[0].data = this.props.data.map(d => d.value);
        this.myChart.update();
    }

    componentDidMount() {
        this.myChart = new Chart(this.canvasRef.current, {
            type: 'line',
            options: {
                maintainAspectRatio: false,
                scales: {
                    xAxes: [
                        {
                            type: 'time',
                            time: {
                                unit: 'week'
                            }
                        }
                    ],
                    yAxes: [
                        {
                            ticks: {
                                sampleSize: 5,
                                stepSize: 40,
                            }
                        }
                    ]
                },
                filler: {
                    propagate: true
                },
                legend: {
                    display: false,
                },
            },
            data: {
                labels: this.props.data.map(d => d.time),
                datasets: [{
                    label: this.props.title,
                    data: this.props.data.map(d => d.value),
                    fill: this.props.fill,
                    backgroundColor: this.props.color,
                    pointRadius: this.props.pointRadius,
                    borderColor: this.props.color,
                    borderWidth: 1,
                    lineTension: this.props.lineTension
                }]
            }
        });
    }

    render() {
        return <canvas width="20rem" height="40rem" className="p-3" ref={this.canvasRef} />;
    }
}

export default LineChart;
