import React, { useState, useCallback } from 'react'
import { createEditor, Editor, Transforms } from 'slate'
import { Slate, Editable, withReact } from 'slate-react'

const EditorTitleComponent = () => {
    [window.titleEditor] = useState(() => withReact(createEditor()))
    const [titleReadOnly, setTitleEditable] = useState(false)
    window.setTitleEditable = setTitleEditable

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
        <Slate editor={window.titleEditor} value={initialValue}>
            <Editable renderElement={renderElement} readOnly={!titleReadOnly} style={{position: "static"}}/>
        </Slate>
    )
}

function RefreshTitleText(text) {
    window.titleEditor.children.map(item => {
        Transforms.delete(window.titleEditor, { at: [0] })
    })
    window.titleEditor.children = [
    {
        type: "p",
        children: [{ text: "" }]
    }];
    Transforms.insertText(window.titleEditor, text, {
        at: { path: [0, 0], offset: 0 },
    })
}

function PullTitleTextOut() {
    let content = []
    window.titleEditor.children.map(item => {
        item.children.map(item => {
            content.push(item.text)
        })
    })

    return content.join('\n')
}

export {EditorTitleComponent, RefreshTitleText, PullTitleTextOut}