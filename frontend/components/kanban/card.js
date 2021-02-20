import {Draggable} from "react-beautiful-dnd";
import React from "react";
import styles from './kanban.module.css';
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faTrophy, faUserNinja} from "@fortawesome/free-solid-svg-icons";
import Link from 'next/link';

const Card = ({task, index, projectId, isEditable}) => {
    return (
        <Draggable draggableId={task.id + ""} index={index} isDragDisabled={!isEditable}>
            {provided => (
                <div className={`card m-2 ${styles.cardCustom}`} ref={provided.innerRef}
                     {...provided.draggableProps}
                     {...provided.dragHandleProps}>
                    <div className="card-body pb-2">
                        <h6 className="card-subtitle mb-1" style={{color: '#0464d4'}}>
                            {
                                isEditable ?
                                    <Link href={`/project/${projectId}/task/${task.id}`}>
                                        {task.title}
                                    </Link> : <span>{task.title}</span>
                            }
                        </h6>
                        <span className={styles.cardSmallText}>
                            Opened by: <b>{task.author.username}</b>
                        </span>
                        <div className={`row justify-content-between mt-3 ${styles.cardSmallText}`}>
                            <div className="row justify-content-center ml-3">
                                <FontAwesomeIcon className="mr-1" icon={faTrophy}/>
                                {
                                    task.milestoneInfo ? <span>{task.milestoneInfo.title}</span>
                                        : <span className="small">No milestone</span>
                                }
                            </div>
                            {
                                task.assignees.length > 0 &&
                                <div className="mr-3">
                                    <FontAwesomeIcon icon={faUserNinja} />
                                </div>
                            }
                        </div>
                    </div>
                </div>
            )}
        </Draggable>
    );
};

export default Card;