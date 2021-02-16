import RichEditor from "../../../components/rich-editor/editor";
import {ProjectContext} from "../../../contexts/projectContext";
import ProjectWrapper from "../../../components/project/wrapper";
import {useContext} from "react";

const Wiki = () => {
    const { project } = useContext(ProjectContext);

    return (
        <ProjectWrapper>
            <RichEditor project={project}/>
        </ProjectWrapper>
    )
};

export default Wiki;
