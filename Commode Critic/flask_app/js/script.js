// var map;
//     function initMap() {
//     map = new google.maps.Map(document.getElementById('map'), {
//         center: {lat: -34.397, lng: 150.644},
//         zoom: 8
//         });
//     }


/* corr to ref js : if (c == 2) {
    msg = num + ' is a Prime number';
    imageshown = "OptimusPrime.gif"
  } else {
     msg = num + ' is NOT a Prime number';
     imageshown = "Megatron.gif"
  }

  var result = document.getElementById('result');
  var img = result.nextElementSibling;

  result.textContent = msg;
  img.src = imageshown;
}  <--function closing*/

/*ref: if (c == 2) {
    document.getElementById('result').innerHTML = num + ' is a Prime number';
    var imageshown = "OptimusPrime.gif"
}else{
    document.getElementById('result').innerHTML = num + ' is NOT a Prime number';
    var imageshown = "Megatron.gif"
}
}        
</script>
<div class="container">
<form  id="contact" method="post">

<h3>Prime-O-Tron</h3>
<h4>Please fill in a number in the field below and press "Calculate" to see if it is a prime number or not.</h4>

Please enter a number:
<input type="number" id="num" name="num" min="0" />
<input type="button" value="Find Prime Number" onclick="findPrime()" name="find" />
<div style="margin-top: 10px;" id="result"></div>
<img src= imageshown>
end ref*/
$(document).ready(function() {
    $("#formButton").click(function() {
      $("#form1").toggle();
    });
  });