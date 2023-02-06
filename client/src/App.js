
import {useEffect, useState } from 'react';
import axios from 'axios';
import './App.css';
function App() {
  // React component
const [opearentionable, setOpearentionable] = useState(false)
const [inputValue, setInputValue] = useState("");
const [message, setMessage] = useState("");
const [isFirst, setFlag] = useState(true);
const initialDate = new Date('2023-01-01');
const [selectedDate, setSelectedDate] = useState(initialDate);
const [hours, setHours] = useState("loading");

useEffect(() => weatherCheck,
   // eslint-disable-next-line react-hooks/exhaustive-deps
   []);

const handleInputChange = (event) => {
    setInputValue(event.target.value);
};


const weatherCheck = async(counter = 1) => {
  // Check if the function is being executed only once
  if (isFirst) {
    // Update the hours variable to loading
    setHours("loading");

    // Get the date from selectedDate object
    const day = (selectedDate.getDate()).toString().padStart(2, '0');
    const month = (selectedDate.getMonth() + 1).toString().padStart(2, '0');
    const year = selectedDate.getFullYear().toString();

    // Make a POST request to the weather endpoint
    const response = await axios.post("http://localhost:5000//weather", { year:year, month:month,day:day});
    
    // Initialize a variable to store the data in HTML format
    var html = '';
    const length = response.data.length;

    // Update the state of operationable based on the data received
    setOpearentionable(typeof(response.data[0]) === "string");

    // Loop through the data received and store it in the HTML format
    for (var i = 0; i < length; i++) {
      html += response.data[i];
      html += "\n";
    }

    // Check if hours is an empty string
    if (hours === "" && counter !=3) {
      // If it is, call the weatherCheck function again
      weatherCheck(counter++);
    } else {
      // If not, update the state of isFirst to false
      setFlag(false);
    }

    // Update the state of hours with the data in HTML format
    setHours(html);
  }
}

const handleSubmit = async (event) => {
  // Prevent the default form submit behavior
  event.preventDefault();
  
  // Send a post request to the server with the input value as the payload
  const response = await axios.post("http://localhost:5000//physics_calc", { inputData: inputValue });
  
  // Update the state with the response data
  setMessage(response.data);
  };

// This function is called whenever the date is changed
const handleDateChange = (event) => {
  // Set the selected date to the new date chosen by the user
  setSelectedDate(new Date(event.target.value));
  // Set the isfirst to true, indicating that the date has been changed
  setFlag(true);
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
      message !== "" ? 
        message !== -9 ? 
          <div>
            {/* Displaying the calculated time, distance and weight */}
            <h3>{message[0]} sec :זמן</h3>
            <h3>{message[1]} m :מרחק מראה</h3>
            <h3>{message[2]} kg :משקל להשמדה</h3>
          </div>
        : 
          <h3>incorrect variable</h3> 
      : 
        <p></p>
    }

    <hr></hr>
    <h3>LATITUDE = 30 : LONGITUDE = 35</h3>
    <h2>בחר/י את התאריך בו המבצע יבוצע</h2>
    <input type="date" value={selectedDate.toISOString().substr(0, 10)} onChange={handleDateChange} />
    <button onClick={ weatherCheck} >שלח</button> 


    {      
  // Conditional rendering to show the result of weather check
    // Check if the first character of `hours` is 'c' or 'l' to show connection_errors or loading
    hours[0] === "c" || hours[0] === "l" ? 
        // If yes, render a paragraph with the contents of `hours`
        <p>{hours}</p>
        // If not, check if `opearentionable` is truthy
        : opearentionable ? 
            // If `opearentionable` is truthy, render a div with the text and the contents of `hours`
            <div>
                <h2 className='Opearentionable_Text_Style'>ניתן לקיים את המבצע בתאריך הנבחר בשעות</h2>
                <h3>{hours}</h3>
            </div>
            // If `opearentionable` is falsy, render a div with the text and the contents of `hours` with a 'c' appended to show celsius
            : <div>
                <h2 className='UnOpearentionable_Text_Style'>לא ניתן לקיים את המבצע בתאריך הנבחר<br></br>:והטמפרטורה באיזור ההמראה בתאריך זה היא</h2>
                <h3>{hours}c</h3>
            </div>
  }
      <div className='star-of-david'></div>
      <span className="dot"></span> 
    </div>
);
}

export default App;
