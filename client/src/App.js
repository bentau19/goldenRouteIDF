
import {useEffect, useState } from 'react';
import axios from 'axios';
import './App.css';
function App() {
  // React component
const [opearentionable, setOpearentionable] = useState(false)
const [inputValue, setInputValue] = useState("");
const [message, setMessage] = useState("");
const [isFirst, setFlag] = useState(false);
const initialDate = new Date('2023-01-01');
const [selectedDate, setSelectedDate] = useState(initialDate);
const [dates, setDates] = useState("loading");

useEffect(() => weatherCheck,[]);

const handleInputChange = (event) => {
    setInputValue(event.target.value);
};

const weatherCheck = async()=> {
        if(isFirst===false){
          setDates("loading")
        const day = (selectedDate.getDate()).toString().padStart(2, '0');
        const month = (selectedDate.getMonth() + 1).toString().padStart(2, '0');
        const year = selectedDate.getFullYear().toString();
        const response = await axios.post("http://localhost:5000//weather", { year:year, month:month,day:day});
        var html = ''
        const length =response.data.length
        setOpearentionable(typeof(response.data[0])==="string")
        for (var i=0;i<length;i++){
            html+=response.data[i]
            html+="\n"
                }
        if (dates === ""){
          weatherCheck()
        }else{
          setFlag(true)
        }
        setDates(html)
    }
 }

const handleSubmit = async (event) => {
    event.preventDefault();
    const response = await axios.post("http://localhost:5000//physics_calc", { inputData: inputValue });
    setMessage(response.data);
};

  const handleDateChange = (event) => {
    setSelectedDate(new Date(event.target.value));
    setFlag(false);
  };

return (
    <div className="App">
      <p>בלמ"ס</p>
      <h1>ברוכים הבאים למחשבון הפיזיקלי</h1>
      <h2>:הזן את המסה של המטען הכבד</h2>
    <form className="number-input" onSubmit={handleSubmit}>
        kg<input type="number" className='number-input' onChange={handleInputChange} value={inputValue} />
        <button className="number-input__button" type="submit">שלח</button> 
    </form>
    {
      message!==""?
      message!==-9?
      <div>
        <h3>{message[0]} sec :זמן</h3>
        <h3>{message[1]} m :מרחק מראה</h3>
        <h3>{message[2]} kg :משקל להשמדה</h3></div>
        :<h3> incorrect varible</h3>:<p></p>
    }
    <hr></hr>
    <h3>LATITUDE = 30 : LONGITUDE = 35</h3>
    <h2>בחר/י את התאריך בו המבצע יבוצע</h2>
    <input type="date" value={selectedDate.toISOString().substr(0, 10)} onChange={handleDateChange} />
    <button onClick={ weatherCheck} >שלח</button> 
    {dates[0]==="c"||dates[0]==="l"?<p>{dates}</p>:opearentionable?
    <div><h2 className='Opearentionable_Text_Style'>:ניתן לקיים את המבצע בתאריך הנבחר בשעות</h2><h3 >{dates}</h3></div>:<div><h2 className='UnOpearentionable_Text_Style'>לא ניתן לקיים את המבצע בתאריך הנבחר
      <br></br>
      :והטמפרטורה באיזור ההמראה בתאריך זה היא</h2><h3 >{dates}c</h3></div>}
      { <div className="star-of-david"></div> }
      <span className="dot"></span> 
    </div>
);
}

export default App;
