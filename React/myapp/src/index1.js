import React, { useState } from 'react';
import ReactDOM from 'react-dom/client';
import './mycss.css';

//const myFirstElement = <h1>Hello React!</h1>

class Company 
{
	constructor(name)
	{
		this.name = name;
	}
	
	show()
	{
		return "The name of the company is "+ this.name;
	}
}

class Industry extends Company
{
	constructor(name,field)
	{
		super(name);
		this.field = field;
	}
	
	testing = () => "Starting";
	
	show()
	{
		let [a,b,c,d] = calculateValues(10,20);
		return (<p>The &#123;field&#125; is {this.field}. {super.show()} <br/>{d}</p>);
	}
}

//Components must start with an uppercase letter
class Car extends React.Component
{
	constructor(props)
	{
		super(props);
		this.state = {color:"red", name : this.props.value, year: 1900, show: true};
	}
	
	changeColor = (newColor) => {
		this.setState({color:newColor});		
	}
	
	/*static getDerivedStateFromProps(props, state)
	{
		return {color: props.color};
	}*/
	
	componentDidMount()
	{
		setTimeout(() => {
			this.setState({color: "maroon"})
		}, 2000)
	}
	
	getSnapshotBeforeUpdate(prevProps, prevState) {
		if(prevState.color !== this.state.color)
		{
			document.getElementById("upd").innerHTML="The colour has changed from "+prevState.color +" to "+this.state.color;
		}
		return null;
	}
	
	componentDidUpdate()
	{
		
	}
	
	removeBrand = () => {
		this.setState({show:false});
	}
	
	render() {
		let brand;
		
		if(this.state.show)
			brand=<Brand val={this.props.brand}/>;
		else
			brand=<p>No brand</p>;
		return (
		<div>
			<p>The car is {this.state.name} and its color is {this.state.color}.</p>
			<p>The year is {this.state.year}.</p>
			<p id="upd"></p>
			<button type="button" onClick={()=>this.changeColor("purple")}>Change colour</button>
			<button type="button" onClick={this.removeBrand}>Unmount brand</button>
			<br/>
			<button type="button" onClick={jump}>Jump</button>
			{brand}
		</div>
		);
	}
}

class Brand extends React.Component 
{
	componentWillUnmount()
	{
		window.alert("The brand is going to unmount!");
	}
	
	render() {
		return <p>The brand is {this.props.val}.</p>;
	}
}

function Bike(props)
{
	return <p>The bike is {props.value}.</p>;
}

function Showroom(props)
{	
	return (
		<div>
			<p>The showroom is open.</p>
			<Bike value={props.value}/>
		</div>
	);
}

function Unique(props)
{
	return <p>This is a {props.name}</p>;
}

function listCars()
{
	let cars = [{id:1,name:'Audi'},{id:2,name:'BMW'},{id:3,name:'Ferrari'}];
	
	return (<ul>
			{cars.map((car) => <Unique key={car.id} name={car.name}/>)}
			</ul>);
}

function jump()
{
	root.render(<p>Gonna jump!</p>);
}

function calculateValues(a,b)
{
	let add = a+b;
	let sub = a-b;
	let mul = a*b;
	let div = a/b;
	
	return [add,sub,mul,div];
}

class Myform extends React.Component 
{
	const [name, setName] = useState("");

	render()
	{
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
}


const root = ReactDOM.createRoot(document.getElementById('root'));
//var comp = new Industry("Google","Information Technology");
//root.render(<Car value="Audi R8" brand="Audi" color="white"/>);
//root.render(listCars());
root.render(<Myform/>);