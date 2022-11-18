import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def sendamail(to, sub):
    if(sub == "Registration Successful!"):
        c = '''  <style>
  html, body {
    height: 100%;
    width: 100%;
  }
  .center {
    text-align: center;
    color: #004085;
  }
  img {
    display: block;
    margin-left: auto;
    margin-right: auto;
  }
  
  div.container {
    text-align: center;
  }
  
  ul.myUL {
    display: inline-block;
    text-align: left;
  }
  .button {
    background-color: #005275;
    border: none;
    color: white;
    padding: 15px 32px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 4px 2px;
  
  }
  .container1 {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 200px;
  }
</style>  
  <h1 class="center">VAST Plasma Donor Application</h1>
  <h1 style="margin: 0; color: #072b52; font-family: 'Lora', Georgia, serif; font-size: 50px; font-weight: normal; letter-spacing: 1px; line-height: 120%; text-align: center; margin-top: 0; margin-bottom: 0;"><strong>thank you.</strong></h1>
<div >
  <p style="margin: 0; font-size: 16px; text-align: center; mso-line-height-alt: 24px;"><span style="font-size:16px;"><strong>Hey there,</strong></span></p>
  <p style="margin: 0; font-size: 16px; text-align: center; mso-line-height-alt: 24px;"><span style="font-size:16px;">Thank you for registering as a donor in Vast.</span></p>
  <p style="margin: 0; font-size: 16px; text-align: center; mso-line-height-alt: 24px;"><span style="font-size:16px;">It's a pleasure to have you as our donor.</span></p>
  <p style="margin: 0; font-size: 16px; text-align: center; mso-line-height-alt: 18px;"> </p>
  <p style="margin: 0; font-size: 16px; text-align: center; mso-line-height-alt: 24px;"><span style="font-size:16px;">We would like to take this time to thank you for your interest</span></p>
  <p style="margin: 0; font-size: 16px; text-align: center; mso-line-height-alt: 24px;"><span style="font-size:16px;">and we hope to see you again soon.</span></p>
  <br><br>
  <p style="margin: 0; font-size: 16px; text-align: center; mso-line-height-alt: 24px;"><span style="font-size:16px; color:red">Plasma is necessary to help your body recover from injury, distribute nutrients,</span></p>
  <p style="margin: 0; font-size: 16px; text-align: center; mso-line-height-alt: 24px;"><span style="font-size:16px; color:red ">Remove waste and prevent infection, while moving throughout your circulatory system</span></p>
  <br>
  <p style="margin: 0; font-size: 16px; text-align: center; mso-line-height-alt: 24px;"><span style="font-size:20px; font-family: 'Lora'; font-weight: bold;">VAST can be used to perform these features</span></p>
  <div class="container">
  <ul class="myUL"> 
    <li>View the eligibility to donate</li>
    <li>Accept to donate</li>
    <li>Help people in need by viewing emergency requirements</li>
    <li>View donation camps nearby</li>
    <li>Save blood donation certificate</li>
    <li>View and update your health card</li>
    <li>Get nearby hospital information on where to donate with the location</li>
  </ul>
</div>
  <div class="container1">
    <a href="#dashboard" class="button">Dashboard</a>
  </div>
  
</div> '''
  
    elif(sub == "Health Card Updated Successfully"):
        c = '''  <style>
    html, body {
  height: 100%;
  width: 100%;
}
.center {
  text-align: center;
  color: #004085;
}
img {
  display: block;
  margin-left: auto;
  margin-right: auto;
}

div.container {
  text-align: center;
}

ul.myUL {
  display: inline-block;
  text-align: left;
}
.button {
  background-color: #005275;
  border: none;
  color: white;
  padding: 15px 32px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 4px 2px;

}
.container1 {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
}

  </style>
  <h1 class="center" style="text-align:center;">VAST Plasma Donor Application</h1>
 
  <h1 style="margin: 0; color: #072b52; font-family: 'Lora', Georgia, serif; font-size: 50px; font-weight: normal; letter-spacing: 1px; line-height: 120%; text-align: center; margin-top: 0; margin-bottom: 0;"><strongThank you</strong></h1>
<div >
  <p style="margin: 0; font-size: 16px; text-align: center; mso-line-height-alt: 24px;"><span style="font-size:16px;"><strong>Hey there,</strong></span></p>
  <p style="margin: 0; font-size: 16px; text-align: center; mso-line-height-alt: 24px;"><span style="font-size:16px;">thank you for visiting Vast and updating your details.</span></p>
  <p style="margin: 0; font-size: 16px; text-align: center; mso-line-height-alt: 24px;"><span style="font-size:16px;">You could view your updated details in VAST by clicking the Dashboard link below.</span></p>
  <p style="margin: 0; font-size: 16px; text-align: center; mso-line-height-alt: 24px;"><span style="font-size:16px;">It's a pleasure to have you as our donor.</span></p>
  <p style="margin: 0; font-size: 16px; text-align: center; mso-line-height-alt: 18px;"> </p>
  <p style="margin: 0; font-size: 16px; text-align: center; mso-line-height-alt: 24px;"><span style="font-size:16px;">We would like to take this time to thank you for your interest</span></p>
  <p style="margin: 0; font-size: 16px; text-align: center; mso-line-height-alt: 24px;"><span style="font-size:16px;">and we hope to see you again soon.</span></p>
  <br><br>
  <p style="margin: 0; font-size: 16px; text-align: center; mso-line-height-alt: 24px;"><span style="font-size:16px; color:red">Plasma is necessary to help your body recover from injury, distribute nutrients,</span></p>
  <p style="margin: 0; font-size: 16px; text-align: center; mso-line-height-alt: 24px;"><span style="font-size:16px; color:red ">remove waste and prevent infection, while moving throughout your circulatory system</span></p>
  <br>
  <p style="margin: 0; font-size: 16px; text-align: center; mso-line-height-alt: 24px;"><span style="font-size:20px; font-family: 'Lora'; font-weight: bold;">VAST can be used to perform these features</span></p>
  <div class="container">
  <ul class="myUL"> 
    <li>View the eligibility to donate</li>
    <li>Accept to donate</li>
    <li>Help people in need by viewing emergency requirements</li>
    <li>View donation camps nearby</li>
    <li>Save blood donation certificate</li>
    <li>View and update your health card</li>
    <li>Get nearby hospital information on where to donate with the location</li>
  </ul>
</div>
  <div class="container1">
    <a href="#dashboard" class="button">Dashboard</a>
  </div>
  
</div>'''
    else:
        c = '''
          <style>
    html, body {
  height: 100%;
  width: 100%;
}
.center {
  text-align: center;
  color: #004085;
}
img {
  display: block;
  margin-left: auto;
  margin-right: auto;
}

div.container {
  text-align: center;
}

ul.myUL {
  display: inline-block;
  text-align: left;
}
.button {
  background-color: #005275;
  border: none;
  color: white;
  padding: 15px 32px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 4px 2px;

}
.container1 {
  display: flex;
  justify-content: center;
  align-items: center;
}


  </style>
  <h1 class="center">VAST Plasma Donor Application</h1>

  <h1 style="margin: 0; color: #072b52; font-family: 'Lora', Georgia, serif; font-size: 50px; font-weight: normal; letter-spacing: 1px; line-height: 120%; text-align: center; margin-top: 0; margin-bottom: 0;"><strong>thank you.</strong></h1>
<div >
  <p style="margin: 0; font-size: 16px; text-align: center; mso-line-height-alt: 24px;"><span style="font-size:16px;"><strong>Hey there,</strong></span></p>
  <p style="margin: 0; font-size: 16px; text-align: center; mso-line-height-alt: 24px;"><span style="font-size:16px;">Thank you for accepting the request.</span></p>
  <p style="margin: 0; font-size: 16px; text-align: center; mso-line-height-alt: 24px;"><span style="font-size:16px;">You could view the hospital details by clicking the Dashboard link below.</span></p>
  <p style="margin: 0; font-size: 16px; text-align: center; mso-line-height-alt: 24px;"><span style="font-size:16px;">It's a pleasure to have you as our donor.</span></p>
  <p style="margin: 0; font-size: 16px; text-align: center; mso-line-height-alt: 18px;"> </p>
  <p style="margin: 0; font-size: 16px; text-align: center; mso-line-height-alt: 24px;"><span style="font-size:16px;">We would like to take this time to thank you for your interest</span></p>
  <p style="margin: 0; font-size: 16px; text-align: center; mso-line-height-alt: 24px;"><span style="font-size:16px;">and we hope to see you again soon.</span></p>
  <br><br>
   <p style="margin: 0; font-size: 20px; text-align: center; mso-line-height-alt: 24px; color:green"> <strong>YAY!!!</strong></p>
  <p style="margin: 0; font-size: 20px; text-align: center; mso-line-height-alt: 24px; color:green"><strong>You're saving a LIFE!</strong></p>
  <br>
  <div class="container1">
    <a href="#dashboard" class="button">Dashboard</a>
  </div>
  
</div>'''
    message = Mail(
        from_email='vastplasmadonation@gmail.com',
        to_emails=to,
        subject=sub,
        html_content=c)
    sg = SendGridAPIClient(os.environ['SENDGRID_API_KEY'])
    response = sg.send(message)