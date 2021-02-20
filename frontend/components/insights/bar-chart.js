import React from 'react';
import { Chart } from 'react-chartjs-2';

class BarChart extends React.Component {
    constructor(props) {
        super(props);
        this.canvasRef = React.createRef();
    }

    componentDidUpdate() {
        this.myChart.data.labels = this.props.data.map(d => d.label);
        this.myChart.data.datasets[0].data = this.props.data.map(d => d.value);
        this.myChart.update();
    }

    componentDidMount() {
        this.myChart = new Chart(this.canvasRef.current, {
            type: 'bar',
            options: {
                maintainAspectRatio: false,
                scales: {
                    xAxes: [
                        {
                            type: 'time',
                            time: {
                                unit: 'day'
                            }
                        }
                    ],
                    yAxes: [
                        {
                            ticks: {
                                min: 0,
                                stepSize: 1
                            }
                        }
                    ]
                },
                legend: {
                    display: false,
                },
            },
            data: {
                labels: this.props.data.map(d => d.label),
                datasets: [{
                    label: this.props.title,
                    data: this.props.data.map(d => d.value.length),
                    backgroundColor: this.props.color
                }]
            }
        });
    }

    render() {
        return (
            <canvas width="20rem" height="40rem" className="p-3" ref={this.canvasRef} />
        );
    }
}

export default BarChart;
