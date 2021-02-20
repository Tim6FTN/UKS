import RichEditor from "../../../components/rich-editor/editor";
import {ProjectContext} from "../../../contexts/projectContext";
import ProjectWrapper from "../../../components/project/wrapper";
import {useContext} from "react";
import {UserContext} from "../../../contexts/userContext";

const Wiki = () => {
    const { project } = useContext(ProjectContext);
    const { user } = useContext(UserContext);

    return (
        <ProjectWrapper>
            <RichEditor project={project} user={user}/>
        </ProjectWrapper>
    )
};

export default Wiki;
