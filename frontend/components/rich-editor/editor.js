import React from 'react';
import Draft, {Editor, EditorState, RichUtils} from 'draft-js';
import 'draft-js/dist/Draft.css';
import InlineStyleControls from "./inline-style-controls";
import {stateToHTML} from 'draft-js-export-html';
import {stateFromHTML} from 'draft-js-import-html';
import {useRouter} from "next/router";
import cogoToast from 'cogo-toast';
import ProjectService from "../../services/projectService";
import BlockStyleControls from "./block-style-controls";

const emptyContentState = Draft.convertFromRaw({
    entityMap: {},
    blocks: [
        {
            text: '',
            key: 'foo',
            type: 'unstyled',
            entityRanges: [],
        },
    ],
});

const RichEditor = ({project, user}) => {
    const [editorState, setEditorState] = React.useState(EditorState.createWithContent(emptyContentState));
    const [isEditable, setIsEditable] = React.useState(false);
    const [isMine, setIsMine] = React.useState(false);

    const editor = React.useRef(null);
    const router = useRouter();

    React.useEffect(() => {
        if (user && project) {
            const mine = project.owner.id === user.id;
            setIsEditable(mine);
            setIsMine(mine);
        }
    }, [user, project]);

    React.useEffect(() => {
        let contentState = stateFromHTML(project?.wiki_content);
        contentState && setEditorState(EditorState.createWithContent(contentState));
    }, [project]);

    const onSubmit = () => {
        const html = stateToHTML(editorState.getCurrentContent());
        const updatedProject = {...project};
        updatedProject.wiki_content = html;

        ProjectService.update(project.id, updatedProject).then(() => {
            cogoToast.success('Wiki updated!');
            router.push(`/project/${project.id}`);
        }, () => cogoToast.error('Oh no'));
    }

    const onChange = (newEditorState) => {
        setEditorState(newEditorState)
    }

    const toggleInlineStyle = (inlineStyle) => {
        onChange(RichUtils.toggleInlineStyle(editorState, inlineStyle));
    }

    const toggleBlockType = (blockType) => {
        onChange(RichUtils.toggleBlockType(editorState, blockType));
    }

    const handleKeyCommand = (command, newEditorState) => {
        const newState = RichUtils.handleKeyCommand(newEditorState, command);
        if (newState) {
            onChange(newState);
            return 'handled';
        }
        return 'not-handled';
    }

    return (
        <>
            {
                isEditable ?
                    <>
                        <div style={{
                            border: "1px solid lightgrey",
                            padding: '0 7px 0 7px',
                            borderRadius: '8px',
                            minHeight: "30em",
                            cursor: "text"
                        }}
                             onClick={() => editor.current.focus()}>
                            <div className="row px-3 justify-content-between">
                                <InlineStyleControls
                                    editorState={editorState}
                                    onToggle={toggleInlineStyle}
                                />
                                <BlockStyleControls
                                    editorState={editorState}
                                    onToggle={toggleBlockType}
                                />
                            </div>
                            <hr style={{margin: '0'}}/>
                            <div style={{marginTop: 10}}>
                                <Editor
                                    readOnly={!isEditable}
                                    ref={editor}
                                    editorKey="editorkey"
                                    editorState={editorState}
                                    onChange={onChange}
                                    placeholder="Write your wiki content here..."
                                    handleKeyCommand={handleKeyCommand}
                                />
                            </div>
                        </div>
                        <div className="container bg-light mt-1 rounded">
                            <div className="row justify-content-between p-3">
                                <div>
                                <button className="btn btn-success" onClick={onSubmit}>Submit wiki</button>
                                <button className="btn btn-info ml-2"
                                        onClick={() => setIsEditable(!isEditable)}>
                                    Preview
                                </button>
                                </div>
                                <button className="btn btn-light"
                                        onClick={() => router.push(`/project/${project.id}`)}>Cancel
                                </button>

                            </div>
                        </div>
                    </> :
                    <div style={{marginTop: 10}}>
                        <Editor
                            readOnly={true}
                            ref={editor}
                            editorKey="editorkey"
                            editorState={editorState}
                        />
                        {isMine &&
                            <div>
                                <hr/>
                                <button
                                    className="btn btn-info"
                                    onClick={() => setIsEditable(!isEditable)}>
                                    Back to edit
                                </button>
                            </div>
                        }
                    </div>
            }
        </>
    );
};

export default RichEditor;
