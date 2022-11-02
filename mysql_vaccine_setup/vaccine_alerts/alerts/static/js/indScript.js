function closePopUp()
{
	document.getElementById("pop_up").remove();
}
function isDataValid()
{
	if(document.getElementById("mail").innerHTML!=null && document.getElementById("mail").innerHTML!=undefined && document.getElementById("mail").innerHTML!='')
	{
		var mailId=document.getElementById("mail").innerHTML;
		if(mailId.indexOf("<")!=-1 || mailId.indexOf(">")!=-1 || mailId.indexOf("?")!=-1 || mailId.indexOf("@")==-1 || mailId.indexOf(".")==-1)
		{
			window.alert("Please enter a valid mail ID!");
			document.getElementById("mail").focus();
			return false;
		}
	}

	if(document.getElementById("state").value!="state" && document.getElementById("state").value!=undefined)
	{
		window.alert("Possible security threat detected. Please refresh the page and try again.");
		return false;
	}
	if(document.getElementById("pin").value!="pin" && document.getElementById("pin").value!=undefined)
	{
		window.alert("Possible security threat detected. Please refresh the page and try again.");
		return false;
	}
	if(document.getElementById("states").value!=null && document.getElementById("states").value!=undefined)
	{
		var val=document.getElementById("states").value
		if(val.indexOf("<")!=-1 || val.indexOf(">")!=-1)
		{
			window.alert("Possible security threat detected. Please refresh the page and try again.");
			return false;
		}
	}
	if(document.getElementById("district").value!=null && document.getElementById("district").value!=undefined)
	{
		var val=document.getElementById("district").value
		if(val.indexOf("<")!=-1 || val.indexOf(">")!=-1)
		{
			window.alert("Possible security threat detected. Please refresh the page and try again.");
			return false;
		}
	}
	if(document.getElementById("pincode").innerHTML!=undefined && document.getElementById("pincode").innerHTML!=null)
	{
		pinValue=document.getElementById("pincode").innerHTML
		
		if(pinVal<1 || pinVal>999999)
		{
			document.getElementById("pincode").focus();
			return false;
		}
	}
return true;
}

var stateName='',districtName='';

function fetchInitialValues()
{
	stateName=document.getElementById("states").value;
}

function stateEntered()
{	
	var val=document.getElementById("states").value;

	if(document.getElementById("states")!=undefined && stateName.localeCompare(val)!=0)
	{
		document.getElementById("form_submit").submit();
	}
}

function distEntered()
{
	if(document.getElementById("district").value!=undefined && "no_district_selected".localeCompare(document.getElementById("district").value)!=0)
	{
		document.getElementById("form_submit").submit();
	}
}