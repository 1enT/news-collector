import React, { useState, useCallback } from 'react'
import { createEditor, Editor, Transforms } from 'slate'
import { Slate, Editable, withReact } from 'slate-react'

const EditorLeadComponent = () => {
    [window.leadEditor] = useState(() => withReact(createEditor()))
    const [leadReadOnly, setLeadEditable] = useState(false)
    window.setLeadEditable = setLeadEditable
    
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
        <Slate editor={window.leadEditor} value={initialValue}>
            <Editable renderElement={renderElement} readOnly={!leadReadOnly} style={{position: "static"}}/>
        </Slate>
    )
}

function RefreshLeadText(text) {
    window.leadEditor.children.map(item => {
        Transforms.delete(window.leadEditor, { at: [0] })
    })
    window.leadEditor.children = [
    {
        type: "p",
        children: [{ text: "" }]
    }];
    Transforms.insertText(window.leadEditor, text, {
        at: { path: [0, 0], offset: 0 },
    })
}

function PullLeadTextOut() {
    let content = []
    window.leadEditor.children.map(item => {
        item.children.map(item => {
            content.push(item.text)
        })
    })

    return content.join('\n')
}

export {EditorLeadComponent, RefreshLeadText, PullLeadTextOut}