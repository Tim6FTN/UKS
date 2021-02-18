import React from 'react';
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {faUserNinja} from "@fortawesome/free-solid-svg-icons";
import LineChart from "./line-chart";

const Contributors = (data) => {

    const [users, setUsers] = React.useState([1, 2, 3, 4, 5]);

    React.useEffect(() => {
        console.log(data);
    }, [data])

    return (
        <>
            <h6 className="text-muted">Contributions to dev, including all commits</h6>
            <div className="card border-light mb-3" style={{backgroundColor: 'whitesmoke', height: '20em'}}>
                    <LineChart
                        data={data.data.data}
                        title={data.data.title}
                        color="#99cfa1"
                        fill='origin'
                        pointRadius={0}
                        lineTension={0.4}
                    />

            </div>
            <div className="row">
                {
                    users.map(() => (
                        <div className="col-6 mb-2">
                            <div className="card border-info">
                                <div className="card-header">
                                    <span>
                                        <FontAwesomeIcon icon={faUserNinja}/>
                                        <b className="m-2">Username</b>
                                    </span>
                                    <div>
                                        <span className="mr-1 small">Commits 13</span>
                                        <span className="mr-1 small" style={{color: 'green'}}>7000++</span>
                                        <span className="mr-1 small" style={{color: 'red'}}>7000--</span>
                                    </div>
                                </div>
                                {data &&
                                <div className="card-body" style={{height: '20em'}}>
                                    <LineChart
                                        data={data.data.data}
                                        title={data.data.title}
                                        color="#fb8533"
                                        fill='origin'
                                        pointRadius={0}
                                        lineTension={0.4}
                                    />
                                </div>
                                }
                            </div>
                        </div>
                    ))
                }
            </div>
        </>

    );
};

export default Contributors;