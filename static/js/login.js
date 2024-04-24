function validateform(){  
    var email=document.myform.email.value;  
    var password=document.myform.password.value;  
      
    if (email==null || email==""){  
      alert("Name can't be blank");  
      return false;  
    }else if(password.length<6){  
      alert("Password must be at least 6 characters long.");  
      return false;  
      }  
    }  