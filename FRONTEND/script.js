base_url = "http://33b07f8d.ngrok.io/";

var data_pass = {}

var score_range = {'1':{'start':2,'end':12},'2':{'start':2,'end':12},'3':{'start':2,'end':12},'4':{'start':2,'end':12},'5':{'start':2,'end':12},'6':{'start':2,'end':12},'7':{'start':2,'end':12},'8':{'start':2,'end':12},}

function clearText(){
    $('#score').hide();
    $('#score').html('Hi! Your Score is: ');
    
    $('#feedback_form').hide();
    $('#feedback_form').html('Rate approximately your score to this essay: ');
    
    $('#prompt_q').html('');

    $('#score_sub').hide()
    $('#feed_q').hide()

    $('#feed_q').html('Chosen score is: ');

    $('#attention_viz').hide();
    $('#attention_viz').html('Here are the attention scores for your essay learnt by our model:');

    $('#reorder_list').hide();
    $('#reorder_list').html('Pl reorder your sentences in decreasing order of importance:');
    // $('#feedback_q').html('Chosen Score is: ');
    $('#done').hide()

    data_pass=={}
};

function add_feedback(){
    var str = '<select id="feedback_scores">';
    var range = score_range[String(data_pass['prompt'])]
    for(var i= range['start']; i<=range['end'];i++){
       str += '<option>'+String(i)+'</option>';
    }
    str += '</select>';

    $('#feedback_form').append(str);
    $('#feedback_form').show();
        $('#score_sub').show();

}

function shader(words, numbers){
    var str = ''
    for (var x=0; x<words.length; x++){
        str+='<span style= "background-color:hsl(120,100%,'+String(100-(numbers[x]*100))+'%)">'+words[x]+'</span>&nbsp &nbsp'
    }
    $('#attention_viz').append(str);
    $('#attention_viz').show();
}

function reorder(){
    var str = ' <ul id="reorder">'
    essay = data_pass['essay']
    sents = essay.split('.')
    console.log(sents)
    sents = sents.filter(function(entry) { return entry.trim() != ''; });
    
    for (var x=0; x<sents.length; x++){
        str+='<li draggable="true" ondragover="dragOver(event)" ondragstart="dragStart(event)">'+ sents[x]+'</li>'   
    }
    str+='</ul>'

    $('#reorder_list').append(str);
    $('#reorder_list').show();
}

function send_logs(data_total){
    $.ajax({
          type: "GET",
          url: base_url + "send_log",
          asyn:false,
          data:data_total,
          dataType: "json",
          success: function(result) {
            alert('Thanks for your feedback');  
          },
          error: function(XMLHttpRequest, textStatus, errorThrown){
                  alert("Some error occured in get file, Try Again");
          },
        });
}

function doneFn(){

    var el=document.getElementById('reorder');
    var listItem = el.getElementsByTagName("li");

    var newNums = [];

    for (var i=0; i < listItem.length-1; i++) {
        newNums.push( listItem[i].innerHTML);
    }
    // data_pass['reorder'] = newNums;
    // console.log(data_pass)
    data_pass['reorder'] = JSON.stringify({'reorder':newNums})
    
    if (!("feedback_score" in data_pass))
    {
        alert('Pl give a rating');
        return;
    }
    
    send_logs(data_pass)
    data_pass={}
    document.getElementById("reset").click();
    // data_pass=[]
}


$(function()
{

	$('#main_form').submit(function(e)
      {
        e.preventDefault();

        $form = $(this);
        
        essay = ($form.serialize()).split('=')[1]
        data_pass['essay']=essay.replace(/[+]/g, ' ')
        if ('prompt' in data_pass){
          send_essay(data_pass);  
        }
        else{
          alert('Please select a prompt first');
        }
        // alert($form.serialize())
      });
      function send_essay(data_total){
        $.ajax({
              type: "GET",
              url: base_url + "get_essay",
              asyn:false,
              data:data_total,

              dataType: "json",
              success: function(result) {
                var score = (result[0]['score']);
                var tokens = (result[0]['tokens']);
                var attn = JSON.parse(result[0]['attn']);
                console.log(attn)
                $('#score').append(score)

                $('#score').show();
                $('.reset').show();

                add_feedback();
                console.log(result)
                shader(tokens,attn);
                reorder();

                $('#done').show();

                // line_chart('2', "MEDICINE-Cost vs YEAR: "+ disease_name,'year','Cost',result)
              },
              error: function(XMLHttpRequest, textStatus, errorThrown){
                      alert("Some error occured in get file, Try Again");
              },
            });  
        }

	
});
