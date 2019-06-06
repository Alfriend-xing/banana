
$(function(){
    // 开始写 jQuery 代码...
    function update_form(jsondata){
        // console.log('update_form')
        var timestampms=new Date().getTime()
        var timestamp=Math.ceil(timestampms/1000)
        for (data in jsondata) {
            var id=jsondata[data]['id']
            var platform=jsondata[data]['platform']
            var ip=jsondata[data]['ip']
            var cpu=jsondata[data]['cpu']
            var mem=JSON.parse(jsondata[data]["mem"])
            var updatetime=jsondata[data]['updatetime']
            var card=$('#'+id)
            // console.log(jsondata[data])
            if (card.length > 0) {
                // console.log('timestamp'+timestamp)
                // console.log('updatetime'+updatetime)
                if (timestamp-updatetime>5) {
                    if (card.find("#state_icon").attr("class")!="mini grey circle icon") {
                        myFunction({"state":false,"msg":ip+"下线"})
                        card.find("#state_icon").attr("class","mini grey circle icon")
                        var b = card.find(".bar")
                        b.first().attr("style","transition-duration: 2000ms; width:0%;")
                        b.last().attr("style","transition-duration: 2000ms; width:0%;")
                        card.find(".label#l1").text("cpu ")
                        card.find(".label#l2").text("mem ")
                    }
                    else {
    
                    }
                }
                else {
                    if (card.find("#state_icon").attr("class")!="mini green circle icon") {
                        myFunction({"state":true,"msg":ip+"上线"})
                        card.find("#state_icon").attr("class","mini green circle icon")
                        
                    }
                    else {
                        
                    }
                    var b = card.find(".bar")
                    b.first().attr("style","transition-duration: 2000ms; width:"+cpu+"%")
                    card.find(".label#l1").text("cpu "+cpu+"%")
                    b.last().attr("style","transition-duration: 2000ms; width:"+mem["percent"]+"%")
                    card.find(".label#l2").text("mem "+mem["percent"]+"%")
                }
                
            }
            else {
                // console.log('add card')
                if (timestamp-updatetime<5) {
                    myFunction({"state":true,"msg":ip+"上线"})
                }
                var label=jsondata[data]['label']
                var msg=jsondata[data]['message']
                if (label) {
    
                } 
                else {
                    label='test server'
                };
                if (msg) {
                    // console.log(msg)
                }
                else {
                    msg='Server description'
                }
                // src={{url_for("static",filename="images/centos.png")}}>\
                var t='<div class="card" id="'+id+'" onclick="serverinfo(\''+id+'\')">\
                        <div class="content">\
                            <div data-tooltip="'+platform+'" data-position="top right" id="platform">\
                            <img class="right floated mini ui image" \
                            src="static/images/centos.png">\
                            </div>\
                            <div class="header" id="ip">'+ip+'<i class="mini green circle icon" id="state_icon"></i>\
                            </div>\
                            <div class="meta">\
                                <a class="ui teal label">'+label+'</a>\
                            </div>\
                            <div class="description">'+msg+'</div>\
                        </div>\
                        <div class="extra content">\
                                <div class="label" id="l1">cpu</div>\
                                <div class="ui teal progress" \
                                style="margin:0 0 0 0;" \
                                data-position="top left" \
                                id="p1">\
                                <div class="bar" \
                                style="transition-duration: 2000ms; width: '+cpu+'%;"></div>\
                                </div>\
                                <div class="label" id="l2">mem</div>\
                                <div class="ui progress" \
                                style="margin:0 0 0 0;" \
                                data-tooltip="'+mem["used"]+'/'+mem["total"]+'" \
                                data-position="bottom left" \
                                id="p2">\
                                <div class="bar"  \
                                style="transition-duration: 2000ms; width: '+mem["percent"]+'%;"></div>\
                                </div>\
                        </div>\
                </div>'
                $("#cards").append(t)
            }
        }
    }
    function refun() {
        $.getJSON( "api", function( data ) {
            update_form(data);
            });
    }
    window.setInterval( refun, 1000);
    $("#ccc").find("#p2").find(".bar").attr("style","transition-duration: 300ms; width: 37%;");
    });

        
// 右下角弹窗函数
function myFunction(data) {
    // data {'state':true,'msg':'127.0.0.1上线'}
    var x = $("#snackbars");
    var sb = $("<div></div>")
    if (data['state']) {
        sb.attr({"id":"snackbar",
                    "class":"show",
                    "style":"background-color: #00b5ad;"})
            // background-color: #00b5ad #888;
    }
    else {
    sb.attr({"id":"snackbar",
                "class":"show",
                "style":"background-color: #888;"})
        // background-color: #00b5ad #888;
    }
sb.text(data["msg"])
x.append(sb)
//   x.className = "show";
    setTimeout(function(){ sb.remove(); }, 3000);
}


// 修改信息函数
function submit_msg() {
    var id =$('.ui.modal').find(".header").attr("id")
    var c_l =$("#change_label").val()
    var c_m =$("#change_msg").val()
    if (c_l || c_m) {
        $("submit").attr("class","ui primary basic loading button")
        data={
            "id":id,
            "label":c_l,
            "message":c_m
        }
        var saveData = $.ajax({
          type: 'POST',
          url: "/api/msg",
          data: data,
          dataType: "json",
          success: function(resultData) { 
              myFunction({"state":true,"msg":"修改成功"});
              $("submit").attr("class","ui primary basic button"); },
          error: function(a,b,c) { 
              myFunction({"state":false,"msg":"修改失败"}); 
              $("submit").attr("class","ui primary basic button");}
      });
      
    }
    else {
      myFunction({"state":false,"msg":"内容为空"});
    }
    
    var c_l =$("#change_label").val("")
    var c_m =$("#change_msg").val("")
  
}


// 删除记录函数
function delete_server() {
    var id =$('.ui.modal').find(".header").attr("id")
    var ip =$('.ui.modal').find(".header").text()
    var r=confirm("将从数据库中删除\n"+ip);
    if (r) {
        data ={"id":id}
      var saveData = $.ajax({
              type: 'POST',
              url: "/api/delete",
              data: data,
              dataType: "json",
              success: function(resultData) { 
                  myFunction({"state":true,"msg":"删除成功"});
                  $("#"+id).remove()},
              error: function(a,b,c) { 
                  myFunction({"state":false,"msg":"删除失败"});}
          });
      }
      else {
          myFunction({"state":false,"msg":"取消"});
      }
    
}

// 画图函数
function drawchart(data) {
    var type=data['type']
    var elementid=data['id']
    var x=data['x']
    var y=data['y']
    var title=data['title']
    var label=data['label']
    $("#"+elementid).remove();
      $('#tab_'+elementid).append('<canvas id="'+elementid+'" style="width: 100%;height: 100%;"></canvas>');
      var ctx = $("#"+elementid)[0].getContext('2d');
      if (type=='net') {
          var upload=new Array()
          var dwload=new Array()
          for(j = 0,len=y.length; j < len; j++) {
              // console.log(y)
              // console.log(y[j])
              if (y[j]==0) {
              upload[j]=0
              dwload[j]=0
              }
              else {
              var tmp=y[j].split('/')
              upload[j]=Number(tmp[0])
              dwload[j]=Number(tmp[1])
              }
          }
          var chart = new Chart(ctx, {
          // The type of chart we want to create
          type: 'line',

          // The data for our dataset
          data: {
              labels: x, //['January', 'February', 'March', 'April', 'May', 'June', 'July'],
              datasets: [{
                  label: "上传流量(MB)", //'My First dataset',
                  fill: false,
                  radius: 0,
                  backgroundColor: 'rgb(0,181,173)',//#00b5ad
                  borderColor: 'rgb(0,181,173)',
                  data: upload, //[0, 10, 5, 2, 20, 30, 45]
              },
              {
                  label:"下载流量(MB)",
                  fill: false,
                  radius: 0,
                  backgroundColor: 'rgb(118,118,118)', //#767676
                  borderColor: 'rgb(118,118,118)',
                  data: dwload, //[0, 10, 5, 2, 20, 30, 45]
              }]
          },

          // Configuration options go here
          options: {
              responsive: true,
              title: {
                  display: true,
                  text: title
              },
          }
      });
      }
      else {
          var chart = new Chart(ctx, {
          // The type of chart we want to create
          type: 'line',

          // The data for our dataset
          data: {
              labels: x, //['January', 'February', 'March', 'April', 'May', 'June', 'July'],
              datasets: [{
                  label: label, //'My First dataset',
                  radius: 0,
                  backgroundColor: 'rgba(0,181,173,0.5)',
                  borderColor: 'rgb(0,181,173)',
                  // pointBorderWidth:0,
                  borderWidth:1,
                  data: y, //[0, 10, 5, 2, 20, 30, 45]
              }]
          },

          // Configuration options go here
          options: {
              tooltips:{
                  mode:'x-axis'
              },
              responsive: true,
              title: {
                  display: true,
                  text: title
              },
              scales: {
                  yAxes: [{
                      ticks: {
                          suggestedMin: 0,
                          suggestedMax: 100,
                      }
                  }]
              }
          }
      });
      }
      
      }
  function drawtab(id) {
      $.getJSON('/api/history/'+id,function(data){
          if (data['state']) {
              // $("div[data-tab='first']").text(data['cpu'])
              // $("div[data-tab='second']").text(data['mem'])
              // $("div[data-tab='third']").text(data['disk'])
              // $("div[data-tab='fourth']").text(data['net'])
              $("div[data-tab='first']").text('')
              $("div[data-tab='second']").text('')
              $("div[data-tab='third']").text('')
              $("div[data-tab='fourth']").text('')
              var datetime= new Array()
              // var time_zone=new Date().getTimezoneOffset()/60
              for (i=0,len=data["updatetime"].length;i<len;i++) {
                  tmp_time=new Date(Number(data["updatetime"][i])*1000)
                  datetime[i]= tmp_time.getMonth()+'-'+tmp_time.getDate()+' '+tmp_time.getHours()+':'+tmp_time.getMinutes()
                  // console.log(datetime[i])
              }
              drawchart({"id":"CPU_chart",
              "type":"cpu",
              "x":datetime,
              "y":data["cpu"],
              "title":"过去24小时CPU使用情况",
              "label":"CPU使用率"})
              drawchart({"id":"MEM_chart",
              "type":"mem",
              "x":datetime,
              "y":data["mem"],
              "title":"过去24小时内存使用情况",
              "label":"内存使用率"})
              drawchart({"id":"DISK_chart",
              "type":"disk",
              "x":datetime,
              "y":data["disk"],
              "title":"过去24小时硬盘使用情况",
              "label":"硬盘使用率"})
              drawchart({"id":"NET_chart",
              "type":"net",
              "x":datetime,
              "y":data["net"],
              "title":"过去24小时网络使用情况",
              "label":""})
          }
          else {
              $("div[data-tab='first']").text('ERROR')
              $("div[data-tab='second']").text('ERROR')
              $("div[data-tab='third']").text('ERROR')
              $("div[data-tab='fourth']").text('ERROR')
          }
      });
  }









