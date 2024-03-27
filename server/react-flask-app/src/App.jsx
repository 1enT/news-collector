import React, {useState, useEffect, useRef} from 'react'
import './App.css';
import News_content from './components/News_content'
import List_News from './components/List_news'
import CreateNewsButton from './components/CreateNewsButton'

import {EditorTitleComponent, RefreshTitleText} from './components/EditorTitle'
import {EditorTextComponent, RefreshTextText} from './components/EditorText'
import {EditorLeadComponent, RefreshLeadText} from './components/EditorLead'


function setContent(num, id) {
    if (window.editMode) {
        return 
    }

    let selected_new = JSON.parse(window.sessionStorage.getItem('processed_data'))[num]
    window.sessionStorage.setItem('opened_new', num)
    window.sessionStorage.setItem('opened_new_id', id)
    //window.setContentNews(selected_new)

    document.getElementsByClassName('content')[0].style.visibility = 'visible'
    document.getElementsByClassName('content_style_buttons')[0].style.visibility = 'visible'
    Array.prototype.slice.call(document.getElementsByTagName('li')).map(elem => elem.getElementsByClassName('news_title')[0].classList.remove('news_active'))
    document.getElementsByTagName('li')[num].getElementsByClassName('news_title')[0].classList.add('news_active')

    RefreshTitleText(selected_new.title)
    RefreshLeadText(selected_new.lead)
    RefreshTextText(selected_new.text, selected_new.link)

}

function clearContentSpace() {
    window.sessionStorage.removeItem('opened_new_id')

    document.getElementsByClassName('content')[0].style.visibility = 'hidden'
    document.getElementsByClassName('content_style_buttons')[0].style.visibility = 'hidden'
    Array.prototype.slice.call(document.getElementsByTagName('li')).map(elem => elem.getElementsByClassName('news_title')[0].classList.remove('news_active'))
}

function App() {
    const [news, setNewsList] = useState([{}, {}]);
    const [content, setContentNews] = useState({
        "hidden": "hidden", 
        "id": -1,
        "title": "", 
        "lead": "", 
        "text": "", 
        "link": ""
    });

    useEffect( () => {
        window.setNewsList = setNewsList
        window.setContentNews = setContentNews
        window.clearContentSpace = clearContentSpace
        window.editMode = false
        window.creatingNews = false
        //window.localStorage.removeItem('local_image_storage')
        window.local_image_storage = {}
        window.editor_last_selection = {
            anchor: {
                offset: 0,
                path: [0, 0]
            },
            focus: {
                offset: 0,
                path: [0, 0]
            }
        }

        document.title = "Собиратель новостей"
        window.sessionStorage.removeItem('opened_new')
        window.sessionStorage.removeItem('opened_new_id')
    }, [])

    useEffect( () => {
        let json_link = {
            type: 'p',
            children: [{
                type: 'a',
                href: "",
                text: ""
            }]
        }
        fetch('api?gotten_news=').then(res => res.json()).then(res => {
            console.log(res)
            let data = []
            for (let i = 0; i < res.length; i++) {
                let elem = res[i]
                if (elem.to_do == 'add') {
                    json_link.children[0].href = elem.content.link
                    json_link.children[0].text = elem.content.link
                    let json_text = JSON.parse(elem.content.text)
                    json_text.push(json_link)
                    elem.content.text = JSON.stringify(json_text)
                }

                data.push(elem.content)
            }
            data = data.sort((a, b) => b.id - a.id)

            window.sessionStorage.setItem('original_data', JSON.stringify(data))
            let processed_data = JSON.parse(window.sessionStorage.getItem("processed_data"))
            if (!processed_data || data != []) {
                window.sessionStorage.setItem('processed_data', JSON.stringify(data))
                setNewsList(data)
            } else {
                setNewsList(processed_data)
            }
        })
        setInterval(() => {
            let original_data = JSON.parse(window.sessionStorage.getItem('original_data'))
            let processed_data = JSON.parse(window.sessionStorage.getItem('processed_data'))

            let gotten_news = []
            for (let item of original_data) {
                if (!item.hasOwnProperty('is_custom'))
                    gotten_news.push(item.id)
            }
            gotten_news = gotten_news.join('.')

            fetch(`api?gotten_news=${gotten_news}`).then(res => res.json()).then(res => {
                if (res != []) {
                    let data = []
                    let to_delete = false
                    for (let elem of res) {
                        switch (elem.to_do) {
                        case 'add':
                            data.push(elem.content)
                            break
                        case 'delete':
                            if (!window.editMode) {
                                let index = -1
                                for (let i = 0; i < original_data.length; i++) {
                                    if (original_data[i].id == elem.id) {
                                        index = i
                                        break
                                    }
                                }
                                original_data.splice(index, 1)
                                processed_data.splice(index, 1)
                                to_delete = true
                            }
                            break
                        }
                    }
                    data = data.sort((a, b) => b.id - a.id)
                    //original_data = original_data.concat(data)
                    //processed_data = processed_data.concat(data)
                    original_data = data.concat(original_data)
                    processed_data = data.concat(processed_data)

                    window.sessionStorage.setItem('original_data', JSON.stringify(original_data))
                    window.sessionStorage.setItem('processed_data', JSON.stringify(processed_data))

                    setNewsList(processed_data)
                    if (to_delete)
                        window.clearContentSpace()
                }
            });
        }, 60000)
    }, []);
    
    return (
        <div className="container">
            <div className="list_news">
                <CreateNewsButton />
                <List_News news={news} news_change={setContent}/>
            </div>
            <div className="content_news">
                <News_content {...content}/>
            </div>
        </div>
    )
}

export default App;
