import React from 'react'
import './News_title.css'

function News_title({num, id, news_change, source, time, title}) {
    return (
		<li className="news" onClick={() => news_change(num, id)} num={num} id={id}>
            <table className="news_body">
                <tbody>
                    <tr>
                        <td className="news_head" valign="top">
                            <span className="news_source">{source}</span>
                            <div className="news_date">
                                <span className="news_time_hour">{time}</span>
                            </div>
                        </td>
                        <td className="news_title" valign="top">
                            {/*console.log(title)*/}
                            {title}
                        </td>
                    </tr>
                </tbody>
            </table>
        </li>
	)
}

export default News_title;