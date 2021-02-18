import React, {useState} from 'react';
import {DragDropContext, Droppable} from "react-beautiful-dnd";
import Card from "./card";
import styles from './kanban.module.css';
import {taskPiority, taskState, taskStatus} from "./task.model";

const TaskList = React.memo(function TaskList({tasks}) {
    return tasks.map((task, index) => (
        <Card task={task} index={index} key={task.id}/>
    ));
});

const BOARD_NAMES = ['Backlog', 'To Do', 'In Progress', 'Done'];

const Board = () => {
    const tasks = [
        {
            id: '1',
            content: 'Task 1',
            title: 'titaaaaaaaaaaaaaaaaaaaaaaaassssssssssssssssssssssssssssaaaale',
            priority: taskPiority.LOW,
            state: taskState.OPEN,
            status: taskStatus.BACKLOG
        },
        {
            id: '2',
            content: 'Task 2',
            title: 'title',
            priority: taskPiority.LOW,
            state: taskState.OPEN,
            status: taskStatus.TODO
        },
        {
            id: '3',
            content: 'Task 3',
            title: 'title',
            priority: taskPiority.LOW,
            state: taskState.OPEN,
            status: taskStatus.IN_PROGRESS
        },
        {
            id: '4',
            content: 'Task 4',
            title: 'title',
            priority: taskPiority.LOW,
            state: taskState.OPEN,
            status: taskStatus.DONE
        },
        {
            id: '5',
            content: 'Task 5',
            title: 'title',
            priority: taskPiority.LOW,
            state: taskState.OPEN,
            status: taskStatus.BACKLOG
        },
        {
            id: '6',
            content: 'Task 6',
            title: 'title',
            priority: taskPiority.LOW,
            state: taskState.OPEN,
            status: taskStatus.BACKLOG
        },
    ];

    const [state, setState] = useState([]);

    React.useEffect(() => {
        // todo load tasks
        setState([
            tasks.filter(el => el.status === taskStatus.BACKLOG),
            tasks.filter(el => el.status === taskStatus.TODO),
            tasks.filter(el => el.status === taskStatus.IN_PROGRESS),
            tasks.filter(el => el.status === taskStatus.DONE)
        ])
    }, []);

    function onDragEnd(result) {
        const {source, destination} = result;

        // dropped outside the list
        if (!destination) {
            return;
        }
        const sInd = +source.droppableId;
        const dInd = +destination.droppableId;

        if (sInd === dInd) {
            const items = reorder(state[sInd], source.index, destination.index);
            const newState = [...state];
            newState[sInd] = items;
            setState(newState);
        } else {
            const result = move(state[sInd], state[dInd], source, destination);
            const newState = [...state];
            newState[sInd] = result[sInd];
            newState[dInd] = result[dInd];

            setState(newState);
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

        return result;
    };

    return (
        <DragDropContext onDragEnd={onDragEnd}>
            <div className="row flex-nowrap">
                {state.map((el, ind) => (
                    <div className="col-3 p-2" key={ind}>
                        <Droppable droppableId={`${ind}`}>
                            {(provided,) => (
                                <div ref={provided.innerRef} {...provided.droppableProps} className={styles.board}>
                                    <h5 className={styles.boardTitle}>{BOARD_NAMES[ind]}</h5>
                                    {el.map((item, index) => (
                                        <Card key={item.id} task={item} index={index}/>
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
