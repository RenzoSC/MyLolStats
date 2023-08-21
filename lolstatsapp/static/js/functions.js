function changeFilter(event){
    target = event.currentTarget;
    let filterId = target.dataset.filterId;
    $.ajax({
        type: 'GET',
        url: '/get_filtered_partidas/',
        data: { filtro: filterId },
        dataType: 'json',
        success: function(data) {
            console.log(data)
        },
        error: function(xhr, status, error) {
            console.log('Error:', error);
        }
    })
}