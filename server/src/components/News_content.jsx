import React from 'react'
import './News_content.css'

import SlateEditorComponent from './SlateEditorComponent'
import {EditorTitleComponent, RefreshTitleText} from './EditorTitle'
import {EditorInnerLeadComponent, RefreshInnerLeadText} from './EditorInnerLead'
import {EditorOutterLeadComponent, RefreshOutterLeadText, fillSpace} from './EditorOutterLead'
import {EditorTextComponent, RefreshTextText} from './EditorText'

{/*<SlateEditorComponentTest />*/}
function News_content(props) {
	return (
        <div className="content" style={{visibility: props.hidden}}>
        	<div className="content_bar">
	        		<div className="content_edit_button" onClick={editButtonClicked}></div>
	        		<div className="content_buttons">
		        		<div className="content_save_button" onClick={saveButtonClicked} style={{visibility: "hidden"}}>Сохранить</div>
		        		<div className="content_reset_button" onClick={declineButtonClicked} style={{visibility: "hidden"}}>Откатить изменения</div>
		        		<div className="content_decline_button">Удалить</div>
		        		<div className="content_publish_button">Опубликовать</div>
	        		</div>
        	</div>
			<div className="content_head">
	            <div className="content_title">
	            	{/*{props.title}*/}
	            	<EditorTitleComponent />
	            </div>
	            <div className="content_inner_lead">
	                {/*{props.inner_lead}*/}
	            	<EditorInnerLeadComponent />
	            </div>
	        </div>
	        <div className="content_body">
	        	<div className="content_lead">
	        		{/*{props.outter_lead}*/}
	        		<EditorOutterLeadComponent />
	        	</div>
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

	window.setTitleEditable(true)
	window.setInnerLeadEditable(true)
	window.setOutterLeadEditable(true)

	window.editMode = true

	//fillSpace()

	window.onbeforeunload = () => {return false}
}

function declineButtonClicked() {
	closeUI()

	let news_num = window.localStorage.getItem('news_num')
	let data = JSON.parse(window.localStorage.getItem('data'))[news_num]
	
	RefreshTitleText(data.title)
	RefreshInnerLeadText(data.inner_lead)
	RefreshOutterLeadText(data.outter_lead)

	window.onbeforeunload = undefined
}

function saveButtonClicked() {
	closeUI()

	window.onbeforeunload = undefined
}

function closeUI() {
	document.getElementsByClassName('content_edit_button')[0].style.visibility = 'visible'
	document.getElementsByClassName('content_edit_button')[0].style.position = 'static'
	document.getElementsByClassName('content_buttons')[0].style.position = 'absolute'
	document.getElementsByClassName('content_save_button')[0].style.visibility = 'hidden'
	document.getElementsByClassName('content_reset_button')[0].style.visibility = 'hidden'

	window.setTitleEditable(false)
	window.setInnerLeadEditable(false)
	window.setOutterLeadEditable(false)

	window.editMode = false
}

export default News_content;