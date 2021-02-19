import React, {useEffect, useState} from 'react';
import {DragDropContext, Droppable} from "react-beautiful-dnd";
import Card from "./card";
import styles from './kanban.module.css';
import {taskStatus} from "./task.model";
import TaskService from '../../services/taskService';
import {useRouter} from "next/router";

const BOARD_NAMES = ['Backlog', 'To Do', 'In Progress', 'Done'];
const POSSIBLE_STATUSES = ['Backlog', 'ToDo', 'InProgress', 'Done'];

const Board = ({isEditable}) => {
    const [tasks, setTasks] = useState([]);
    const [projectId, setProjectId] = useState(null);
    const router = useRouter();

    useEffect(() => {
        if (router.query.id) {
            getTasks(router.query.id);
            setProjectId(router.query.id);
        }
    }, [router.query.id]);

    const getTasks = async (id) => {
        const newTasks = (await TaskService.getAll(id)).data;
        setTasks([
            newTasks.filter(el => el.task_status === taskStatus.BACKLOG),
            newTasks.filter(el => el.task_status === taskStatus.TODO),
            newTasks.filter(el => el.task_status === taskStatus.IN_PROGRESS),
            newTasks.filter(el => el.task_status === taskStatus.DONE)
        ]);
    };

    function onDragEnd(res) {
        const {source, destination} = res;

        // dropped outside the list
        if (!destination) {
            return;
        }
        const sInd = +source.droppableId;
        const dInd = +destination.droppableId;

        if (sInd === dInd) {
            const items = reorder(tasks[sInd], source.index, destination.index);
            const newState = [...tasks];
            newState[sInd] = items;
            setTasks(newState);
        } else {
            const result = move(tasks[sInd], tasks[dInd], source, destination);
            const newState = [...tasks];
            newState[sInd] = result[sInd];
            newState[dInd] = result[dInd];

            setTasks(newState);
        }
    }

    const reorder = (list, startIndex, endIndex) => {
        const result = Array.from(list);
        const [removed] = result.splice(startIndex, 1);
        result.splice(endIndex, 0, removed);
        return result;
    }

    const move = (source, destination, droppableSource, droppableDestination) => {
        console.log('Source', source[droppableSource.index])    // task koji je premesten
        console.log('Destination', droppableDestination);       // droppable id je id board-a

        const sourceClone = Array.from(source);
        const destClone = Array.from(destination);
        const [removed] = sourceClone.splice(droppableSource.index, 1);

        destClone.splice(droppableDestination.index, 0, removed);

        const result = {};
        result[droppableSource.droppableId] = sourceClone;
        result[droppableDestination.droppableId] = destClone;

        const newStatus = POSSIBLE_STATUSES[droppableDestination.droppableId];
        const updatedTask = {...source[droppableSource.index], task_status: newStatus};
        updateStatus(updatedTask).then(() => console.log('success'));

        return result;
    };

    const updateStatus = async (updatedTask) => {
        await TaskService.patch(projectId, updatedTask.id, updatedTask);
    }

    return (
        <DragDropContext onDragEnd={onDragEnd}>
            <div className="row flex-nowrap">
                {tasks.map((el, ind) => (
                    <div className="col-3 p-2" key={ind}>
                        <Droppable droppableId={`${ind}`}>
                            {(provided,) => (
                                <div ref={provided.innerRef} {...provided.droppableProps} className={styles.board}>
                                    <h5 className={styles.boardTitle}>{BOARD_NAMES[ind]}</h5>
                                    {el.map((item, index) => (
                                        <Card key={item.id} task={item} index={index} projectId={projectId} isEditable={isEditable}/>
                                    ))}
                                    {provided.placeholder}
                                </div>
                            )}
                        </Droppable>
                    </div>
                ))}
            </div>
        </DragDropContext>
    );
};

export default Board;
