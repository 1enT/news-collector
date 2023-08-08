import React, { useState, useCallback } from 'react'
import { createEditor, Editor, Transforms } from 'slate'
import { Slate, Editable, withReact } from 'slate-react'

/*const [headEditor] = useState(() => withReact(createEditor()))
const [bodyEditor] = useState(() => withReact(createEditor()))*/

const headEditor = 0
const bodyEditor = 1

const SlateEditorComponentTest = ({part}) => {
    /*const editor = part == 'head' ? headEditor : bodyEditor

    const initialValue = [
        {
            type: 'paragraph',
            children: [{ text: "" }],
        },
    ]

  

  const renderElement = useCallback(props => {
    console.log(props.element.type)
    switch (props.element.type) {
      case 'code':
        return <p >TEST</p>
      default:
        return <p {...props.attributes}>{props.children}</p>
    }
  }, [])

  return (
    <Slate editor={editor} value={initialValue}>
      <button onClick={() => {
        Transforms.insertText(editor, 'some words', {
              at: { path: [0, 0], offset: 3 },
            })
      }
      }>click</button>
      <Editable
        renderElement={renderElement}
        onKeyDown={event => {
          if (event.key === '`' && event.ctrlKey) {
            // Prevent the "`" from being inserted by default.
            event.preventDefault()
            // Otherwise, set the currently selected blocks type to "code".
            
            Transforms.insertText(editor, 'some words', {
              at: { path: [0, 0], offset: 3 },
            })
          }
        }}
      />
    </Slate>
  )*/
}

/*const RefreshHeadText = (text) => {
    Transforms.insertText(headEditor, text, {
        at: { path: [0, 0], offset: 0 },
    })
}

const RefreshBodyText = (text) => {
    Transforms.insertText(bodyEditor, text, {
        at: { path: [0, 0], offset: 0 },
    })
}*/

export default SlateEditorComponentTest