import React, { useEffect, useState, useCallback, useRef } from 'react'
import { createEditor, Editor, Transforms, Text, Range, Node, Element } from 'slate'
import { Slate, Editable, withReact, ReactEditor, useSlate, useFocused } from 'slate-react'
//import { withHistory, HistoryEditor, History } from 'slate-history'

//import escapeHtml from 'escape-html'
import Emoji from './Emoji'

//import HoveringToolbar from './HoveringToolbar'

const withNormalize = editor => {
    const { normalizeNode } = editor

    editor.normalizeNode = entry => {
        const [node, path] = entry

        if (Text.isText(node) && !node.hasOwnProperty('selected') && (
            node.hasOwnProperty('href') || node.hasOwnProperty('bold') || node.hasOwnProperty('cursive') || node.hasOwnProperty('underline')
        )) {
            let left_spaces = node.text.match(/^\s+/)
            let right_spaces = node.text.match(/\s+$/)
            if (left_spaces != null) {
                Transforms.select(editor, {
                    anchor: { offset: 0, path: path },
                    focus: { offset: left_spaces[0].length, path: path }
                })
                Editor.removeMark(editor, 'href')
                Editor.removeMark(editor, 'bold')
                Editor.removeMark(editor, 'cursive')
                Editor.removeMark(editor, 'underline')
                Transforms.collapse(editor, {edge: 'anchor'})
            }
            if (right_spaces != null) {
                Transforms.select(editor, {
                    anchor: { offset: right_spaces.index, path: path },
                    focus: { offset: right_spaces.index+right_spaces[0].length, path: path }
                })
                Editor.removeMark(editor, 'href')
                Editor.removeMark(editor, 'bold')
                Editor.removeMark(editor, 'cursive')
                Editor.removeMark(editor, 'underline')
                Transforms.collapse(editor, {edge: 'focus'})
            }
        }
        normalizeNode(entry)
    }
    return editor
}

const EditorTextComponent = () => {
    /*const { normalizeNode } = window.textEditor
    window.textEditor.normalizeNode = entry => {
        const [node, path] = entry
        console.log(entry)
        //if (Text.isText(node) && node.text == 'p') {

        //}

        normalizeNode(entry)
    }*/
    /*window.fff = () => {
        const { normalizeNode } = window.textEditor
        //Editor.normalize(window.textEditor)
        window.textEditor.normalizeNode = entry => {
            const [node, path] = entry
            console.log(entry)

            normalizeNode(entry)
        }
        Editor.normalize(window.textEditor)
    }*/

    //[window.textEditor] = useState(() => withReact( withHistory(createEditor()) ))
    [window.textEditor] = useState(() => withNormalize(withReact( createEditor() )))
    const [textReadOnly, setTextEditable] = useState(false)
    window.setTextEditable = setTextEditable

    const initialValue = [
        {
            type: 'paragraph',
            children: [{ text: "" }],
        },
    ]

    const { isVoid, insertText, deleteBackward, deleteForward, insertBreak, deleteFragment } = window.textEditor
    window.textEditor.isVoid = elem => {
        return elem.type == 'img'
    }
    window.textEditor.insertBreak = () => {
        let cur_anchor = window.textEditor.selection.anchor
        let cur_focus = window.textEditor.selection.focus
        let prev = Editor.before(window.textEditor, window.textEditor.selection.anchor)
        let next = Editor.after(window.textEditor, window.textEditor.selection.focus)
        if (next == undefined || next.path[0] - cur_focus.path[0] >= 1) { // Каретка в конце нода
            Transforms.insertNodes(window.textEditor, {
                type: 'p',
                children: [{
                    type: 'plain',
                    text: ''
                }]
            })
        } else if (prev == undefined || cur_anchor.path[0] - prev.path[0] >= 1) { // Каретка в начале нода
            Transforms.insertNodes(window.textEditor, {
                type: 'p',
                children: [{
                    type: 'plain',
                    text: ''
                }]
            })
            Transforms.select(window.textEditor, {
                anchor: { offset: 0, path: [cur_anchor.path[0]+1, 0] },
                focus: { offset: 0, path: [cur_anchor.path[0]+1, 0] }
            })
        } else {
            insertBreak()
        }
    }
    window.textEditor.insertText = (text) => {
        console.log(text)
        Editor.addMark(window.textEditor, 'bold', true)
        insertText(text)
    }
    // Работает только, когда нет выделения! Сделать то же самое, но для случая с выделением
    window.textEditor.deleteBackward = (options) => {
        let cur_anchor = window.textEditor.selection.anchor
        let prev = Editor.before(window.textEditor, window.textEditor.selection.anchor)
        let cur_node = Editor.first(window.textEditor, cur_anchor)
        if (prev == undefined && cur_node[0].text == '') {
            Editor.deleteForward(window.textEditor)
        } else {
            deleteBackward(options)
        }
    }
    window.textEditor.deleteForward = (options) => {
        let cur_focus = window.textEditor.selection.focus
        let next = Editor.after(window.textEditor, window.textEditor.selection.focus)
        let cur_node = Editor.last(window.textEditor, cur_focus)
        if (next == undefined && cur_node[0].text == '') {
            Editor.deleteBackward(window.textEditor)
        } else {
            deleteForward(options)
        }
    }

    const renderElement = useCallback(props => {
        switch (props.element.type) {
            case 'plain':
                return <p {...props.attributes}>{props.children}</p>
            case 'img':
                return (
                    <div {...props.attributes}>
                        <div> {/*contentEditable={false}*/}
                            <img src={props.element.src}></img>
                        </div>
                        {props.children}
                    </div>
                )
            case 'quote':
                return (<blockquote {...props.attributes}>{props.children}</blockquote>)
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
                                //textDecoration: props.leaf.underline ? 'underline' : 'none'
                                //textDecoration: props.leaf.selected ? 'underline' : 'none'
                                borderBottom: props.leaf.selected ? '3px solid #3367d1' : 'none'
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
                                //borderBottom: props.leaf.selected ? '3px solid #3367d1' : 'none'
                            }}
                            target="_blank"
                        >{props.children}</a>)
        }
        return <a 
                    {...props.attributes}
                    style = {{color: 'red'}}
                >{props.children}</a>
    }, [])

    window.linkButtonClickedType = ''
    window.selectedLinkLeaf = {}

    window.editor_style_bold_clicked = (e) => {
        //console.log(window.selectedLinkLeaf)
        //window.textEditor.selection = window.selectedLinkLeaf
        let marks = Editor.marks(window.textEditor)
        if (marks) {
            collapse_underline_selection()
            /*let { selection } = window.textEditor
            Transforms.select(window.textEditor, {
                anchor: {
                    path: selection.anchor.path,
                    offset: 0
                },
                focus: {
                    path: selection.focus.path,
                    offset: 0
                }
            })*/
            let is_bold = marks.bold
            if (!is_bold)
                Editor.addMark(window.textEditor, 'bold', true)
            else
                Editor.removeMark(window.textEditor, 'bold')
            window.styleTextSelected('bold', !is_bold)
            ReactEditor.focus(window.textEditor)
            window.editor_deselect()

            //collapse_selection()
            /*marks = Editor.marks(window.textEditor)
            if (!marks.href && !marks.cursive && !marks.bold) {
                let { selection } = window.textEditor
                Transforms.mergeNodes(window.textEditor, {
                    at: selection.anchor.path,
                    match: (node, path) => {
                        console.log(node, path)
                        return path.length == 2
                        //return true
                    }
                })
            }*/
        }
    }

    window.editor_style_italic_clicked = () => {
        let marks = Editor.marks(window.textEditor)
        if (marks) {
            collapse_underline_selection()
            let is_curs = marks.cursive
            if (!is_curs)
                Editor.addMark(window.textEditor, 'cursive', true)
            else
                Editor.removeMark(window.textEditor, 'cursive')
            window.styleTextSelected('cursive', !is_curs)
            ReactEditor.focus(window.textEditor)
            window.editor_deselect()
        }
    }

    /*window.editor_style_underline_clicked = () => {
        let marks = Editor.marks(window.textEditor)
        if (marks) {
            let is_underline = marks.underline
            Editor.addMark(window.textEditor, 'underline', !is_underline)
            window.styleTextSelected('underline', !is_underline)
            ReactEditor.focus(window.textEditor)
        }
    }*/

    window.editor_style_quote_clicked = () => {
        let marks = Editor.marks(window.textEditor)
        if (marks) {
            collapse_underline_selection()
            let { selection } = window.textEditor
            let parent_node = Editor.parent(window.textEditor, selection.anchor.path)
            if (parent_node[0].type != 'quote') {
                //HistoryEditor.withoutSaving(window.textEditor, () => {
                    Transforms.insertNodes(window.textEditor, {
                        'type': 'quote',
                        'children': [{
                            'type': 'plain',
                            'text': Editor.string(window.textEditor, selection.anchor.path)
                        }]
                    })
                //})
            }
            ReactEditor.focus(window.textEditor)
            window.editor_deselect()
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

    window.editor_image_upload = (e) => {
        const file = e.target.files[0]
        if (file.type === "image/png" || file.type === "image/pjpeg" || file.type === "image/jpg" || file.type === "image/jpeg") {
            let src = URL.createObjectURL(file)
            //window.local_image_storage.push(file)
            window.local_image_storage[src] = file

            /*let reader = new FileReader()
            reader.readAsArrayBuffer(file)
            reader.onload = function() {
                let local_image_storage = JSON.parse(window.localStorage.getItem('local_image_storage'))
                if (!local_image_storage) {
                    local_image_storage = {}
                }

                local_image_storage[src] = file //reader.result
                console.log(local_image_storage)
                console.log(reader.result)
                window.localStorage.setItem('local_image_storage', JSON.stringify(local_image_storage))
            };*/

            if (window.textEditor.selection == null)
                Transforms.select(window.textEditor, {
                    anchor: { path: [0, 0], offset: 0 }, 
                    focus: { path: [0, 0], offset: 0 }
                })
            Transforms.insertNodes(window.textEditor, {
                'type': 'img',
                'src': src,
                'children': [{
                    'text': ''
                }]
            })
        }
        document.getElementById('img').value = ''
    }

    window.editor_style_link_clicked_enter = (event) => {
        //collapse_selection()
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
                    if (window.textEditor.selection == null)
                        Transforms.select(window.textEditor, {
                            anchor: { path: [0, 0], offset: 0 }, 
                            focus: { path: [0, 0], offset: 0 }
                        })
                    Transforms.insertNodes(window.textEditor, {
                        'type': 'img',
                        'src': input_href,
                        'children': [{
                            'text': ''
                        }]
                    })
                    break
            }

            window.editor_deselect()
            window.editor_style_link_close()
    }

    window.editor_style_link_clicked_key = (event) => {
        Transforms.setSelection(window.textEditor)
        if (event.key == 'Enter') {
            window.editor_style_link_clicked_enter(event)
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
                /*let {selection} = window.textEditor
                Transforms.select(window.textEditor, {
                    anchor: {
                        path: selection.anchor.path,
                        offset: 0
                    },
                    focus: {
                        path: window.selectedLinkLeaf.path,
                        offset: selection.anchor.path
                    }
                })*/
                Editor.removeMark(window.textEditor, 'href')
                Editor.addMark(window.textEditor, 'type', 'plain')
            }
        }

        
        window.editor_deselect()
        window.editor_style_link_close()
    }

    window.editor_style_link_close = () => {
        document.getElementsByClassName('content_style_buttons_link_input')[0].style.visibility = 'hidden'
        document.getElementsByClassName('content_style_buttons_link_input_abort')[0].style.visibility = 'hidden'
        document.getElementsByClassName('content_style_buttons_link_input')[0].getElementsByTagName('input')[0].value = ''
        window.linkButtonClickedType = ''
    }

    window.editor_deselect = () => {
        /*let marks = Editor.marks(window.textEditor)
        if (marks) {
            HistoryEditor.withoutSaving(window.textEditor, () => {
                Editor.addMark(window.textEditor, 'selected', false)
            })
            let { selection } = window.textEditor
            Transforms.mergeNodes(window.textEditor, {
                at: selection.anchor.path
            })
        }*/
        collapse_underline_selection()
        Transforms.deselect(window.textEditor)
    }

    window.editor_emojiPast = (e) => {
        window.editor_last_selection = window.textEditor.selection
        //if (editor_selection.anchor != editor_selection.focus)
            Transforms.insertNodes(window.textEditor, {
                type: 'plain',
                text: e.native
            })
        console.log(e)
    }

    function specifySelectedLinkLeaf(is_link=false) {
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

    window.editor_closeEmoji = () => {
        document.getElementsByTagName('em-emoji-picker')[0].removeAttribute('style')
    }

    function collapse_underline_selection() {
        //console.log('collapse selection')
        let marks = Editor.marks(window.textEditor)
        if (marks) {
            let is_selected = marks.selected
            //HistoryEditor.withoutSaving(window.textEditor, () => {
                Editor.removeMark(window.textEditor, 'selected')
                //Editor.addMark(window.textEditor, 'selected', false)
            //})
            /*let { selection } = window.textEditor
            if (selection.anchor != selection.focus &&marks.selected &&
                !marks.href && !marks.bold && !marks.cursive) {
                Transforms.mergeNodes(window.textEditor, {
                    at: selection.anchor.path,
                    match: (node, path) => {*/
                        /*console.log('here')
                        console.log(node, path, !node.href && !node.bold && !node.cursive && path.length === 2)
                        if (path.length === 2) {
                            let prev_node = window.textEditor.children[path[0]].children[path[1]-1]
                            console.log(prev_node)
                            if (prev_node != undefined)
                                return !prev_node.href && !prev_node.bold && !prev_node.cursive
                        }
                        return false*/
                        /*return true
                    }
                })
            }*/
        }
    }

    return (
        <>
        <Emoji 
            onMouseDown={event => {
                ReactEditor.focus(window.textEditor)
            }}
        />
        <Slate editor={window.textEditor} value={initialValue}>
            {/*<HoveringToolbar />*/}
            <Editable 
                renderElement={renderElement}
                renderLeaf = {renderLeaf}
                readOnly={!textReadOnly}
                style={{position: "static"}}
                //onSelect={() => window.forceUpdateToolbar()}
                onBlur={() => {
                    let selection = window.textEditor.selection
                    let marks = Editor.marks(window.textEditor)
                    if (marks && selection && !Range.isCollapsed(selection) && Editor.string(window.textEditor, selection) !== '') {
                        //HistoryEditor.withoutSaving(window.textEditor, () => {
                            //Editor.addMark(window.textEditor, 'selected', !is_selected)
                            Editor.addMark(window.textEditor, 'selected', true)
                        //})
                    }
                    //window.editor_closeEmoji()
                }}
                onFocus={() => {
                    collapse_underline_selection()
                    /*let marks = Editor.marks(window.textEditor)
                    if (marks) {
                        let is_selected = marks.selected
                        HistoryEditor.withoutSaving(window.textEditor, () => {
                            //Editor.addMark(window.textEditor, 'selected', !is_selected)
                            Editor.addMark(window.textEditor, 'selected', false)
                        })
                        let { selection } = window.textEditor
                        Transforms.mergeNodes(window.textEditor, {
                            at: selection.anchor.path
                        })
                    }*/
                }}
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
                    window.editor_closeEmoji()
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
                    window.editor_closeEmoji()
                }}
                /*onContextMenu={event => {
                    if (window.editMode) {
                        event.preventDefault()
                        Transforms.collapse(window.textEditor)
                        let container = document.getElementsByClassName('content_body')[0]
                        let leftOffset = container.getBoundingClientRect().left
                        let emojiWidth = document.getElementsByTagName('em-emoji-picker')[0].getBoundingClientRect().width
                        container = document.getElementsByClassName('content')[0]
                        let container_style = container.currentStyle || window.getComputedStyle(container);
                        let marginLeft = parseInt(container_style.marginLeft.replace('px', ''))
                        let style = {
                            left: event.clientX-leftOffset+marginLeft,
                            top: event.clientY + 20
                        }
                        if (style.left+emojiWidth + 20 > container.getBoundingClientRect().width)
                            style.left = container.getBoundingClientRect().width - emojiWidth + 20
                        document.getElementsByTagName('em-emoji-picker')[0].style.left = `${style.left}px`
                        document.getElementsByTagName('em-emoji-picker')[0].style.top = `${style.top}px`
                        document.getElementsByTagName('em-emoji-picker')[0].style.opacity = 1
                    }
                }}*/
            />
        </Slate>
        </>
    )
}



function RefreshTextText(text, link = '') {
    //window.textEditor.history = {undos: [], redos: []}
    //HistoryEditor.withoutSaving(window.textEditor, () => {
        let json_text = JSON.parse(text)
        window.textEditor.children.map(item => {
            Transforms.delete(window.textEditor, { at: [0] })
        })
        window.textEditor.children = json_text
        //Editor.normalize(window.textEditor)
    //})
}

function PullTextTextOut() {
    return window.textEditor.children
}

export {EditorTextComponent, RefreshTextText, PullTextTextOut}