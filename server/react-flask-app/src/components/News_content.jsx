import React, {useState, useEffect} from 'react'
import './News_content.css'

import SlateEditorComponent from './SlateEditorComponent'
import {EditorTitleComponent, RefreshTitleText, PullTitleTextOut} from './EditorTitle'
/*import {EditorInnerLeadComponent, RefreshInnerLeadText} from './EditorInnerLead'
import {EditorOutterLeadComponent, RefreshOutterLeadText, fillSpace} from './EditorOutterLead'*/
import {EditorLeadComponent, RefreshLeadText, PullLeadTextOut} from './EditorLead'
import {EditorTextComponent, RefreshTextText, PullTextTextOut} from './EditorText'

{/*<SlateEditorComponentTest />*/}
function News_content(props) {
	return (
        <div className="content" style={{visibility: props.hidden}}>
        	<div className="content_bar">
	        		<div className="content_edit_button" onClick={editButtonClicked}></div>
	        		<div className="content_buttons">
		        		<div className="content_save_button" onClick={saveButtonClicked} style={{visibility: "hidden"}}>Сохранить</div>
		        		<div className="content_reset_button" onClick={resetButtonClicked} style={{visibility: "hidden"}}>Откатить изменения</div>
		        		<div className="content_decline_button" onClick={removeNews}>Удалить</div>
		        		<div className="content_publish_button" onClick={publishButtonClicked}>Опубликовать</div>
	        		</div>
        	</div>
			<div className="content_head">
	            <div className="content_title">
	            	{/*{props.title}*/}
	            	<EditorTitleComponent />
	            </div>
	            {/*<div className="content_inner_lead">
	            	<EditorInnerLeadComponent />
	            </div>*/}
	            <div className="content_lead">
	                {/*{props.inner_lead}*/}
	            	<EditorLeadComponent />
	            </div>
	        </div>
	        <div className="content_body">
	        	{/*<div className="content_lead">
	        		<EditorOutterLeadComponent />
	        	</div>*/}
	        	{/*<div dangerouslySetInnerHTML={{__html: props.text}}></div>*/}
	        	<EditorTextComponent />
	            <p className="content_link">
	                <a href={props.link} target="_blank" rel="noopener noreferrer">{props.link}</a>
	            </p>
	        </div>
	    </div>
	)
}

function editButtonClicked() {
	document.getElementsByClassName('content_edit_button')[0].style.visibility = 'hidden'
	document.getElementsByClassName('content_edit_button')[0].style.position = 'absolute'
	document.getElementsByClassName('content_buttons')[0].style.position = 'static'
	document.getElementsByClassName('content_save_button')[0].style.visibility = 'visible'
	document.getElementsByClassName('content_reset_button')[0].style.visibility = 'visible'
	document.getElementsByClassName('content_publish_button')[0].style.visibility = 'hidden'

	window.setTitleEditable(true)
	window.setLeadEditable(true)
	/*window.setInnerLeadEditable(true)
	window.setOutterLeadEditable(true)*/

	window.editMode = true

	//fillSpace()

	window.onbeforeunload = () => {return false}
}

function resetButtonClicked() {
	closeUI()

	let opened_new = window.localStorage.getItem('opened_new')
	let processed_data = JSON.parse(window.localStorage.getItem('processed_data'))
	let original_data = JSON.parse(window.localStorage.getItem('original_data'))
	processed_data[opened_new].title = original_data[opened_new].title
	processed_data[opened_new].lead = original_data[opened_new].lead
	
	RefreshTitleText(original_data[opened_new].title)
	RefreshLeadText(original_data[opened_new].lead)
	/*RefreshInnerLeadText(data.inner_lead)
	RefreshOutterLeadText(data.outter_lead)*/
	window.setNewsList(original_data)

	window.onbeforeunload = undefined
}

function saveButtonClicked() {
	closeUI()

	let opened_new = window.localStorage.getItem('opened_new')
	let processed_data = JSON.parse(window.localStorage.getItem('processed_data'))
	processed_data[opened_new].title = PullTitleTextOut()
	processed_data[opened_new].lead = PullLeadTextOut()

	window.localStorage.setItem('processed_data', JSON.stringify(processed_data))
	window.setNewsList(processed_data)

	window.onbeforeunload = undefined
}

function publishButtonClicked() {
	let opened_new = window.localStorage.getItem('opened_new')
	let new_to_publish = JSON.parse(window.localStorage.getItem('processed_data'))[opened_new]

	let message_title = `*${new_to_publish.title}*`
	//let message_body = `${new_to_publish.lead}%0A%0A${new_to_publish.text}%0A%0A${new_to_publish.link}`
	let message_body = `${new_to_publish.lead}%0A%0A${new_to_publish.link}`
	let message = `${message_title}%0A%0A${message_body}`
	fetch(`https://api.telegram.org/bot6012282382:AAG4RclgeGuSxpadCw6MiQQPH4aGblF5LVI/sendMessage?chat_id=@tatartestnews&text=${message}&parse_mode=markdown&disable_web_page_preview=true`).then(res => {
        console.log(res)
    })

    removeNews()
}

function removeNews() {
	closeUI(true)

	let opened_new = window.localStorage.getItem('opened_new')
	let opened_new_id = window.localStorage.getItem('opened_new_id')

	fetch(`/dispose?num=${opened_new_id}`).then(res => res.json()).then(data => {
		let processed_data = JSON.parse(window.localStorage.getItem('processed_data'))
		let original_data = JSON.parse(window.localStorage.getItem('original_data'))

		processed_data.splice(opened_new, 1)
		original_data.splice(opened_new, 1)

		window.localStorage.setItem('processed_data', JSON.stringify(processed_data))
		window.localStorage.setItem('original_data', JSON.stringify(original_data))
		window.setNewsList(processed_data)
		window.clearContentSpace()
	})
}

function closeUI(total = false) {
	document.getElementsByClassName('content_edit_button')[0].style.visibility = 'visible'
	document.getElementsByClassName('content_edit_button')[0].style.position = 'static'
	document.getElementsByClassName('content_buttons')[0].style.position = 'absolute'
	document.getElementsByClassName('content_save_button')[0].style.visibility = 'hidden'
	document.getElementsByClassName('content_reset_button')[0].style.visibility = 'hidden'
	document.getElementsByClassName('content_publish_button')[0].style.visibility = 'visible'

	if (total) {
		document.getElementsByClassName('content_edit_button')[0].style.removeProperty('visibility')
		document.getElementsByClassName('content_publish_button')[0].style.removeProperty('visibility')
	}

	window.setTitleEditable(false)
	window.setLeadEditable(false)
	/*window.setInnerLeadEditable(false)
	window.setOutterLeadEditable(false)*/

	window.editMode = false
}

export default News_content;