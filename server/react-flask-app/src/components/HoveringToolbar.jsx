import React, { useRef, useEffect, useReducer } from 'react'
import { useSlate, useFocused } from 'slate-react'
import { Editor, Range, Transforms } from 'slate'

import './HoveringToolbar.css'

const HoveringToolbar = () => {
	const ref = useRef()
	const editor = window.textEditor
	const inFocus = useFocused()

	const [, forceUpdate] = useReducer(x => x + 1, 0);
	window.forceUpdateToolbar = forceUpdate
	
	console.log(1)
	useEffect(() => {
		/*Transforms.select(window.textEditor, {
    "anchor": {
        "path": [
            0,
            0
        ],
        "offset": 15
    },
    "focus": {
        "path": [
            0,
            0
        ],
        "offset": 23
    }
})*/
	    const el = ref.current
	    const { selection } = editor

	    if (!el) {
	      return
	    }

	    //console.log(selection, inFocus, Range.isCollapsed(selection), Editor.string(editor, selection) === '')
	    if (
	      !selection ||
	      !inFocus ||
	      Range.isCollapsed(selection) ||
	      Editor.string(editor, selection) === ''
	    ) {
	      el.removeAttribute('style')
	      return
	    }

		let container = document.getElementsByClassName('content_body')[0]
		const container_rect_left = container.getBoundingClientRect().left
		let container_style = container.currentStyle || window.getComputedStyle(container);
		const paddingLeft = parseInt(container_style.paddingLeft.replace('px', ''))

		container = document.getElementsByClassName('content')[0]
		container_style = container.currentStyle || window.getComputedStyle(container);
		const marginLeft = parseInt(container_style.marginLeft.replace('px', ''))
		const container_rect_width = container.getBoundingClientRect().width + 2*marginLeft

		const container_rect_top = container.getBoundingClientRect().top

	    const domSelection = window.getSelection()
	    const domRange = domSelection.getRangeAt(0)
	    const rect = domRange.getBoundingClientRect()

	    const LeftOffset = - container_rect_left + marginLeft //+ paddingLeft
	    const TopOffset = - container_rect_top

	    const style ={
	    	top: rect.top + TopOffset - el.offsetHeight,  // window.pageYOffset
	    	left: rect.left + LeftOffset - el.offsetWidth / 2 + rect.width / 2  // window.pageXOffset
	    }
	    if (style.left < 10)
	    	style.left = 10
	    else if (style.left + el.offsetWidth > container_rect_width)
	    	style.left = container_rect_width - el.offsetWidth -20
	    el.style.opacity = '1'
	    el.style.top = `${style.top}px`
	    el.style.left = `${style.left}px`
	    console.log(rect.left, LeftOffset, el.offsetWidth, rect.width)
	    //console.log(rect)
	})


	return (
		<div 
			ref={ref}
			className="HoveringToolbar"
			onMouseDown={e => {
				e.preventDefault()
			}}
		>
			123dfdfd
			<span className="spannn" onClick={() => { alert(1) }}>Span</span>
			<input className="inputtt" onFocus={e => {
				Transforms.select(window.textEditor, window.lastSelection)
				//window.textEditor.selection = window.lastSelection
				e.preventDefault()
			}}></input>
		</div>
	)
}

export default HoveringToolbar;