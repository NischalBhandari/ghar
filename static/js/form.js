



$(document).ready(function(){
		ajaxtime();
});
function ajaxtime()
{

	alert("hello")
	$('form').on('submit',function(event){

		$.ajax({
			data:{
				name: $('#nameInput').val(),
				email: $('#emailInput').val()


			},
			type: 'POST',
			url: '/process'
		})
		.done(function(data){
			if (data.error){
				alert(data)
				$('#errorAlert').text(data.error).show();

				$('#successAlert').hide();
			}
			else{
				$('#successAlert').text(name).show();
				$('content').text(data.date).show();
				$('#errorAlert').hide();
				alert(data)
			}

			setTimeout(ajaxtime,1000);
			$('#content').text(data.date).show();
		});

		event.preventDefault();

	});
}
