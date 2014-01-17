var result=new Array()
result['mybx']=new Array()
result['mylx']=new Array()
result['mybj']=new Array()
result['yhqbj']=new Array()
result['yhqbj'][0]=0
//-----------------------等额本息--------------------------------------
function show_calculate(){
    var qs=parseInt($('select[name=loan_deadline] option:selected').val())//获取输入期数
    if($('input[name=loan_amount_num]').val()!="")
        var bj=parseFloat($('input[name=loan_amount_num]').val())//获取输入本金
    else
        var bj=0;
    if($('input[name=annual_interest_rate]').val()!="") 
        var yll=parseFloat($('input[name=annual_interest_rate]').val())/100//获取输入月利率
    else
        var yll=0;
    var repayment_type=parseInt($('select[name=repayment_type] option:selected').val())
    if (repayment_type=='1')
        result=calculate_debj(bj,yll,qs)
    else
        result=calculate(1,bj,0,yll,qs)
    $('#table_result').html("");   
    for (var n=1;n<=qs;n++){ 
        $ul = $("<tr></tr>");
        $li_qs=$("<td></td>")
        $li_mybx = $("<td></td>");
        $li_mybj = $("<td></td>");
        $li_mylx = $("<td></td>");
        $li_data = $("<td></td>");
        var next_count=parseInt(n)+1
        $ul.append($li_qs.append(n))
        $ul.append($li_mybj.append("<input class='tbblur1' id='mybj"+n+"' name='mybj"+n+"' value='"+result['mybj'][n]+"' onchange='tqhk("+next_count+","+result['yhqbj'][n-1]+",\"table_result\")'/>"))

        $ul.append($li_mylx.append("<span class='tbblur2' id='mylx"+n+"'>"+result['mylx'][n]+"</span><input type='hidden' name='mylx"+n+"' value='"+result['mylx'][n]+"'>"))
        $ul.append($li_mybx.append("<span class='tbblur3' id='mybx"+n+"'>"+result['mybx'][n]+"</span><input type='hidden' name='mybx"+n+"' value='"+result['mybx'][n]+"'>"))
        $ul.append($li_data.append("<input type='text' name='myrq"+n+"' class='datepicker' data-date-format='yyyy-mm-dd' role='hkr' readonly/>"))
        $('#table_result').append($ul)

    }
    hkrq();//设置还款日期
    Frame();
    
}

function tqhk(qsqs,yhqbj,table){
    var qs=parseInt($('select[name=loan_deadline] option:selected').val())
    var bj=parseFloat($('input[name=loan_amount_num]').val())
    var yll=parseFloat($('input[name=annual_interest_rate]').val())/100
	var qsqs=parseInt(qsqs)
	var syq=qsqs-1
    var syqbj=parseFloat($("#mybj"+syq).val())
    var tr= document.getElementById(table).getElementsByTagName("tr");

    for(tr.length;tr.length>=qsqs;tr.length--){
        document.getElementById(table).deleteRow(tr.length-1);//删除重叠行
    }
    var yhqbj_total=parseFloat(yhqbj)+syqbj

    result=calculate(qsqs,bj,yhqbj_total,yll,qs)
    for (var n=qsqs;n<=qs;n++){
         $ul = $("<tr></tr>");
        $li_qs=$("<td></td>")
        $li_mybx = $("<td></td>");
        $li_mybj = $("<td></td>");
        $li_mylx = $("<td></td>");
        $li_data = $("<td></td>");
        var next_count=parseInt(n)+1
        $ul.append($li_qs.append(n))
        $ul.append($li_mybj.append("<input class='tbblur1' id='mybj"+n+"' name='mybj"+n+"' value='"+result['mybj'][n]+"' onchange='tqhk("+next_count+","+result['yhqbj'][n-1]+",\"table_result\")'/>"))

        $ul.append($li_mylx.append("<span class='tbblur2' id='mylx"+n+"'>"+result['mylx'][n]+"</span><input type='hidden' name='mylx"+n+"' value='"+result['mylx'][n]+"'>"))
        $ul.append($li_mybx.append("<span class='tbblur3' id='mybx"+n+"'>"+result['mybx'][n]+"</span><input type='hidden' name='mybx"+n+"' value='"+result['mybx'][n]+"'>"))
        $ul.append($li_data.append("<input type='text' name='myrq"+n+"' class='datepicker' data-date-format='yyyy-mm-dd' role='hkr' readonly/>"))
        $('#table_result').append($ul)

    }
    hkrq();//设置还款日期
    Frame();
}

//-----------------------计算等额本息--------------------------------------
//月还款金额计算公式:每月还款额=[贷款本金×月利率×（1+月利率）^还款月数]÷[（1+月利率）^还款月数—1]
//param:qsqs:起始期数 bj:本金 yhqbj:已还清本金 yll:月利率 zqs:总期数
function calculate(qsqs,bj,yhqbj,yll,zqs){

    qsqs=parseInt(qsqs)
    zqs=parseInt(zqs)
    yll=parseFloat(yll)
    yhqbj=parseFloat(yhqbj)
    bj=parseFloat(bj)

    var syqs=zqs-qsqs+1 //剩余期数
    var bjye=bj-yhqbj //本金余额
    var mybx_value

    var cleared_bj=0 //当前已还清本金
	var yhqbj_total=yhqbj//累计已还清本金
    mybx_value=(bjye*((yll*Math.pow(1+yll,syqs))/(Math.pow(1+yll,syqs)-1))).toFixed(2)//每月本息固定值
	result['yhqbj'][qsqs-1]=yhqbj
	
    
    var count=qsqs
    for (var n=1;n<=syqs;n++){

        result['mybx'][count]=mybx_value
        result['mylx'][count]=((bjye-cleared_bj)*yll).toFixed(2) //每月利息
        result['mybj'][count]=(mybx_value-result['mylx'][count]).toFixed(2)//每月本金
		
		
        cleared_bj+=parseFloat(result['mybj'][count])
		yhqbj_total+=parseFloat(result['mybj'][count])
        result['yhqbj'][count]=yhqbj_total
        count++
    }

    return result
}

//-----------------------计算等额本金--------------------------------------
//param: bj:本金 yhqbj:已还清本金 yll:月利率 zqs:总期数
function calculate_debj(bj,yll,zqs){
    /*月还款金额计算公式:每月还款额=每月本金+每月利息
    当月本金还款=总贷款数÷还款次数
    当月利息=总贷款数×（1－（还款月数-1）÷还款次数）×月利率
    当月月还款额=当月本金还款＋当月利息*/
    var qs=parseInt(zqs)
    var bj=parseFloat(bj)
    var yll=parseFloat(yll)
    var mybj=parseFloat((bj/qs)).toFixed(2)
    var cleared_bj=0 //当前已还清本金
    var yhqbj_total=0//累计已还清本金
    for (var n=1;n<=qs;n++){
        if (n==qs)
            mybj=(bj-result['yhqbj'][qs-1]).toFixed(2)
        result['mybj'][n]=parseFloat(mybj)
        result['mylx'][n]=parseFloat(bj*(1-(n-1)/qs)*yll).toFixed(2)
        result['mybx'][n]=parseFloat(result['mybj'][n])+parseFloat(result['mylx'][n])
        cleared_bj+=parseFloat(result['mybj'][n])
        yhqbj_total+=parseFloat(result['mybj'][n])
        result['yhqbj'][n]=yhqbj_total

    }

    return result
}

//-----------------------设置还款日期--------------------------------------
function hkrq(){
    var firstRq=$("input[name=loan_date]").val();
    $("input[name=first_repayment_date]").val(firstRq);
    var nian=firstRq.split("-")[0]  
    var day=parseInt(firstRq.split("-")[2])
    day=creattime(day);
    $('input[role=hkr]').each(function(num){                
        var month=parseInt(firstRq.split("-")[1])
        month=parseInt(month)+num
        month=creattime(month);
        if(month<=12){
            if(day==31){
                if(month=="04"||month=="06"||month=="09"||month=="11")
                    this.value=nian+"-"+month+"-30";
                else if(month=="02")
                    this.value=nian+"-"+month+"-28";
                else
                    this.value=nian+"-"+month+"-31";
            }
            else if(day>=28){
                if(month=="02")
                    this.value=nian+"-"+month+"-28";
                else
                    this.value=nian+"-"+month+"-"+day;
            }
            else
                this.value=nian+"-"+month+"-"+day;
        }   
        else{   
            month=parseInt(firstRq.split("-")[1])+num-12
            month=creattime(month);
            nian=parseInt(firstRq.split("-")[0])+1
            if(month<=12){
                if(day==31){
                    if(month=="04"||month=="06"||month=="09"||month=="11")
                        this.value=nian+"-"+month+"-30";
                    else if(month=="02")
                        this.value=nian+"-"+month+"-28";
                    else
                        this.value=nian+"-"+month+"-31";
                }
                else if(day>=28){
                    if(month=="02")
                        this.value=nian+"-"+month+"-28";
                    else
                        this.value=nian+"-"+month+"-"+day;
                }
                else
                    this.value=nian+"-"+month+"-"+day;
            }
            else{
                month=parseInt(firstRq.split("-")[1])+num-24
                month=creattime(month);
                nian=parseInt(firstRq.split("-")[0])+2
                if(day==31){
                    if(month=="04"||month=="06"||month=="09"||month=="11")
                        this.value=nian+"-"+month+"-30";
                    else if(month=="02")
                        this.value=nian+"-"+month+"-28";
                    else
                        this.value=nian+"-"+month+"-31";
                }
                else if(day>=28){
                    if(month=="02")
                        this.value=nian+"-"+month+"-28";
                    else
                        this.value=nian+"-"+month+"-"+day;
                }
                else
                    this.value=nian+"-"+month+"-"+day;
            }
        }
    });
    
}
