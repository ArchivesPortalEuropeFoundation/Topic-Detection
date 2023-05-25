// Quick and simple export target #table_id into a csv
function download_table_as_csv(table_id, query_name,separator = ',') {
    // Select rows from table_id
    var rows = document.querySelectorAll('table#' + table_id + ' tr');
    // Construct csv
    var csv = [];
    for (var i = 0; i < rows.length; i++) {
        var row = [], cols = rows[i].querySelectorAll('td, th');
        for (var j = 0; j < cols.length; j++) {
            // Clean innertext to remove multiple spaces and jumpline (break csv)
            var data = cols[j].innerText.replace(/(\r\n|\n|\r)/gm, '').replace(/(\s\s)/gm, ' ')
            // Escape double-quote with double-double-quote (see https://stackoverflow.com/questions/17808511/properly-escape-a-double-quote-in-csv)
            data = data.replace(/"/g, '""');
            // Push escaped string
            row.push('"' + data + '"');
        }
        csv.push(row.join(separator));
    }
    var csv_string = csv.join('\n');
    // Download it
    var filename = query_name + '.csv';
    var link = document.createElement('a');
    link.style.display = 'none';
    link.setAttribute('target', '_blank');
    link.setAttribute('href', 'data:text/csv;charset=utf-8,' + encodeURIComponent(csv_string));
    link.setAttribute('download', filename);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

function hideSearch() {
    var x = document.getElementById("advancedSearch");
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}

$(document).ready(function () {
    $("form").submit(function (event) {
        var formData = {
            text: $("#query").val(),
            lang: $("#lang").val(),
            type: $("#type").val(),
            n_res: $("#n_res").val(),
            topic: $("#topic").val(),
            name: $("#name").val()
        };

        if (formData['name'] !== undefined){
            $("#username").html(" <strong>" + formData['name'] + "</strong>");
            $("#usernameDiv").hide();
            document.cookie = "name="+formData['name'];
        }

        var action = $(this).attr('action');
        if($("#broad_entity_search").prop('checked') == true) {
            formData.broad_entity_search = "True";
        }
        if($("#boolean_search").prop('checked') == true) {
            formData.boolean_search = "True";
        }

        $("#loader").show();
        $("#download_csv").hide();
        $("#no-more-tables").hide();
        $("#send-feedback").hide();
        $("#noofresults").hide();

        $.ajax({
            type: "POST",
            url: action,
            data: formData,
            dataType: "html",
            encode: true,
        }).done(function (data) {

            $("#loader").hide();
            $("#download_csv").show();
            $("#no-more-tables").show();

            $("#send-feedback").show();
            $("#noofresults").show();

            var query_string = $("#query").val().replace(" ","+") +"_"+$("#lang").val()+"_"+$("#type").val()+"_"+"boolean_search:"+($("#boolean_search").prop('checked') == true ? "True": "False")+"_"+"broad_entity_search:"+($("#broad_entity_search").prop('checked') == true ? "True": "False")
            $("#download_csv a").attr("onclick","download_table_as_csv('results','"+query_string+"');")
            $("#download_csv").show();
            // $("#no-more-tables").html("<table border=\"1\" class=\"dataframe data\" id=\"results\">"+$('.dataframe', data).html()+"</table>");
            $("#no-more-tables").html(data);

            handleResults(formData);
        });
        event.preventDefault();
    });

    //remember user name
    var nameCookie = getCookie("name");
    if (nameCookie !== undefined && nameCookie.length>1){
        $("#username").html(" back <strong>"+unescape(nameCookie) + "</strong>");
        $("#usernameDiv").hide();
    }
});


function handleResults(formData) {
    var link = "https://docs.google.com/forms/d/e/1FAIpQLScUB5V7-16iJusy4UEDD6hD9nJHYbi9Mmu1e7hiR0GLaSEJ-Q/viewform?usp=pp_url";

    //name
    var name = getCookie("name");
    if (name.length>1) {
        link += "&entry.1137846=" + unescape(name);
    }

    if (formData['text'] !== undefined && formData['text'].length > 0){
        link += "&entry.742507833=" + formData['text'];
    }

    if (formData['type'] == 'concept'){
        link += "&entry.471934155=Concept";
    }
    else {
        link += "&entry.471934155=Entity";
    }

    if (formData['topic'] !== undefined && formData['topic'].length > 0){
        link += "&entry.1730248296=" + formData['topic'];
    }

    if (formData['lang'] == 'en'){
        link += "&entry.1348571205=English";
    }
    else if (formData['lang'] == 'de'){
        link += "&entry.1348571205=German";
    }
    else if (formData['lang'] == 'es'){
        link += "&entry.1348571205=Spanish";
    }
    else if (formData['lang'] == 'fi'){
        link += "&entry.1348571205=Finnish";
    }
    else if (formData['lang'] == 'fr'){
        link += "&entry.1348571205=French";
    }
    else if (formData['lang'] == 'he'){
        link += "&entry.1348571205=Hebrew";
    }
    else if (formData['lang'] == 'it'){
        link += "&entry.1348571205=Italian";
    }
    else if (formData['lang'] == 'lv'){
        link += "&entry.1348571205=Latvian";
    }
    else if (formData['lang'] == 'pl'){
        link += "&entry.1348571205=Polish";
    }
    else if (formData['lang'] == 'ru'){
        link += "&entry.1348571205=Russian";
    }
    else if (formData['lang'] == 'sl'){
        link += "&entry.1348571205=Slovenian";
    }
    else if (formData['lang'] == 'sv'){
        link += "&entry.1348571205=Swedish";
    }

    var isBooleanSearch = false;
    if (formData['boolean_search'] !== undefined && formData['boolean_search'].length > 0){
        if (formData['boolean_search'] == 'True'){
            link += "&entry.75174792=Yes";
            isBooleanSearch = true;
        }
        else {
            link += "&entry.75174792=No";
        }
    }
    else {
        link += "&entry.75174792=No";
    }

    if (formData['text'] !== undefined && formData['text'].length > 0 && isBooleanSearch){
        if (formData['text'].includes(' AND ')) {
            link += "&entry.219473517=AND";
        }
        else if (formData['text'].includes(' OR ')) {
            link += "&entry.219473517=OR";
        }
        else if (formData['text'].includes('"')) {
            link += "&entry.219473517=\" \" quotation marks";
        }
        else {
            link += "&entry.219473517=None";
        }
    }

    if (formData['text'] !== undefined && formData['text'].length > 0){
        if (formData['text'].includes('*')) {
            link += "&entry.1654784031=Yes";
        }
        else {
            link += "&entry.1654784031=No";
        }
    }
    else {
        link += "&entry.1654784031=No";
    }

    if (formData['broad_entity_search'] !== undefined && formData['broad_entity_search'].length > 0){
        if (formData['broad_entity_search'] == 'True'){
            link += "&entry.2014304321=Yes";
        }
        else {
            link += "&entry.2014304321=No";
        }
    }
    else {
        link += "&entry.2014304321=No";
    }


    var noOfResults = $('.data tr').length-1;
    if (noOfResults<0) noOfResults = 0;
    if (noOfResults >10 ){
        link += "&entry.693038502=Other number (e.g. when you changed the setting)";
    }
    else {
        link += "&entry.693038502="+noOfResults;
    }

    var topicCounter = 0;
    var catholicismCounter = 0;
    var democracyCounter = 0;
    var economicsCounter = 0;
    var firstworldwarCounter = 0;
    var genealogyCounter = 0;
    var germanCounter = 0;
    var healthCounter = 0;
    var mapsCounter = 0;
    var napoleonCounter = 0;
    var notariesmCounter = 0;
    var slaveryCounter = 0;
    var transportCounter = 0;
    var otherCounter = 0;
    var genealogyCounter = 0;
    var rowCounter = 1;
    $(".data > thead > tr").each(function () {
        $(this).prepend($('<th style="width:66px;">Row #</th>'));
    });
    $(".data > tbody > tr").each(function () {
        $(this).prepend($('<td style="text-align:center">'+rowCounter+'</td>'));

        rowCounter++;
        var topic = $(this).find('td').eq(1).text();
        var content = $(this).find('td').eq(2).text();
        var country = $(this).find('td').eq(3).text();

        var translatedTopic = getTopic(topic);

        if (formData['topic'] !== undefined && formData['topic'].length > 0) {
            if (translatedTopic === formData['topic']) {
                topicCounter++;
            }
        }

        if (topic === 'Catholicism'){
            catholicismCounter++;
        }
        else if (topic === 'Economics'){
            economicsCounter++;
        }
        else if (topic === 'Democracy'){
            democracyCounter++;
        }
        else if (topic === 'Germandemocraticrepublic'){
            germanCounter++;
        }
        else if (topic === 'Health'){
            healthCounter++;
        }
        else if (topic === 'Maps'){
            mapsCounter++;
        }
        else if (topic === 'Firstworldwar'){
            firstworldwarCounter++;
        }
        else if (topic === 'FrenchNapoleonI'){
            napoleonCounter++;
        }
        else if (topic === 'Notaries'){
            notariesmCounter++;
        }
        else if (topic === 'Slavery'){
            slaveryCounter++;
        }
        else if (topic === 'Transport'){
            transportCounter++;
        }
        else if (topic === 'Other'){
            otherCounter++;
        }
        else if (topic === 'Genealogy'){
            genealogyCounter++;
        }
    });

    if (noOfResults > 0) {
        link += "&entry.1039251261=" + topicCounter;

        link += "&entry.1503735674=" + catholicismCounter;
        link += "&entry.1776866503=" + democracyCounter;
        link += "&entry.1196786101=" + economicsCounter;
        link += "&entry.542326017=" + firstworldwarCounter;
        link += "&entry.1688750304=" + genealogyCounter;
        link += "&entry.1050908082=" + germanCounter;
        link += "&entry.1374463374=" + healthCounter;
        link += "&entry.519272721=" + mapsCounter;
        link += "&entry.1114335179=" + napoleonCounter;
        link += "&entry.764641060=" + notariesmCounter;
        link += "&entry.1092656563=" + slaveryCounter;
        link += "&entry.1162342864=" + transportCounter;

    }


    $("#send-feedback a").attr("href", link);
    $("#noofresultsdisplay").html(noOfResults);
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

function getTopic(initialTopic){
    if (initialTopic == 'Economics'){
        return "Economics";
    }
    else if (initialTopic == 'Democracy'){
        return "Democracy";
    }
    else if (initialTopic == 'Germandemocraticrepublic'){
        return "German Democratic Republic";
    }
    else if (initialTopic == 'Health'){
        return "Health";
    }
    else if (initialTopic == 'Maps'){
        return "Maps";
    }
    else if (initialTopic == 'Firstworldwar'){
        return "First World War";
    }
    else if (initialTopic == 'Genealogy'){
        return "Genealogy";
    }
    else if (initialTopic == 'FrenchNapoleonI'){
        return "Napoleon I";
    }
    else if (initialTopic == 'Notaries'){
        return "Notaries";
    }
    else if (initialTopic == 'Slavery'){
        return "Slavery";
    }
    else if (initialTopic == 'Transport'){
        return "Transport";
    }
    else if (initialTopic == 'Other'){
        return "Other";
    }
    else if (initialTopic == 'Catholicism'){
        return "Catholicism";
    }
}
