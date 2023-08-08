import React, {useState, useEffect} from 'react'
import './App.css';
import News_content from './components/News_content'
import List_News from './components/List_news'

import {EditorTitleComponent, RefreshTitleText} from './components/EditorTitle'
import {EditorInnerLeadComponent, RefreshInnerLeadText} from './components/EditorInnerLead'
import {EditorOutterLeadComponent, RefreshOutterLeadText} from './components/EditorOutterLead'
import {EditorTextComponent, RefreshTextText} from './components/EditorText'

function App() {
    /*window.addEventListener("unload", function() {
        window.setTitleEditable(false)
        window.setInnerLeadEditable(false)
        window.setOutterLeadEditable(false)
    });*/

    const [news, setNewsList] = useState([{}, {}]);
    const [content, setContentNews] = useState({"hidden": "hidden", 
        "title": "", 
        "inner_lead": "", "outter_lead": "", "text": "", "link": ""});
    window.localStorage.setItem('content', JSON.stringify(content))

    window.editMode = false

    useEffect( () => {
        fetch('api').then(res => res.json()).then(data => {
                setNewsList(data)
                window.localStorage.setItem('data', JSON.stringify(data))
                window.edittedNews = []
        })
        setInterval(() => {
            fetch('api').then(res => res.json()).then(data => {
                setNewsList(data)
                window.localStorage.setItem('data', JSON.stringify(data))
            });
        }, 15000)
    }, []);

    function setContent(num) {
        if (window.editMode) {
            return 
        }
        let data = JSON.parse(window.localStorage.getItem('data'))[num]
        window.localStorage.setItem('news_num', num)
        setContentNews(data)

        document.getElementsByClassName('content')[0].style.visibility = 'visible'
        Array.prototype.slice.call(document.getElementsByTagName('li')).map(elem => elem.getElementsByClassName('news_title')[0].classList.remove('news_active'))
        document.getElementsByTagName('li')[num].getElementsByClassName('news_title')[0].classList.add('news_active')

        RefreshTitleText(data.title)
        RefreshInnerLeadText(data.inner_lead)
        RefreshOutterLeadText(data.outter_lead)
        RefreshTextText(data.text)

        if (window.edittedNews[num] == undefined) {
            window.edittedNews[num] = data
        }
    }
    
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
