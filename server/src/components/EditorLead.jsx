import React, { useState, useCallback } from 'react'
import { createEditor, Editor, Transforms } from 'slate'
import { Slate, Editable, withReact } from 'slate-react'

const EditorInnerLeadComponent = () => {
    [window.innerLeadEditor] = useState(() => withReact(createEditor()))
    const [innerLeadReadOnly, setInnerLeadEditable] = useState(false)
    window.setInnerLeadEditable = setInnerLeadEditable
    
    const initialValue = [
        {
            type: 'paragraph',
            children: [{ text: "" }],
        },
    ]

    const renderElement = useCallback(props => {
        //console.log(props.element.type)
        switch (props.element.type) {
            case 'code':
                return <p >TEST</p>
            default:
                return <p {...props.attributes}>{props.children}</p>
        }
    }, [])

    return (
        <Slate editor={window.innerLeadEditor} value={initialValue}>
            <Editable renderElement={renderElement} readOnly={!innerLeadReadOnly} style={{position: "static"}}/>
        </Slate>
    )
}

function RefreshInnerLeadText(text) {
    window.innerLeadEditor.children.map(item => {
        Transforms.delete(window.innerLeadEditor, { at: [0] })
    })
    window.innerLeadEditor.children = [
    {
        type: "p",
        children: [{ text: "" }]
    }];
    Transforms.insertText(window.innerLeadEditor, text, {
        at: { path: [0, 0], offset: 0 },
    })
}

export {EditorInnerLeadComponent, RefreshInnerLeadText}