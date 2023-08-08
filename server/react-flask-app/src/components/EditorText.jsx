import React, { useState, useCallback } from 'react'
import { createEditor, Editor, Transforms, Text } from 'slate'
import { Slate, Editable, withReact } from 'slate-react'

import escapeHtml from 'escape-html'

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
        //console.log(props)
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
        type: "ppp",
        children: [{ text: "" }]
    }];
    Transforms.insertText(window.textEditor, text, {
        at: { path: [0, 0], offset: 0 },
    })

    //serialize(text)
    console.log(text)
    console.log(JSON.parse(text))
}

function PullTextTextOut() {
    let content = []
    window.textEditor.children.map(item => {
        item.children.map(item => {
            content.push(item.text)
        })
    })

    return content.join('\n')
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

function serialize (node) {
  if (Text.isText(node)) {
    let string = escapeHtml(node)
    if (node.bold) {
      string = `<strong>${string}</strong>`
    }
    return string
  }

  const children = node.children.map(n => serialize(n)).join('')

  switch (node.type) {
    case 'quote':
      return `<blockquote><p>${children}</p></blockquote>`
    case 'paragraph':
      return `<p>${children}</p>`
    case 'link':
      return `<a href="${escapeHtml(node.url)}">${children}</a>`
    default:
      return children
  }
}

export {EditorTextComponent, RefreshTextText, PullTextTextOut}