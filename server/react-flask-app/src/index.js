import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import reportWebVitals from './reportWebVitals';

import { ErrorBoundary } from "react-error-boundary";
import {PullTitleTextOut} from './components/EditorTitle'
import {PullTextTextOut} from './components/EditorText'
import {PullLeadTextOut} from './components/EditorLead'

const onError = (error, info) => {
    let title = PullTitleTextOut()
    let text = JSON.stringify(PullTextTextOut())
    let logs = `${error}\n${info.componentStack}`.split('\n').join('%0A')
    fetch(`log_internal?logs=${logs}&post_title=${title}&post_text=${text}`)

    /*let opened_new = window.sessionStorage.getItem('opened_new')
    let processed_data = JSON.parse(window.sessionStorage.getItem('processed_data'))
    processed_data[opened_new].title = title
    processed_data[opened_new].lead = PullLeadTextOut()
    processed_data[opened_new].text = text
    window.sessionStorage.setItem('processed_data', JSON.stringify(processed_data))*/
};

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
        <ErrorBoundary fallback={<div>Что-то пошло не так<br/>Обновите страницу</div>}
                       onError={onError}
        >
            <App />
        </ErrorBoundary>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
