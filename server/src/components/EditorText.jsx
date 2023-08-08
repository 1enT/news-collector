import React, { useState, useCallback } from 'react'
import { createEditor, Editor, Transforms } from 'slate'
import { Slate, Editable, withReact } from 'slate-react'

const EditorTextComponent = () => {
    [window.textEditor] = useState(() => withReact(createEditor()))
    const [textReadOnly, setTextEditable] = useState(false)
    window.setTextEditable = setTextEditable

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
        <Slate editor={window.textEditor} value={initialValue}>
            <Editable renderElement={renderElement} readOnly={!textReadOnly} style={{position: "static"}}/>
        </Slate>
    )
}

function RefreshTextText(text) {
    window.textEditor.children.map(item => {
        Transforms.delete(window.textEditor, { at: [0] })
    })
    window.textEditor.children = [
    {
        type: "p",
        children: [{ text: "" }]
    }];
    Transforms.insertText(window.textEditor, text, {
        at: { path: [0, 0], offset: 0 },
    })
}

function rrr(text) {
    window.textEditor.children.map(item => {
        Transforms.delete(window.textEditor, { at: [0] })
    })
    window.textEditor.children = [
    {
        type: "p",
        children: [{ text: "" }]
    }];
    Transforms.removeNodes(window.textEditor, {
       at: [0],
    })

    const BLOCK_TAGS = {
        p: 'paragraph',
        h2: 'header',
        img: 'image'
    }

    const rules = [
        {
            deserialize(el, next) {
              const type = BLOCK_TAGS[el.tagName.toLowerCase()]
              if (type) {
                return {
                  object: 'block',
                  type: type,
                  data: {
                    className: el.getAttribute('class'),
                  },
                  nodes: next(el.childNodes),
                }
              }
            },
        },
    ]
}

export {EditorTextComponent, RefreshTextText}