import React, { useState, useEffect } from 'react'
import { Editor, Transforms } from 'slate'
import { ReactEditor } from 'slate-react'
import './CreateNewsButton.css'

import { RefreshTitleText } from './EditorTitle'
import { RefreshLeadText } from './EditorLead'
import { RefreshTextText } from './EditorText'

function create_own_news() {
	if (window.editMode) {
		let r = window.confirm("Изменения не сохранены. Продолжить?")
		if (r) {
			window.do_edit_mode()
		} else {
			return
		}
	}
	window.creatingNews = true

    document.getElementsByClassName('content')[0].style.visibility = 'visible'
    document.getElementsByClassName('content_style_buttons')[0].style.visibility = 'visible'
    window.do_edit_mode()

    window.sessionStorage.removeItem('opened_new')
    window.sessionStorage.removeItem('opened_new_id')

	let original_data = JSON.parse(window.sessionStorage.getItem('original_data'))
    let processed_data = JSON.parse(window.sessionStorage.getItem('processed_data'))
    let id = -1
    original_data.map(item => {
    	if (id < item.id)
    		id = item.id
    })
    id += 100000
    let item = {
    	id: id,
    	time: "",
    	source: "Заметка",
    	title: "",
    	lead: "",
    	text: JSON.stringify([{
    		type: 'p',
    		children: [{
    			type: 'plain',
    			text: ''
    		}]
    	}]),
    	link: "",
    	is_custom: true
    }
    original_data.unshift(item)
    processed_data.unshift(item)
    window.sessionStorage.setItem('original_data', JSON.stringify(original_data))
    window.sessionStorage.setItem('processed_data', JSON.stringify(processed_data))
    window.sessionStorage.setItem('opened_new', 0)
    window.sessionStorage.setItem('opened_new_id', id)
    window.setNewsList(processed_data)

    Array.prototype.slice.call(document.getElementsByTagName('li')).map(elem => elem.getElementsByClassName('news_title')[0].classList.remove('news_active'))
    document.getElementsByTagName('li')[0].getElementsByClassName('news_title')[0].classList.add('news_active')

    RefreshTitleText(item.title)
    RefreshLeadText(item.lead)
    RefreshTextText(item.text)

	ReactEditor.focus(window.titleEditor)
	Transforms.select(window.titleEditor, {offset: 0, path:[0, 0]})
}

const CreateNewsButton = () => {
	return (
		<div className="create_news_button" onClick={create_own_news}>
			Создать пост
		</div>
	)
}

export default CreateNewsButton;