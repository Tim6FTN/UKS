import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faBold} from "@fortawesome/free-solid-svg-icons/faBold";
import {faItalic} from "@fortawesome/free-solid-svg-icons/faItalic";
import {faUnderline} from "@fortawesome/free-solid-svg-icons/faUnderline";
import {faCode} from "@fortawesome/free-solid-svg-icons/faCode";

const InlineStyleButton = ({style, onToggle, label, active}) => {
    const onMouseDown = (e) => {
        e.preventDefault();
        onToggle(style);
    }

    return (
        <button className="btn btn-light mr-1 my-1" style={{color: active ? 'blue' : null}} onMouseDown={onMouseDown}>
            {label === 'Bold' && <FontAwesomeIcon icon={faBold}/>}
            {label === 'Italic' && <FontAwesomeIcon icon={faItalic}/>}
            {label === 'Underline' && <FontAwesomeIcon icon={faUnderline}/>}
            {label === 'Monospace' && <FontAwesomeIcon icon={faCode}/>}
        </button>
    );
}

export default InlineStyleButton;
