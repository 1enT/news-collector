import React, {useState, useEffect, useRef} from 'react'
import { Editor, Transforms } from 'slate'
import { ReactEditor } from 'slate-react'
import './News_content.css'

import {EditorTitleComponent, RefreshTitleText, PullTitleTextOut} from './EditorTitle'
import {EditorLeadComponent, RefreshLeadText, PullLeadTextOut} from './EditorLead'
import {EditorTextComponent, RefreshTextText, PullTextTextOut} from './EditorText'

function News_content(props) {
	window.styleTextSelected = styleTextSelected

	return (
        <div className="content" style={{visibility: props.hidden}}>
        	<div className="content_bar">
	        		<div className="content_style_buttons">
	        			<span className="content_edit_button" onMouseDown={editButtonClicked}></span>

	        			{/*<div>*/}
	        			<span className="content_style_buttons_bold" onClick={window.editor_style_bold_clicked} style={{visibility: "hidden"}}>B</span>
	        			<span className="content_style_buttons_italic" onClick={window.editor_style_italic_clicked} style={{visibility: "hidden"}}>I</span>
	        			<span className="content_style_buttons_underline" onClick={window.editor_style_underline_clicked} style={{visibility: "hidden"}}></span>
	        			<span className="content_style_buttons_quote" onClick={window.editor_style_quote_clicked} style={{visibility: "hidden"}}></span>
	        			<span className="content_style_buttons_link" onClick={window.editor_style_link_clicked} style={{visibility: "hidden"}}></span>
	        			<span className="content_style_buttons_image" onClick={window.editor_style_image_clicked} style={{visibility: "hidden"}}></span>

	        			<label htmlFor="img" className="content_style_buttons_image_upload" style={{visibility: "hidden"}}></label>
						<input name="img" type="file" className="content_style_buttons_image_upload_input" id="img" accept="image/pjpeg,image/jpeg,image/png" onInput={window.editor_image_upload}/>
						{/*</div>*/}
						{/*
	        			<input type="file" className="content_style_buttons_image_upload" onClick={window.editor_style_image_upload_clicked} style={{visibility: "hidden"}}></input>
	        			*/}
	        			<div className="content_style_buttons_link_input" style={{visibility: "hidden"}}>
	        				<input type="text" name="link_input" autoComplete="off" onKeyDown={window.editor_style_link_clicked_key}></input>
	        				<span className="content_style_buttons_link_input_enter" onClick={window.editor_style_link_clicked_enter}></span>
	        				<span className="content_style_buttons_link_input_abort" onClick={window.editor_style_link_clicked_abort}></span>
	        			</div>

	        			<span className="content_reset_button" onClick={resetButtonClicked}></span>
	        			<span className="content_decline_button" onClick={discardNews}></span>
	        			<span className="content_publish_button" onClick={publishButtonClicked}></span>
	        		</div>
        	</div>
			<div className="content_head">
	            <div className="content_title">
	            	<EditorTitleComponent />
	            </div>
	            <div className="content_lead">
	            	<EditorLeadComponent />
	            </div>
	        </div>
	        <div className="content_body">
	        	<EditorTextComponent />
	        </div>
	    </div>
	)
}

function styleTextSelected(type, is_styled) {
	switch (type) {
		case 'bold':
			if (is_styled) 
				document.getElementsByClassName('content_style_buttons_bold')[0].classList.add('content_style_buttons_active')
			else
				document.getElementsByClassName('content_style_buttons_bold')[0].classList.remove('content_style_buttons_active')
			break
		case 'cursive':
			if (is_styled)
				document.getElementsByClassName('content_style_buttons_italic')[0].classList.add('content_style_buttons_active')
			else
				document.getElementsByClassName('content_style_buttons_italic')[0].classList.remove('content_style_buttons_active')
			break
		case 'underline':
			if (is_styled)
				document.getElementsByClassName('content_style_buttons_underline')[0].classList.add('content_style_buttons_active')
			else
				document.getElementsByClassName('content_style_buttons_underline')[0].classList.remove('content_style_buttons_active')
			break
	}
}

function editButtonClicked() {
	if (!window.editMode) {
		document.getElementsByClassName('content_style_buttons_bold')[0].style.visibility = 'visible'
		document.getElementsByClassName('content_style_buttons_italic')[0].style.visibility = 'visible'
		document.getElementsByClassName('content_style_buttons_underline')[0].style.visibility = 'visible'
		document.getElementsByClassName('content_style_buttons_link')[0].style.visibility = 'visible'
		document.getElementsByClassName('content_style_buttons_quote')[0].style.visibility = 'visible'
		document.getElementsByClassName('content_style_buttons_image')[0].style.visibility = 'visible'
		document.getElementsByClassName('content_style_buttons_image_upload')[0].style.visibility = 'visible'

		document.getElementsByClassName('content_reset_button')[0].style.visibility = 'hidden'
		document.getElementsByClassName('content_decline_button')[0].style.visibility = 'hidden'
		document.getElementsByClassName('content_publish_button')[0].style.visibility = 'hidden'

		window.setTitleEditable(true)
		window.setLeadEditable(true)
		window.setTextEditable(true)

		window.onbeforeunload = () => {return false}
	} else {
		window.editor_deselect()
		window.editor_closeEmoji()
		saveNews()
	}

	window.editMode = !window.editMode
}

window.do_edit_mode = editButtonClicked

function saveNews() {
	closeEditUI()

	let opened_new = window.sessionStorage.getItem('opened_new')
	let processed_data = JSON.parse(window.sessionStorage.getItem('processed_data'))
	processed_data[opened_new].title = PullTitleTextOut()
	processed_data[opened_new].lead = PullLeadTextOut()
	processed_data[opened_new].text = JSON.stringify(PullTextTextOut())

	window.sessionStorage.setItem('processed_data', JSON.stringify(processed_data))
	window.setNewsList(processed_data)

	window.onbeforeunload = undefined
}

function resetButtonClicked() {
	closeEditUI()

	let opened_new = window.sessionStorage.getItem('opened_new')
	let processed_data = JSON.parse(window.sessionStorage.getItem('processed_data'))
	let original_data = JSON.parse(window.sessionStorage.getItem('original_data'))
	processed_data[opened_new].title = original_data[opened_new].title
	processed_data[opened_new].lead = original_data[opened_new].lead
	processed_data[opened_new].text = original_data[opened_new].text

	window.sessionStorage.setItem('processed_data', JSON.stringify(processed_data))
	
	RefreshTitleText(original_data[opened_new].title)
	RefreshLeadText(original_data[opened_new].lead)
	RefreshTextText(original_data[opened_new].text, original_data[opened_new].link)

	window.setNewsList(processed_data)

	window.onbeforeunload = undefined
}

function publishButtonClicked() {
	closeEditUI()

	let opened_new = window.sessionStorage.getItem('opened_new')
	let new_to_publish = JSON.parse(window.sessionStorage.getItem('processed_data'))[opened_new]

	let content = []
    let is_there_img = false
    let img_array = []
    let img_local_array = []
    window.textEditor.children.map(tag => {
    	let inner_content = []
    	if (tag.type == 'p') {
	        tag.children.map(item => {
	        	let shilded_item_text = shieldText(item.text)
	        	if (item.type == 'a' && shilded_item_text != '') {
	        		let shilded_item_href = shieldText(item.href)
	        		inner_content.push(`[${shilded_item_text.replaceAll('*', '\\*')}](${shilded_item_href})`)
	        	}
	        	else if (item.bold) {
	        		/*let star_pos = shilded_item_text.indexOf('*')
	        		if (star_pos + 1) {
	        			inner_content.push(`*${shilded_item_text.replaceAll('*', '\\*')}*`)
	        		} else {
	        			inner_content.push(`*${shilded_item_text}*`)
	        		}*/
	        		inner_content.push(`*${shilded_item_text.replaceAll('*', '\\*')}*`)
	        	}
	        	else if (item.cursive) {
	        		inner_content.push(`_${shilded_item_text.replaceAll('*', '\\*')}_`)
	        	}
	        	else {
	        		inner_content.push(`${shilded_item_text.replaceAll('*', '\\*')}`)
	        	}
	        })
	        inner_content = inner_content.join('')
	        if (inner_content != '')
	        	content.push(inner_content)
	    }
	    else if (tag.type == 'quote') {
	    	tag.children.map(item => {
	    		let shilded_item_text = shieldText(item.text)
	        	if (item.bold) {
	        		inner_content.push(`*${shilded_item_text.replaceAll('*', '\\*')}*`)
	        	}
	        	else if (item.cursive) {
	        		inner_content.push(`_${shilded_item_text.replaceAll('*', '\\*')}_`)
	        	}
	        	else {
	        		inner_content.push(`${shilded_item_text.replaceAll('*', '\\*')}`)
	        	}
	        })
	        inner_content = inner_content.join('')
	        inner_content = '> ' + inner_content
	        if (inner_content != '')
	        	content.push(inner_content)
	    }
	    else if (tag.type == 'img') {
        	is_there_img = true
        	/*let src = new URL(tag.src)
        	let media = ''
        	if (src.protocol == 'blob:') {
        		let this_img = window.local_image_storage[tag.src]
        		img_local_array.push(this_img)
        	} else {*/
        		let media = tag.src.replaceAll(' ', '%20')
	        	img_array.push({
	        		type: "photo",
	        		media: media
	        	})
	        //}
	    }
    })
    let formData = new FormData()
    if (img_local_array.length > 0) {
        is_there_img = true
	    img_local_array.forEach( (image, index) => {
	    	console.log(`image${index}`, image)
	    	formData.append(`image${index}`, image)
	    })
	}
	let opened_new_id = window.sessionStorage.getItem('opened_new_id')
	formData.append('news_id', opened_new_id)
	formData.append('is_custom', new_to_publish.hasOwnProperty('is_custom'))

    content = content.join('%0A%0A')
    //content = shieldText(content)

    let post_title = getShieldingTitle(new_to_publish.title)
    post_title = shieldText(post_title)

	let lead = ''
	if (new_to_publish.lead.replaceAll(' ', '').replaceAll('\n', '') != '') {
		lead = `${shieldText(new_to_publish.lead)}%0A%0A`
	}
	let post_body = `${lead}${content}`
	post_body = post_body.replaceAll('%0A', '\n')
	let post = `${post_title}%0A%0A${post_body}`.replaceAll('%0A', '\n')
	
	if (is_there_img && post.length > 1024 || post.length > 4096) {
		console.log(post)
		alert("Слишком длинный пост. Без картинок макс. 4096 символов, с картинками макс. 1024 символа")
		return
	}
	if (img_array.length > 10) {
		alert("Слишком много картинок. Максимум 10 картинок")
		return
	}
	
	if (!is_there_img) {
		//formData.append('message', post)
		formData.append('message_title', post_title)
		formData.append('message_body', post_body)
		fetch('send_message', {
			method: 'post',
			body: formData
			/*body: JSON.stringify({
				message: post
			})*/
		})
	} else if (img_array.length + img_local_array.length == 1) {
		//formData.append('caption', post)
		formData.append('caption_title', post_title)
		formData.append('caption_body', post_body)
		formData.append('photo', img_array.length > 0 ? img_array[0].media : null)
		fetch('send_photo', {
			method: 'post',
			body: formData
			/*body: JSON.stringify({
				caption: post,
				photo: img_array.length > 0 ? img_array[0].media : null,
				local_photo: img_local_array.length > 0 ? formData : null
			})*/
		})
	} else {
		img_array = img_array.map((x) => x.media)
		//formData.append('caption', post)
		formData.append('caption_title', post_title)
		formData.append('caption_body', post_body)
		formData.append('media', img_array.length > 0 ? JSON.stringify(img_array) : null)
		fetch('send_media_group', {
			method: 'post',
			body: formData
			/*body: JSON.stringify({
				caption: post,
				media: img_array,
				local_media: img_local_array.length > 0 ? formData : null
			})*/
		})
	}


    removeNewsAfterPublishing()
}

async function getBlob(src) {
	let reader = new FileReader()
    let fetch_blob = await fetch(src)
    let blob = await fetch_blob.blob()
    console.log(blob)
    return blob
}

function removeNewsFromUI(opened_new) {
	let processed_data = JSON.parse(window.sessionStorage.getItem('processed_data'))
	let original_data = JSON.parse(window.sessionStorage.getItem('original_data'))

	processed_data.splice(opened_new, 1)
	original_data.splice(opened_new, 1)

	window.sessionStorage.setItem('processed_data', JSON.stringify(processed_data))
	window.sessionStorage.setItem('original_data', JSON.stringify(original_data))
	window.setNewsList(processed_data)
	window.clearContentSpace()
	window.sessionStorage.removeItem('opened_new')
    window.sessionStorage.removeItem('opened_new_id')
}

function removeNewsAfterPublishing() {
	let opened_new = window.sessionStorage.getItem('opened_new')
	removeNewsFromUI(opened_new)
}

function discardNews() {
	let opened_new = window.sessionStorage.getItem('opened_new')
	let opened_new_id = window.sessionStorage.getItem('opened_new_id')
	let processed_data = JSON.parse(window.sessionStorage.getItem('processed_data'))

	if (processed_data[opened_new].hasOwnProperty('is_custom')) {
		removeNewsFromUI(opened_new)
	} else {
		fetch(`/dispose?num=${opened_new_id}&is_custom=${processed_data[opened_new].hasOwnProperty('is_custom')}`).then(res => res.json()).then(data => {
			removeNewsFromUI(opened_new)
		})
	}
}

function closeEditUI() {
	window.editor_style_link_close()

	document.getElementsByClassName('content_style_buttons_bold')[0].style.visibility = 'hidden'
	document.getElementsByClassName('content_style_buttons_italic')[0].style.visibility = 'hidden'
	document.getElementsByClassName('content_style_buttons_underline')[0].style.visibility = 'hidden'
	document.getElementsByClassName('content_style_buttons_quote')[0].style.visibility = 'hidden'
	document.getElementsByClassName('content_style_buttons_link')[0].style.visibility = 'hidden'
	document.getElementsByClassName('content_style_buttons_image')[0].style.visibility = 'hidden'
	document.getElementsByClassName('content_style_buttons_image_upload')[0].style.visibility = 'hidden'

	/*document.getElementsByClassName('content_reset_button')[0].style.visibility = 'visible'
	document.getElementsByClassName('content_decline_button')[0].style.visibility = 'visible'
	document.getElementsByClassName('content_publish_button')[0].style.visibility = 'visible'*/
	document.getElementsByClassName('content_reset_button')[0].style.removeProperty('visibility')
	document.getElementsByClassName('content_decline_button')[0].style.removeProperty('visibility')
	document.getElementsByClassName('content_publish_button')[0].style.removeProperty('visibility')

	window.setTitleEditable(false)
	window.setLeadEditable(false)
	window.setTextEditable(false)

	//window.editMode = false
}

function getShieldingTitle(raw_title) {
	let post_title = ''
    let star_pos = raw_title.indexOf('*')
    let title = raw_title.replaceAll('*', '')
    switch (star_pos) {
    	case -1:
    		post_title = `*${title}*`
    		break
    	case 0:
    		post_title = `\\**${title}*`
    		break
    	case raw_title.length - 1:
    		post_title = `*${title}*\\*`
    		break
    	default:
    		post_title = `*${title}*`
    		break
    }
    return post_title
}

function shieldText(raw_text) {
	let text = ''
    /*text = raw_text.replaceAll('#', '%23')
	text = text.replaceAll('&', '%26')
	text = text.replaceAll('?', '%3F')
	text = text.replaceAll('@', '%40')*/
	text = raw_text.replaceAll('_', '\\_')
	text = text.replaceAll('[', '\\[')
	text = text.replaceAll(']', '\\]')
	text = text.replaceAll('(', '\\(')
	text = text.replaceAll(')', '\\)')
	text = text.replaceAll('~', '\\~')
	text = text.replaceAll('`', '\\`')
	text = text.replaceAll('>', '\\>')
	text = text.replaceAll('#', '\\#')
	text = text.replaceAll('+', '\\+')
	text = text.replaceAll('-', '\\-')
	text = text.replaceAll('=', '\\=')
	text = text.replaceAll('|', '\\|')
	text = text.replaceAll('{', '\\{')
	text = text.replaceAll('}', '\\}')
	text = text.replaceAll('.', '\\.')
	text = text.replaceAll('!', '\\!')
	
	return text
}

function log(logs, error = false) {
	fetch(`log_telegram?logs=${logs}&error=${+error}`)
}

export default News_content;