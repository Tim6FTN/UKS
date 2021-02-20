import React from 'react';
import Pulse from "./pulse";
import Commits from "./commits";
import Contributors from "./contributors";
import codeService from "../../services/codeService";
import taskService from "../../services/taskService";
import {convertUnixTimestampToDate} from "../../helpers/date.helper";

const InsightsWrapper = ({project}) => {
    const [activeTab, setActiveTab] = React.useState('Pulse');

    // pulse
    const [activeTasks, setActiveTasks] = React.useState(0);
    const [closedTasks, setClosedTasks] = React.useState(0);
    const [totalCommitsToMain, setTotalCommitsToMain] = React.useState(0);
    const [mainMetaData, setMainMetaData] = React.useState({});

    // contributors
    const [commits, setCommits] = React.useState({});
    const [contributors, setContributors] = React.useState([]);

    React.useEffect(() => {
        if (project) {
            taskService.getAll(project.id).then(tasks => {
                setActiveTasks(tasks.data.reduce((total, task) => (task.state === 'Open' ? total + 1 : total), 0));
                setClosedTasks(tasks.data.reduce((total, task) => (task.state === 'Closed' ? total + 1 : total), 0));
            })

            const temp = {
                filesAdded: 0,
                filesDeleted: 0,
                additions: 0,
                deletions: 0
            };

            codeService.getBranches(project.repository).then(branches => {
                const mainId = branches.data.find(branch => branch.name === 'main')?.id;
                codeService.getCommits(mainId).then(commitsResponse => {
                    setTotalCommitsToMain(commitsResponse.data.length);
                    commitsResponse.data.forEach(commit => {
                        temp.filesAdded += commit.commit_meta_data.file_additions_count;
                        temp.filesDeleted += commit.commit_meta_data.file_deletions_count;
                        temp.additions += commit.commit_meta_data.line_additions_count;
                        temp.deletions += commit.commit_meta_data.line_deletions_count;

                        convertUnixTimestampToDate(commit.timestamp);
                    });
                    setMainMetaData(temp);
                    setCommits(commitsResponse.data);
                })
            });

            setContributors([...project.collaborators].concat([project.owner]));
        }
    }, [project]);

    return (
        <div className="row mt-4">
            <div className="col-2">
                <div className="list-group">
                    <button type="button" className="list-group-item list-group-item-action"
                            onClick={() => setActiveTab('Pulse')}>Pulse
                    </button>
                    <button type="button" className="list-group-item list-group-item-action"
                            onClick={() => setActiveTab('Contributors')}>Contributors
                    </button>
                    <button type="button" className="list-group-item list-group-item-action"
                            onClick={() => setActiveTab('Commits')}>Commits
                    </button>
                </div>
            </div>
            <div className="col-10">
                {activeTab === 'Pulse' && <Pulse activeTasks={activeTasks}
                                                 closedTasks={closedTasks}
                                                 mainMetaData={mainMetaData}
                                                 totalCommitsToMain={totalCommitsToMain}/>}
                {activeTab === 'Contributors' && <Contributors commits={commits} contributors={contributors}/>}
                {activeTab === 'Commits' && <Commits commits={commits}/>}
            </div>
        </div>
    );
};

export default InsightsWrapper;
