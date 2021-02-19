const Spinner = ({msg}) => {
    return (
        <div className="text-center">
            <div className="spinner-border mb-2" role="status">
                <span className="sr-only">Loading...</span>
            </div>
            <h4 className="font-weight-lighter">{msg}</h4>
        </div>
    )
}

export default Spinner;
