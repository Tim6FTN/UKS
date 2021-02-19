import React from "react";
import ProjectWrapper from "../../../components/project/wrapper";
import Board from "../../../components/kanban/board";
import {useContext} from "react";
import {UserContext} from "../../../contexts/userContext";
import {ProjectContext} from "../../../contexts/projectContext";

const Kanban = () => {
    const { user } = useContext(UserContext);
    const { project } = useContext(ProjectContext);

    const [isEditable, setIsEditable] = React.useState(false);

    React.useEffect(() => {
        const allowEdit = user?.id === project?.owner.id ||
            project?.collaborators?.find((el) => el.id === user.id);
        setIsEditable(allowEdit);
    }, [user]);

    return (
        <ProjectWrapper>
            <Board isEditable={isEditable}/>
        </ProjectWrapper>
    )
};

export default Kanban;
