import {Draggable} from "react-beautiful-dnd";
import React from "react";
import styles from './kanban.module.css';
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faTrophy, faUserNinja} from "@fortawesome/free-solid-svg-icons";

const Card = ({task, index}) => {
    return (
        <Draggable draggableId={task.id} index={index} >
            {provided => (
                <div className={`card m-2 ${styles.cardCustom}`} ref={provided.innerRef}
                     {...provided.draggableProps}
                     {...provided.dragHandleProps}>
                    <div className="card-body pb-1">
                        <h6 className="card-subtitle mb-1" style={{color: '#0464d4'}}>{task.title}</h6>
                        <span className={styles.cardSmallText}>
                            Opened by: <b>Usernaam</b>
                        </span>
                        <div className={`row justify-content-between mt-3 ${styles.cardSmallText}`}>
                            <div className="row justify-content-center ml-3">
                                <FontAwesomeIcon className="mr-1" icon={faTrophy}/>
                                <p>Stable release</p>
                            </div>
                            {
                                //todo if assigned render user
                            }
                            <div className="mr-3">
                                <FontAwesomeIcon icon={faUserNinja} />
                            </div>
                        </div>
                    </div>

                </div>

            )}
        </Draggable>
    );
};

export default Card;