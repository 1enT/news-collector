import React from 'react'
import News_title from './News_title'

function List_news({news, news_change}) {
	const rows = []
    //let news = JSON.parse(window.localStorage.getItem('news'))
    for (let i = 0; i < news.length; i++) {
        rows.push( <News_title key={i} num={i} id={news[i].id} news_change={news_change} source={news[i].source} time={news[i].time} title={news[i].title}/> )
    }
    return <ul>{rows}</ul>
}

export default List_news;