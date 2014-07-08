/**
 * Created by johhny on 14-7-2.
 */

function Calculate(){
    var str=document.getElementById('Cal_text').value;
    var data='';
    data=tran(str);
    var result=Cal_RPN(data);
    return result;
}

/**
* 将中序表达式转换为逆波兰式
* */
function tran(str){
    var len=str.length;
    var str_p=0,opr_top= 0,exp_top= 0;
    var stack_opr=new Array()
    var stack_exp=new Array()
    var ch='',tmp_ch='',tmp_tran_num='',tmp_num,num;
    var flag;
    stack_opr[opr_top]='#'

    while (str_p<len){

        ch=str[str_p];

        switch (ch){
            case '(':
                opr_top++;
                stack_opr[opr_top]=ch;

                break;
            case ')':
                while(stack_opr[opr_top]!='('){
                    stack_exp[exp_top++]=stack_opr[opr_top--];
                }
                opr_top--;

                break;
            case '+':
            case '-':
                tmp_ch=stack_opr[opr_top];

                while(tmp_ch!='#'){

                    if (tmp_ch=='('){
                        break
                    }
                    else{
                        stack_exp[exp_top++]=stack_opr[opr_top--];
                    }
                    tmp_ch=stack_opr[opr_top];
                }
                opr_top++;
                stack_opr[opr_top]=ch;

                break;
            case '*':
            case '/':
                tmp_ch=stack_opr[opr_top];
                while(tmp_ch!='#'&&tmp_ch!='+'&&tmp_ch!='-'){

                    if (tmp_ch=='('){
                        break
                    }
                    else{
                        stack_exp[exp_top++]=stack_opr[opr_top--];
                    }
                    tmp_ch=stack_opr[opr_top];
                }
                opr_top++;
                stack_opr[opr_top]=ch;
                break;
            default :

                tmp_num=ch;

                while (tmp_num>='0'&&tmp_num<='9'||tmp_num=='.'){
                    tmp_tran_num+=tmp_num;
                    str_p++;
                    tmp_num=str[str_p];

                }
                str_p--;

                num=Number(tmp_tran_num);
                tmp_tran_num='';
                stack_exp[exp_top++]=num;

        }
        str_p++;

    }

    while (stack_opr[opr_top]!='#'){
        stack_exp[exp_top++]=stack_opr[opr_top--];
    }

    return stack_exp;
}
/**
 * 计算逆波兰式
 * */
function Cal_RPN(stack_exp){
    var stack_cal=new Array();
    var exp_top= 0,cal_top=0;
    var ch='';


    while (exp_top<stack_exp.length){
        ch=stack_exp[exp_top++];

        switch(ch) {
            case '+':
                stack_cal[cal_top-2]=stack_cal[cal_top-2]+stack_cal[cal_top-1];
                cal_top--;
                break;
            case '-':
                stack_cal[cal_top-2]=stack_cal[cal_top-2]-stack_cal[cal_top-1];
                cal_top--;
                break;
            case '*':
                stack_cal[cal_top-2]=stack_cal[cal_top-2]*stack_cal[cal_top-1];
                cal_top--;
                break;
            case '/':
                if (stack_cal[cal_top-1]==0){
                    alert("除数无法为0");
                    break;
                }
                stack_cal[cal_top-2]=stack_cal[cal_top-2]/stack_cal[cal_top-1];
                cal_top--;
                break;
            default :
                stack_cal[cal_top++]=Number(ch);


        }


    }
    //alert(stack_cal[0]);
	$("#answer").val(stack_cal[0]);
}

