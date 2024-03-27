import React from 'react'
import News_title from './News_title'

function List_news({news, news_change}) {
    const options = {
        year: "numeric",
        month: "2-digit",
        day: "numeric",
        hour: "numeric",
        minute: "numeric"
    }
	const rows = []
    for (let i = 0; i < news.length; i++) {
        let time = undefined
        if (!!news[i].time)
            time = new Intl.DateTimeFormat('ru', options).format(new Date(news[i].time))
        
        rows.push( <News_title key={i} num={i} id={news[i].id} news_change={news_change} source={news[i].source} time={time} title={news[i].title}/> )
    }
    return <ul>{rows}</ul>
}

export default List_news;