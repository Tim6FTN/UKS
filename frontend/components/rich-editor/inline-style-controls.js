import InlineStyleButton from "./inline-style-button";

const InlineStyleControls = ({editorState, onToggle}) => {
    const inlineStyles = [
        {label: 'Bold', style: 'BOLD'},
        {label: 'Italic', style: 'ITALIC'},
        {label: 'Underline', style: 'UNDERLINE'},
        {label: 'Monospace', style: 'CODE'},
    ];

    const currentStyle = editorState.getCurrentInlineStyle();
    return (
        <div>
            {inlineStyles.map(type =>
                <InlineStyleButton
                    key={type.label}
                    active={currentStyle.has(type.style)}
                    label={type.label}
                    onToggle={onToggle}
                    style={type.style}
                />
            )}
        </div>
    );
};

export default InlineStyleControls;
