import {useState} from "react";
import {useRouter} from "next/router";
import ProjectService from "../../services/projectService";
import Spinner from "../../components/util/spinner";

const NewRepository = () => {
    const emptyProject = {
        name: "",
        repositoryUrl: "",
        description: "",
        isPublic: true,
    };

    const router = useRouter();
    const [project, setProject] = useState(emptyProject);
    const [loading, setLoading] = useState(false);

    const [error, setError] = useState("");

    const onSubmit = async (event) => {
        event.preventDefault();
        setLoading(true);
        try {
            await ProjectService.create(project).then(() => {
                router.push("/project");
                setLoading(false);
            });
        } catch (error) {
            setError(error?.response?.data);
            setLoading(false);
        }
    };

    const handleChange = (name) => (event) => {
        setError("");
        setProject({...project, [name]: event.target.value});
    };
    return (
        <>
            {
                loading ? <Spinner msg={"Creating your project, please wait..."}/> :
                    <>

                        <h1>Create a new project</h1>
                        <form onSubmit={onSubmit}>
                            <div className="form-group">
                                <label>Project name</label>
                                <input
                                    type="text"
                                    className="form-control"
                                    value={project.name}
                                    onChange={handleChange("name")}
                                    required
                                />
                            </div>
                            <div className="form-group">
                                <label>Repository URL</label>
                                <input
                                    type="text"
                                    className="form-control"
                                    value={project.repositoryUrl}
                                    onChange={handleChange("repositoryUrl")}
                                    required
                                />
                            </div>
                            <div className="form-group">
                                <label>Description</label>
                                <textarea
                                    className="form-control"
                                    rows={10}
                                    value={project.description}
                                    onChange={handleChange("description")} />
                            </div>

                            <div className="form-check">
                                <input
                                    className="form-check-input"
                                    type="checkbox"
                                    checked={project.isPublic}
                                    onChange={(event) =>
                                        setProject({...project, isPublic: event.target.checked})
                                    }
                                />
                                <label className="form-check-label">Is public?</label>
                            </div>
                            <div className="form-group">
                                <input
                                    type="submit"
                                    className="btn btn-success"
                                    value="Create project"
                                />
                            </div>
                            <div className="text-danger">{error}</div>
                        </form>
                    </>}
        </>
    );
}
;

export default NewRepository;
