import {ProjectContext} from "../../../contexts/projectContext";
import ProjectWrapper from "../../../components/project/wrapper";
import Board from "../../../components/kanban/board";
import {useContext} from "react";

const Kanban = () => {
    const { project } = useContext(ProjectContext);

    return (
        <ProjectWrapper>
            <Board />
        </ProjectWrapper>
    )
};

export default Kanban;