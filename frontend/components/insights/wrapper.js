import React from 'react';
import Pulse from "./pulse";
import Commits from "./commits";
import Contributors from "./contributors";

function getRandomArray(numItems) {
    // Create random array of objects
    let names = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    let data = [];
    for(let i = 0; i < numItems; i++) {
        data.push({
            label: names[i],
            value: Math.round(20 + 80 * Math.random())
        });
    }
    return data;
}

function getRandomDateArray(numItems) {
    // Create random array of objects (with date)
    let data = [];
    let baseTime = new Date('2018-05-01T00:00:00').getTime();
    let dayMs = 24 * 60 * 60 * 1000;
    for(let i = 0; i < numItems; i++) {
        data.push({
            time: new Date(baseTime + i * dayMs),
            value: Math.round(20 + 80 * Math.random())
        });
    }
    return data;
}

function getData() {
    let data = [];

    data.push({
        title: 'Visits',
        data: getRandomDateArray(30)
    });

    data.push({
        title: 'Categories',
        data: getRandomArray(10)
    });

    console.log(data)
    return data;
}

const InsightsWrapper = () => {
    const [state, setState] = React.useState(null);
    const [activeTab, setActiveTab] = React.useState('Pulse');

    React.useEffect(() => {
        setState(getData());
    }, []);

    return (
        <div className="row mt-4">
            <div className="col-2">
                <div className="list-group">
                    <button type="button" className="list-group-item list-group-item-action" onClick={() => setActiveTab('Pulse')}>Pulse</button>
                    <button type="button" className="list-group-item list-group-item-action" onClick={() => setActiveTab('Contributors')}>Contributors</button>
                    <button type="button" className="list-group-item list-group-item-action" onClick={() => setActiveTab('Commits')}>Commits</button>
                </div>
            </div>
            <div className="col-10">
                { activeTab === 'Pulse' && <Pulse /> }
                { activeTab === 'Contributors' && <Contributors data={state[0]}/> }
                { activeTab === 'Commits' && <Commits barData={state[1]} lineData={state[0]}/>}
            </div>
        </div>
    );
};

export default InsightsWrapper;
