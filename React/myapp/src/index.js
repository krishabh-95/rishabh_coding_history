import React, { useState } from 'react';
import ReactDOM from 'react-dom/client';
import './mycss.css';

function Myform()
{
	const [name, setName] = useState("Rishabh");

	
	return (
		<div>
			<form>
				<label>Enter your name: &nbsp;
				<input type="text" value={name} onChange={(event)=>setName(event.target.value)} />
				</label>
			</form>
			<p>Your name is {name}.</p>
		</div>
		);
}


const root = ReactDOM.createRoot(document.getElementById('root'));
//var comp = new Industry("Google","Information Technology");
//root.render(<Car value="Audi R8" brand="Audi" color="white"/>);
//root.render(listCars());
root.render(<Myform/>);