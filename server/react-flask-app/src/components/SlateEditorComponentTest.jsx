import React, { useState, useCallback } from 'react'
import { createEditor, Editor, Transforms } from 'slate'
import { Slate, Editable, withReact } from 'slate-react'

/*const [headEditor] = useState(() => withReact(createEditor()))
const [bodyEditor] = useState(() => withReact(createEditor()))*/

const SlateEditorComponentTest = ({part}) => {
    [window.titleEditor] = useState(() => withReact(createEditor()))
    [window.innerLeadEditor] = useState(() => withReact(createEditor()))
    [window.outterEditor] = useState(() => withReact(createEditor()))
    [window.textEditor] = useState(() => withReact(createEditor()))
    
    let editor = 0
    if (part == 'title') {
        editor = window.titleEditor
    } else if (part == 'innerLead') {
        editor = window.innerLeadEditor
    } else if (part == 'outterLead') {
        editor = window.outterLeadEditor
    } else if (part == 'text') {
        editor = window.textEditor
    }
    console.log(editor)
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
    //console.log(part)
    if (part == 'title') {
        return (
            <Slate editor={window.titleEditor} value={initialValue}>
                <Editable renderElement={renderElement} />
            </Slate>
        )
    } else if (part == 'innerLead') {
        return (
            <Slate editor={window.innerLeadEditor} value={initialValue}>
                <Editable renderElement={renderElement} />
            </Slate>
        )
    } else if (part == 'outterLead') {
        return (
            <Slate editor={window.outterLeadEditor} value={initialValue}>
                <Editable renderElement={renderElement} />
            </Slate>
        )
    } else if (part == 'text') {
        return (
            <Slate editor={window.textEditor} value={initialValue}>
                <Editable renderElement={renderElement} />
            </Slate>
        )
    }
}


        /*onKeyDown={event => {
          if (event.key === '`' && event.ctrlKey) {
            // Prevent the "`" from being inserted by default.
            event.preventDefault()
            // Otherwise, set the currently selected blocks type to "code".
            
            Transforms.insertText(editor, 'some words', {
              at: { path: [0, 0], offset: 0 },
            })
          }
        }}*/

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

function RefreshOutterLeadText(text) {
    window.outterLeadEditor.children.map(item => {
        Transforms.delete(window.outterLeadEditor, { at: [0] })
    })
    window.outterLeadEditor.children = [
    {
        type: "p",
        children: [{ text: "" }]
    }];
    Transforms.insertText(window.outterLeadEditor, text, {
        at: { path: [0, 0], offset: 0 },
    })
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

export {SlateEditorComponentTest, RefreshTitleText, RefreshInnerLeadText, RefreshOutterLeadText, RefreshTextText}