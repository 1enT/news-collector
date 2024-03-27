import React, { useEffect, useState, useCallback } from 'react'
import { createEditor, Editor, Transforms, Text } from 'slate'
import { Slate, Editable, withReact, ReactEditor } from 'slate-react'

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
        switch (props.element.type) {
            case 'plain':
                return <p {...props.attributes}>{props.children}</p>
            case 'img':
                return <img src={props.element.src} contentEditable={false}></img>
            default:
                return <p {...props.attributes}>{props.children}</p>
        }
    }, [])

    const renderLeaf = useCallback(props => {
        switch (props.leaf.type) {
            case 'plain':
                return (
                        <span 
                            {...props.attributes}
                            style = {{
                                fontWeight: props.leaf.bold ? 'bold' : 'normal',
                                fontStyle: props.leaf.cursive ? 'italic' : 'normal',
                                textDecoration: props.leaf.underline ? 'underline' : 'none'
                            }}
                        >{props.children}</span>)
            case 'a':
                return (
                        <a 
                            {...props.attributes}
                            href={props.leaf.href}
                            style = {{
                                fontWeight: props.leaf.bold ? 'bold' : 'normal',
                                fontStyle: props.leaf.cursive ? 'italic' : 'normal'
                            }}
                            target="_blank"
                        >{props.children}</a>)
        }
    }, [])

    window.linkButtonClickedType = ''
    window.selectedLinkLeaf = {}

    window.editor_style_bold_clicked = () => {
        console.log(window.selectedLinkLeaf)
        //window.textEditor.selection = window.selectedLinkLeaf
        let marks = Editor.marks(window.textEditor)
        if (marks) {
            let is_bold = marks.bold
            Editor.addMark(window.textEditor, 'bold', !is_bold)
            window.styleTextSelected('bold', !is_bold)
            ReactEditor.focus(window.textEditor)
        }
    }

    window.editor_style_italic_clicked = () => {
        let marks = Editor.marks(window.textEditor)
        if (marks) {
            let is_curs = marks.cursive
            Editor.addMark(window.textEditor, 'cursive', !is_curs)
            window.styleTextSelected('cursive', !is_curs)
            ReactEditor.focus(window.textEditor)
        }
    }

    window.editor_style_underline_clicked = () => {
        let marks = Editor.marks(window.textEditor)
        if (marks) {
            let is_underline = marks.underline
            Editor.addMark(window.textEditor, 'underline', !is_underline)
            window.styleTextSelected('underline', !is_underline)
            ReactEditor.focus(window.textEditor)
        }
    }

    window.editor_style_link_clicked = () => {
        if (window.linkButtonClickedType == 'a') {
            window.editor_style_link_close()
            return
        }

        window.linkButtonClickedType = 'a'
        document.getElementsByClassName('content_style_buttons_link_input')[0].style.visibility = 'visible'
        document.getElementsByClassName('content_style_buttons_link_input_abort')[0].style.visibility = 'visible'
    }

    window.editor_style_image_clicked = () => {
        if (window.linkButtonClickedType == 'img') {
            window.editor_style_link_close()
            return
        }

        window.linkButtonClickedType = 'img'
        document.getElementsByClassName('content_style_buttons_link_input')[0].style.visibility = 'visible'
        document.getElementsByClassName('content_style_buttons_link_input_abort')[0].style.visibility = 'hidden'
    }

    window.editor_style_link_clicked_enter = (event) => {
        Transforms.setSelection(window.textEditor)
        if (event.key == 'Enter') {
            switch (window.linkButtonClickedType) {
                case 'a':
                    if (JSON.stringify(window.selectedLinkLeaf) == JSON.stringify({})) {
                        let marks = Editor.marks(window.textEditor)
                        if (marks) {
                            let input_href  = document.getElementsByClassName('content_style_buttons_link_input')[0].getElementsByTagName('input')[0].value
                            if ( !input_href.includes('https://') && !input_href.includes('http://') ) {
                                input_href = 'http://' + input_href
                            }
                            Editor.addMark(window.textEditor, 'type', 'a')
                            Editor.addMark(window.textEditor, 'href', input_href)
                        }
                    } else {
                        let marks = Editor.marks(window.textEditor)
                        if (marks) {
                            let input_href  = document.getElementsByClassName('content_style_buttons_link_input')[0].getElementsByTagName('input')[0].value
                            if ( !input_href.includes('https://') && !input_href.includes('http://') ) {
                                input_href = 'http://' + input_href
                            }
                            Transforms.select(window.textEditor, {
                                anchor: {
                                    path: window.selectedLinkLeaf.path,
                                    offset: 0
                                },
                                focus: {
                                    path: window.selectedLinkLeaf.path,
                                    offset: window.selectedLinkLeaf.offset
                                }
                            })
                            Editor.addMark(window.textEditor, 'href', input_href)
                        }
                    }
                    break
                case 'img':
                    let input_href  = document.getElementsByClassName('content_style_buttons_link_input')[0].getElementsByTagName('input')[0].value
                    if ( !input_href.includes('https://') && !input_href.includes('http://') ) {
                        input_href = 'http://' + input_href
                    }
                    Transforms.insertNodes(window.textEditor, {
                        'type': 'img',
                        'src': input_href,
                        'children': [{
                            'text': ''
                        }]
                    })
                    break
            }


            window.editor_style_link_close()
        }
    }

    window.editor_style_link_clicked_abort = () => {
        if (window.linkButtonClickedType) {
            if (JSON.stringify(window.selectedLinkLeaf) != JSON.stringify({})) {
                Transforms.select(window.textEditor, {
                    anchor: {
                        path: window.selectedLinkLeaf.path,
                        offset: 0
                    },
                    focus: {
                        path: window.selectedLinkLeaf.path,
                        offset: window.selectedLinkLeaf.offset
                    }
                })
                Editor.removeMark(window.textEditor, 'href')
                Editor.addMark(window.textEditor, 'type', 'plain')
            }
        }

        window.editor_style_link_close()
    }

    window.editor_style_link_close = () => {
        document.getElementsByClassName('content_style_buttons_link_input')[0].style.visibility = 'hidden'
        document.getElementsByClassName('content_style_buttons_link_input_abort')[0].style.visibility = 'hidden'
        document.getElementsByClassName('content_style_buttons_link_input')[0].getElementsByTagName('input')[0].value = ''
        window.linkButtonClickedType = ''
    }

    function specifySelectedLinkLeaf() {
        let editor_selection = window.textEditor.selection
        if (editor_selection !== null) {
            let anchor = editor_selection.anchor.path
            let focus = editor_selection.focus.path

            for (let i = anchor[0]; i <= focus[0]; i++) {
                for (let j = anchor[1]; j <= focus[1]; j++) {
                    let leaf = window.textEditor.children[i].children[j]
                    if (leaf.type == 'a') {
                        document.getElementsByClassName('content_style_buttons_link_input')[0].getElementsByTagName('input')[0].value = leaf.href
                        window.selectedLinkLeaf = {
                            path: [i, j],
                            offset: leaf.text.length,
                            leaf: leaf
                        }
                        return
                    }
                }
            }
        }
        document.getElementsByClassName('content_style_buttons_link_input')[0].getElementsByTagName('input')[0].value = ''
        window.selectedLinkLeaf = {}
    }

    return (
        <Slate editor={window.textEditor} value={initialValue}>
            <Editable 
                renderElement={renderElement}
                renderLeaf = {renderLeaf}
                readOnly={!textReadOnly}
                style={{position: "static"}}
                onKeyDown={event => {
                    let marks = Editor.marks(window.textEditor)
                    if (marks) {
                        let is_bold = marks.bold
                        let is_curs = marks.cursive
                        let is_underline = marks.underline

                        window.styleTextSelected('bold', is_bold)
                        window.styleTextSelected('italic', is_curs)
                        window.styleTextSelected('underline', is_underline)
                    }

                    specifySelectedLinkLeaf()
                }}
                onClick={event => {
                    let marks = Editor.marks(window.textEditor)
                    if (marks) {
                        let is_bold = marks.bold
                        let is_curs = marks.cursive
                        let is_underline = marks.underline

                        window.styleTextSelected('bold', is_bold)
                        window.styleTextSelected('cursive', is_curs)
                        window.styleTextSelected('underline', is_underline)
                    }

                    specifySelectedLinkLeaf()
                }}
            />
        </Slate>
    )
}

function RefreshTextText(text, link) {
    /*let json_link = {
        type: 'p',
        children: [{
            type: 'a',
            href: link,
            text: link
        }]
    }
    let json_text = JSON.parse(text)
    json_text.push(json_link)*/
    let json_text = JSON.parse(text)
    window.textEditor.children.map(item => {
        Transforms.delete(window.textEditor, { at: [0] })
    })
    window.textEditor.children = json_text
}

function PullTextTextOut() {
    /*let content = []
    window.textEditor.children.map(item => {
        item.children.map(item => {
            content.push(item.text)
        })
    })

    return content.join('\n')*/
    //console.log(window.textEditor.children)
    return window.textEditor.children
}

export {EditorTextComponent, RefreshTextText, PullTextTextOut}