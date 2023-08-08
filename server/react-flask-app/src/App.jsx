import React, {useState, useEffect} from 'react'
import './App.css';
import News_content from './components/News_content'
import List_News from './components/List_news'

import {EditorTitleComponent, RefreshTitleText} from './components/EditorTitle'
/*import {EditorInnerLeadComponent, RefreshInnerLeadText} from './components/EditorInnerLead'
import {EditorOutterLeadComponent, RefreshOutterLeadText} from './components/EditorOutterLead'*/
import {EditorTextComponent, RefreshTextText} from './components/EditorText'
import {EditorLeadComponent, RefreshLeadText} from './components/EditorLead'

function App() {
    /*, {
        chat_id: "@tatartestnews",
        text: 123
    }*/
    /*let mes = "*3213*%0A%0A321"
    fetch(`https://api.telegram.org/bot6012282382:AAG4RclgeGuSxpadCw6MiQQPH4aGblF5LVI/sendMessage?chat_id=@tatartestnews&text=${mes}&parse_mode=markdown`).then(res => {
        console.log(res)
    })*/
    /*window.addEventListener("unload", function() {
        window.setTitleEditable(false)
        window.setInnerLeadEditable(false)
        window.setOutterLeadEditable(false)
    });*/

    const [news, setNewsList] = useState([{}, {}]);
    window.setNewsList = setNewsList
    const [content, setContentNews] = useState({"hidden": "hidden", "id": -1,
        "title": "", 
        "lead": "", "text": "", "link": ""});
    //window.localStorage.setItem('content', JSON.stringify(content))

    window.editMode = false

    useEffect( () => {
        fetch('api').then(res => res.json()).then(data => {
            window.localStorage.setItem('original_data', JSON.stringify(data))
            window.localStorage.setItem('processed_data', JSON.stringify(data))
            setNewsList(data)
        })
        setInterval(() => {
            fetch('api').then(res => res.json()).then(data => {
                let original_data = JSON.parse(window.localStorage.getItem('original_data'))
                let processed_data = JSON.parse(window.localStorage.getItem('processed_data'))

                let len_outdated_news = original_data.length
                let len_fresh_news = data.length

                if (len_fresh_news > len_outdated_news) {
                    let sliced_data = data.slice(len_outdated_news)

                    original_data = original_data.concat(sliced_data)
                    processed_data = processed_data.concat(sliced_data)

                    window.localStorage.setItem('original_data', JSON.stringify(original_data))
                    window.localStorage.setItem('processed_data', JSON.stringify(processed_data))

                    setNewsList(processed_data)
                }
            });
        }, 15000)
    }, []);

    function setContent(num, id) {
        if (window.editMode) {
            return 
        }
        /*let data = JSON.parse(window.localStorage.getItem('data'))[num]
        window.localStorage.setItem('opened_new', num)
        setContentNews(data)*/

        let selected_new = JSON.parse(window.localStorage.getItem('processed_data'))[num]
        window.localStorage.setItem('opened_new', num)
        window.localStorage.setItem('opened_new_id', id)
        setContentNews(selected_new)

        document.getElementsByClassName('content')[0].style.visibility = 'visible'
        Array.prototype.slice.call(document.getElementsByTagName('li')).map(elem => elem.getElementsByClassName('news_title')[0].classList.remove('news_active'))
        document.getElementsByTagName('li')[num].getElementsByClassName('news_title')[0].classList.add('news_active')

        RefreshTitleText(selected_new.title)
        /*RefreshInnerLeadText(data.inner_lead)
        RefreshOutterLeadText(data.outter_lead)*/
        RefreshLeadText(selected_new.lead)
        RefreshTextText(selected_new.text)

    }

    function clearContentSpace() {
        window.localStorage.removeItem('opened_new_id')

        document.getElementsByClassName('content')[0].style.visibility = 'hidden'
        Array.prototype.slice.call(document.getElementsByTagName('li')).map(elem => elem.getElementsByClassName('news_title')[0].classList.remove('news_active'))

        /*RefreshTitleText('')
        RefreshLeadText('')
        RefreshTextText('')*/
    }
    window.clearContentSpace = clearContentSpace
    
    return (
        <div className="container">
            <div className="list_news">
                <List_News news={news} news_change={setContent}/>
            </div>
            <div className="content_news">
                <News_content {...content}/>
                {/*<AlloyEditorComponent container="editable" />*/}
                {/*<SlateEditorComponentTest content={content} />*/}
            </div>
        </div>
    )
}

export default App;
