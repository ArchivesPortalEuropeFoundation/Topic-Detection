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
            n_res: $("#n_res").val()
        };
        if($("#broad_entity_search").prop('checked') == true) {
            formData.broad_entity_search = "True";
        }
        if($("#boolean_search").prop('checked') == true) {
            formData.boolean_search = "True";
        }

        $.ajax({
            type: "POST",
            url: "query.php",
            data: formData,
            dataType: "html",
            encode: true,
        }).done(function (data) {
            var query_string = $("#query").val().replace(" ","+") +"_"+$("#lang").val()+"_"+$("#type").val()+"_"+"boolean_search:"+($("#boolean_search").prop('checked') == true ? "True": "False")+"_"+"broad_entity_search:"+($("#broad_entity_search").prop('checked') == true ? "True": "False")
            $("#download_csv a").attr("onclick","download_table_as_csv('results','"+query_string+"');")
            $("#download_csv").show();
            // $("#no-more-tables").html("<table border=\"1\" class=\"dataframe data\" id=\"results\">"+$('.dataframe', data).html()+"</table>");
            $("#no-more-tables").html(data);
        });
        event.preventDefault();
    });
});
