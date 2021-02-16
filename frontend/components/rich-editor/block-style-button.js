import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faListOl, faListUl, faTerminal} from "@fortawesome/free-solid-svg-icons";

const BlockStyleButton = ({style, onToggle, active, label}) => {
    const onMouseDown = (e) => {
        e.preventDefault();
        onToggle(style);
    }

    return (
        <button className="btn btn-light mr-1 my-1" style={{color: active ? 'blue' : null}} onMouseDown={onMouseDown}>
            {label === 'H1' && <b>H1</b>}
            {label === 'H2' && <b>H2</b>}
            {label === 'H3' && <b>H3</b>}
            {label === 'H4' && <b>H4</b>}
            {label === 'H5' && <b>H5</b>}
            {label === 'H6' && <b>H6</b>}
            {label === 'UL' && <FontAwesomeIcon icon={faListUl}/>}
            {label === 'OL' && <FontAwesomeIcon icon={faListOl}/>}
            {label === 'Code Block' && <FontAwesomeIcon icon={faTerminal}/>}
        </button>
    );
}

export default BlockStyleButton;
