import React from 'react'
import ReactDOM from 'react-dom/client'
import { Widget } from './components/chat/Widget'
import './index.css'

// 1. We create a container div and append it to the body
const containerId = 'digital-twin-widget-container'
let container = document.getElementById(containerId)

if (!container) {
  container = document.createElement('div')
  container.id = containerId
  document.body.appendChild(container)
}

// 2. We render the React app into that container
ReactDOM.createRoot(container).render(
  <React.StrictMode>
    <Widget />
  </React.StrictMode>,
)
