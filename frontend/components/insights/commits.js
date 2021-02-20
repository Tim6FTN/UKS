import React from 'react';
import LineChart from "./line-chart";
import BarChart from "./bar-chart";
import {convertUnixTimestampToDate, getDates, getDatesBarChart} from "../../helpers/date.helper";

const Commits = ({commits}) => {

    const [stats, setStats] = React.useState(null);
    const [weekStats, setWeekStats] = React.useState(null);

    React.useEffect(() => {
        const today = new Date();
        const monthAgo = new Date(today);
        monthAgo.setDate(monthAgo.getDate() - 30);

        const lastMonthDays = getDatesBarChart(monthAgo, new Date());
        lastMonthDays.forEach(el => {
            const foundCommit = commits.find(com => convertUnixTimestampToDate(com.timestamp) === el.label);
            if (foundCommit) {
                el.value.push(foundCommit);
            }
        });
        setStats(lastMonthDays);

        const weekAgo = new Date(today);
        weekAgo.setDate(weekAgo.getDate() - 7);

        const lastWeekDays = getDates(weekAgo, new Date());
        lastWeekDays.forEach(el => {
            const convertedTime = el.time.toISOString().split('T')[0];
            const foundCommit = commits.find(com => convertUnixTimestampToDate(com.timestamp) === convertedTime);
            if (foundCommit) {
                el.value.push(foundCommit);
            }
        });
        setWeekStats(lastWeekDays);

    }, [commits])

    return (
        <>
            <div className="card mb-3" style={{height: '15em'}}>
                {   stats &&
                    <BarChart
                        data={stats}
                        title="Commits"
                        color="#fb8533"
                    />
                }
            </div>
            <div className="card" style={{height: '20em'}}>
                {
                    weekStats &&
                    <LineChart
                        data={weekStats}
                        title="Commits"
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
