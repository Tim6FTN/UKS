import React from 'react';
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faUserNinja} from "@fortawesome/free-solid-svg-icons";
import LineChart from "./line-chart";
import {convertUnixTimestampToDate, getDates} from "../../helpers/date.helper";

const Contributors = ({commits, contributors}) => {
    const [stats, setStats] = React.useState(null);

    React.useEffect(() => {
        const today = new Date();
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
        setStats(lastWeekDays);
    }, [commits])

    return (
        <>
            <h6 className="text-muted">Contributions to main, including all commits (past 7 days)</h6>
            <div className="card border-light mb-3" style={{backgroundColor: 'whitesmoke', height: '20em'}}>
                {
                    stats && <LineChart
                        data={stats}
                        // title={data.data.title}
                        color="#99cfa1"
                        fill='origin'
                        pointRadius={0}
                        lineTension={0.4}
                        isUser={false}
                        username={""}
                    />
                }
            </div>
            <div className="row">
                {
                    contributors.map((contributor) => (
                        <div className="col-6 mb-2" key={contributor.id}>
                            <div className="card border-info">
                                <div className="card-header">
                                    <span>
                                        <FontAwesomeIcon icon={faUserNinja}/>
                                        <b className="m-2">{contributor.username}</b>
                                    </span>
                                    <div>
                                        <span className="mr-1 small">Commits 13</span>
                                        <span className="mr-1 small" style={{color: 'green'}}>7000++</span>
                                        <span className="mr-1 small" style={{color: 'red'}}>7000--</span>
                                    </div>
                                </div>
                                <div className="card-body" style={{height: '20em'}}>
                                    {
                                        stats && <LineChart
                                            data={stats}
                                            // title={data.data.title}
                                            color="#fb8533"
                                            fill='origin'
                                            pointRadius={0}
                                            lineTension={0.4}
                                            isUser={true}
                                            username={contributor.username}
                                        />
                                    }
                                </div>
                            </div>
                        </div>
                    ))
                }
            </div>
        </>

    );
};

export default Contributors;