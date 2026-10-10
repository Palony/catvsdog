import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import heroImg from './assets/hero.png'
import './App.css'

function App() {

  const [selectedFile, setSelectedFile] = useState(null)
  const [url, setUrl] = useState(null)
  const [className, setClassname] = useState(null)



  const handleImageChange = async (event) => {
    const file = event.target.files[0];

    if(file){
      setSelectedFile(file)

      const filePreview = URL.createObjectURL(file)
      setUrl(filePreview)
      sendAnimal(file)

    }
  }

  const sendAnimal = async (fileToSend) => {
    const url = "http://127.0.0.1:8000/animal"

    const formdata = new FormData()

    formdata.append('file', fileToSend)

    const response = await fetch(url, {
      method: 'POST',
      body: formdata
    })

    const data = await response.json()
    console.log(data)
    setClassname(data.class)
  }

  return (
    <>
      <div className='mainPanel'>
        <p>Wprowadź zwierzaka</p>
        <div className='imagePanel'>
          {url && <img src={url} className="selectedImg"></img>}
        </div>
        {className && <p>To jest {className}</p>}
        <input type='file' accept='image/*' onChange = {handleImageChange} />
      </div>
    </>
  )
}

export default App
