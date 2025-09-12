import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import { createBrowserRouter, RouterProvider } from 'react-router'
import { Toaster } from 'react-hot-toast'
import Chat from './components/Chat.jsx'
import ChatProvider from './store/ChatProvider.jsx'


let router = createBrowserRouter([
  { 
    path : "/",
    element : <App/>
  },
  {
    path : "/chat",
    element : <Chat/>
  },
  {
    path : "*",
    element : <h1>404 Not Found</h1>
  }
])


createRoot(document.getElementById('root')).render(
  <>
  <ChatProvider>
      <RouterProvider router={router}/>
    </ChatProvider>

    {/* to show notifications */}
    <Toaster position="top-center" reverseOrder={false} /> 
  </>
)
