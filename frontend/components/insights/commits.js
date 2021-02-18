import React from 'react';
import LineChart from "./line-chart";
import BarChart from "./bar-chart";

const Commits = ({barData, lineData}) => {

    React.useEffect(() => {
        console.log('Line data', lineData);
    }, [lineData])

    return (
        <>
            <div className="card mb-3" style={{height: '15em'}}>
                {
                    barData &&
                    <BarChart
                        data={barData.data}
                        title={barData.title}
                        color="#fb8533"
                    />
                }
            </div>
            <div className="card" style={{height: '20em'}}>
                {
                    lineData &&
                    <LineChart
                        data={lineData.data}
                        title={lineData.title}
                        color="green"
                        fill="none"
                        pointRadius={2}
                        lineTension={0}
                    />
                }
            </div>
        </>
    );
};

export default Commits;
