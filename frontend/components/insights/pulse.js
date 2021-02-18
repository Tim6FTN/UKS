const Pulse = () => {

    return (
        <div className="card">
            <div className="card-header">Overview</div>
            <div className="card-body row">
                <div className="col-6">Closed tasks: 12</div>
                <div className="col-6">New tasks: 8</div>
            </div>

            <hr/>

            <div className="card-body">
                <h5 className="font-weight-lighter">
                    Excluding merges, <b>5</b> authors have pushed 44 commits to dev and 61
                    commits to all branches. On dev, 147 files have changed and there have been 9,771 additions and
                    7,957 deletions.
                </h5>
            </div>
        </div>
    );
};

export default Pulse;
