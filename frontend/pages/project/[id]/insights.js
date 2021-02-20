import ProjectWrapper from "../../../components/project/wrapper";
import InsightsWrapper from "../../../components/insights/wrapper";
import {useContext} from "react";
import {ProjectContext} from "../../../contexts/projectContext";

const Insights = () => {
    const { project } = useContext(ProjectContext);

    return (
        <ProjectWrapper>
            <InsightsWrapper project={project}/>
        </ProjectWrapper>
    )
};

export default Insights;
