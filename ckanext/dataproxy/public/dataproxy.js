document.addEventListener("DOMContentLoaded", function(event) {

//Creates DataProxy button and injects it into DOM
function createButton(){
    var icon = document.createElement('i');
    icon.className = 'icon-rocket';
    var btn = document.createElement('a');
    btn.id = 'dataproxy-assist';
    btn.className = 'btn';
    btn.href = 'javascript:;';
    btn.onclick = 'myfunc()';
    btn.appendChild(icon);
    btn.appendChild(document.createTextNode('DataProxy'));
    $('#field-image-upload').parent().append(btn);
}
createButton();

//maps database type to default port
var portMap = {'postgresql': 5432, 'mysql': 3306, 'mssql+pymssql': ''};

function formatConnString(){
    //formats SQLAlchemy connection string from entered values
    var db = $('#field-dataproxy-db').val();
    var port = $('#field-dataproxy-port').val();
    var host = $('#field-dataproxy-host').val();
    var user = $('#field-dataproxy-user').val();
    var password = $('#field-dataproxy-password').val();
    if(password === ''){
        password = '_password_';
    }
    var database = $('#field-dataproxy-database').val();
    if(port !== ''){
        port = ':' + port;
    }
    var connstr = db + '://' + user + ':' + password + '@' + host + port + '/' +database;
    $('#field-image-url').val(connstr);
}

$('#content').on("change", "#field-dataproxy-db", function(){
    //preselect default database port for connstring
    db = $(this).val();
    $('#field-dataproxy-port').val(portMap[db]);
    formatConnString();
});

$('#content').on("keyup", "#dataproxy-fields input", function(){
    formatConnString();
});

$('#content').on("click", "#dataproxy-assist", function() {
    //enable fields so they get submitted with form
    $('#dataproxy-fields input, #dataproxy-fields select').prop("disabled", false); //enable fields
    $('#dataproxy-fields').show();
    //Now mimic the behaviour as if Link button was pressed
    var parent = $('#dataproxy-assist').parent().parent();
    parent.siblings('div').show();
    parent.hide();
});

$('#content').on("click", ".btn.btn-danger.btn-remove-url", function() {
    $('#dataproxy-fields').hide();
    //disable fields so they don't get submitted
    $('#dataproxy-fields input, #dataproxy-fields select').prop("disabled", true);
});
});
