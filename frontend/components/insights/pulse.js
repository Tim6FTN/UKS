const Pulse = ({activeTasks, closedTasks, mainMetaData, totalCommitsToMain}) => {

    return (
        <div className="card">
            <div className="card-header">Overview</div>
            <div className="card-body row">
                <div className="col-6 align-self-center"><h5 style={{color: 'red'}}>Closed tasks: {closedTasks}</h5></div>
                <div className="col-6"><h5 style={{color: 'green'}}>New tasks: {activeTasks}</h5></div>
            </div>

            <hr className="mt-0"/>

            <div className="card-body">

                <h5 className="font-weight-lighter">
                    Including all <b>{totalCommitsToMain}</b> commits to main,
                    <b> {mainMetaData.filesAdded}</b> files have been added, <b>{mainMetaData.filesDeleted}</b> files have been deleted
                    and there have been <b style={{color: 'green'}}>{mainMetaData.additions}</b> additions and
                    <b style={{color: 'red'}}> {mainMetaData.deletions}</b> deletions.
                </h5>
            </div>
        </div>
    );
};

export default Pulse;
