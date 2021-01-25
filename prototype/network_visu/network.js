function getTools(selected_operation,tools){
    var rows = [];
    $.each(tools,function(keyS,value){
        if (value.operation == selected_operation){
            rows.push(value);
        }
    });
    return(rows)

}

function createTable(rows){
    var html = "<table border='1|1'>";
    for (var i = 0; i < rows.length; i++) {
        var joinedGroup = rows[i].group.join(", ")
        html+="<tr>";
        html+="<td>"+rows[i].name+"</td>";
        html+="<td>"+rows[i].operation+"</td>";
        html+="<td>"+joinedGroup+"</td>";

        html+="</tr>";

    }
    html+="</table>";
    return (html)
}


function selectLevel(links,iter,nodes,allnodes,distance,score){
    var it = 0;
    var selected_links = []
    var selected_nodes = []
    var integratednodes = [];
    var getlinks = []
    var valueIter = parseInt(iter, 10)
    var valueScore =  parseFloat(score, 10)
    while(it != valueIter){
        it = it + 1;
        //For each node...
        //First iteration only the selected node.Each iterations => append new nodes
        var tmpNodes = nodes;
        //console.log(tmpNodes)
        $.each(tmpNodes,function(keyS,valueS){
            var obj = valueS.id
            $.each(links, function(key, value){
                if (value.source.search(obj) != -1)
                {
                    if(parseFloat(value[distance],10) >= valueScore){
                        //console.log(value[distance]);
                        console.log(valueScore);
                        if(getlinks.indexOf(value.source+"_"+value.target) == -1){
                            selected_links.push({'data':{'id':value.source+"_"+value.target,'source':value.source,'target':value.target,'jaccard':value.jaccard,'salton':value.salton,'hubert':value.hubert}});
                            getlinks.push(value.source+"_"+value.target);
                            if (integratednodes.indexOf(value.target) == -1)
                        {
                            nodes.push({'id':value.target});
                            integratednodes.push(value.target);
                            $.each(allnodes, function(key, valueN){
                                if (valueN.id == value.target)
                                {
                                    //console.log(value.target);
                                    //console.log(value)

                                    selected_nodes.push({'data':valueN});
                                }
                            });
                            
                        }
                        if (integratednodes.indexOf(value.source) == -1)
                        {
                            nodes.push({'id':value.source});
                            integratednodes.push(value.source);
                            $.each(allnodes, function(key, valueN){
                                if (valueN.id == value.source)
                                {
                                    //console.log(value.source);
                                    //console.log(value)
                                    selected_nodes.push({'data':valueN});
                                }
                            });
                        }

                        }
                    }
                    
                }
                
            });
        });
       
    }
    return ({'edges':selected_links,'nodes':selected_nodes})
}

function createNetwork(selectedObject,data){
    var isNode = []
    var elementsJSON = []
    var nodes = data.nodes;
    var links = data.links;

    $.each(links, function(key, value){
        if (value.target.search(click_text) != -1 || value.source.search(click_text) != -1)
    {
        elementsJSON.push({'data':{'id':value.source+"_"+value.target,'source':value.source,'target':value.target}});
        if (isNode.indexOf(value.target) == -1)
        {
            //console.log(value.target);
            isNode.push(value.target);
        }
        if (isNode.indexOf(value.source) == -1)
        {
            //console.log(value.target);
            isNode.push(value.source);
        }
    }
        
    });
    
}

$(document).ready(function(){
    $.ajaxSetup({ cache: false });
-
    $.getJSON('data_tools.json', function(data) {
        var operations = data.operations;
        var tools = data.tools;
        var links = data.links;
        $('#search').keyup(function(){
            $('#result').html('');
            $('#state').val('');
            var searchField = $('#search').val();
            var expression = new RegExp(searchField, "i");
            $.each(operations, function(key, value){
                //console.log(value)
                var group_it = value.group.join(", ")
                if (value.id.search(expression) != -1)
                {
                    $('#result').append('<li class="list-group-item link-class">'+value.id);
                }
            });   

        });
        $('#result').on('click', 'li', function() {
            var click_text = $(this).text();
            $('#selectedvalue').append(click_text);
            var iter = document.getElementById('iteration').value;
            var distance = document.getElementById('distance').value;
            var score = document.getElementById('score').value;
            
            var elements = selectLevel(links,iter,[{'id':click_text}],operations,distance,score)
            //console.log(elements)
            var cy = cytoscape({
                container: document.getElementById('cy'),
                elements: {
                    nodes : elements.nodes,
                    edges : elements.edges
                },
                style: [{
                    selector: 'node',
                    css: {
                      'content': 'data(id)',
                      'text-valign': 'center',
                      'text-halign': 'center'
                    }
                  },
                  {
                    selector: '$node > node',
                    css: {
                      'padding-top': '10px',
                      'padding-left': '10px',
                      'padding-bottom': '10px',
                      'padding-right': '10px',
                      'text-valign': 'top',
                      'text-halign': 'center',
                      'background-color': '#bbb'
                    }
                  },
                  {
                    selector: 'edge',
                    css: {
                      'target-arrow-shape': 'triangle',
                      'curve-style': 'bezier'
                    }
                  },
                  {
                    selector: ':selected',
                    css: {
                      'background-color': '#aaa',
                      'line-color': 'black',
                      'target-arrow-color': 'black',
                      'source-arrow-color': 'black'
                    }
                  }
                ],
          
            });
            cy.layout({
                name: 'breadthfirst',
            }).run();
            cy.on('tap', 'node', function (evt) {
                var operation =  evt.target.id()
                var rows = getTools(operation,tools);
                //console.log(rows)
                var html = createTable(rows)
                //console.log(evt.target.id())
                document.getElementById("box").innerHTML = html;
                $("#myModal").modal()
            });
            
            cy.on('tap', function(e){
                if( e.cyTarget === cy ){
                    cy.elements().removeClass('faded');
                }
            });
            $('#search').val($.trim(''));
            $("#result").html(click_text);
        });
        
    });
});