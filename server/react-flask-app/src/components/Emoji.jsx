import data from '@emoji-mart/data'
import Picker from '@emoji-mart/react'

import './Emoji.css'

const Emoji = (ref) => {
	return (
		<div className="emoji_picker">
		<Picker 
			data={data} 
			onEmojiSelect={window.editor_emojiPast} 
			locale="ru"
			emojiSize="20"
			categories={["people", "nature", "foods", "activity", "places", "objects", "symbols", "flags"]}
			emojiButtonColors="pink"
			perLine="7"
			previewPosition="none"
			searchPosition="none"
			/*onBlur={(event) => {
				console.log(1323213)
				document.getElementsByTagName('em-emoji-picker')[0].removeAttribute('style')
			}}*/
		/>
		</div>
	)
}

export default Emoji;