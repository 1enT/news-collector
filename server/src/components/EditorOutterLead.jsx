import React, { useState, useCallback } from 'react'
import { createEditor, Editor, Transforms } from 'slate'
import { Slate, Editable, withReact } from 'slate-react'

const EditorOutterLeadComponent = () => {
    [window.outterLeadEditor] = useState(() => withReact(createEditor()))
    const [outterLeadReadOnly, setOutterLeadEditable] = useState(false)
    window.setOutterLeadEditable = setOutterLeadEditable
    
    const initialValue = [
        {
            type: 'paragraph',
            children: [{ text: "" }],
        },
    ]

    const renderElement = useCallback(props => {
        console.log(props)
        switch (props.element.type) {
            case 'empty':
                return <p></p>
            default:
                return <p {...props.attributes}>{props.children}</p>
        }
    }, [])

    return (
        <Slate editor={window.outterLeadEditor} value={initialValue}>
            <Editable renderElement={renderElement} readOnly={!outterLeadReadOnly} style={{position: "static"}}/>
        </Slate>
    )
}

function fillSpace() {
    console.log(123)
    Transforms.insertText(window.outterLeadEditor, "123", {
        at: { path: [0, 0], offset: 0 },
    })
}

function RefreshOutterLeadText(text) {
    window.outterLeadEditor.children.map(item => {
        Transforms.delete(window.outterLeadEditor, { at: [0] })
    })
    window.outterLeadEditor.children = [
    {
        //type: text == "" ? "empty" : "p",
        type: "p",
        children: [{ text: "" }]
    }];
    Transforms.insertText(window.outterLeadEditor, text, {
        at: { path: [0, 0], offset: 0 },
    })
}

export {EditorOutterLeadComponent, RefreshOutterLeadText, fillSpace}