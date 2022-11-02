function isDataValid()
{
if(document.getElementById("mail").value!=null && document.getElementById("mail").value!=undefined && document.getElementById("mail").value!='')
{
	var mailId=document.getElementById("mail").value;
	if(mailId.indexOf("<")!=-1 || mailId.indexOf(">")!=-1 || mailId.indexOf("?")!=-1 || mailId.indexOf("@")==-1 || mailId.indexOf(".")==-1)
	{
		window.alert("Please do not alter your mail ID!");
		return false;
	}
}

if(document.getElementById("district_id").value!=null && document.getElementById("district_id").value!=undefined)
{
	var val=document.getElementById("district_id").value
	if(val.indexOf("<")!=-1 || val.indexOf(">")!=-1)
	{
		window.alert("Please clear your browser cache and try again.");
		return false;
	}
}

if(document.getElementById("pincode").value!=undefined && document.getElementById("pincode").value!=null)
{
	pinValue=document.getElementById("pincode").value
	
	if(pinVal<1 || pinVal>999999)
	{
		window.alert("Please clear your browser cache and try again.");
		return false;
	}
}

if(document.getElementById("otp").value!=undefined && document.getElementById("otp").value!=null)
{
	pinValue=document.getElementById("otp").value
	
	if(pinVal<1 || pinVal>999999)
	{
		window.alert("Please clear your browser cache and try again.");
		return false;
	}
}
return true;
}