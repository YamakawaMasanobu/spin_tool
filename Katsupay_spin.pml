mtype = {s_Item, s_nfc, s_charge, s_suc, s_fail, s_bfail, s_csuc, HTTP_waiting, HTTP_receive,
 press_pay_btn, press_item_charge_btn, press_nfc_cxl_btn, nfc_pay, nfc_charge, press_charge_charge_btn, press_ok_btn, press_toitem_btn, press_tocharge_btn, press_fail_return_btn, press_bfail_return_btn, press_bfail_charge_btn,
 req_HTTP_pay, suc_HTTP_pay, fail_HTTP_pay, req_HTTP_charge, suc_HTTP_charge, fail_HTTP_charge, req_HTTP_getbalance, suc_HTTP_getbalance, fail_HTTP_getbalance
 paytype_none, paytype_charge, paytype_payment};

mtype Screen_state = s_Item;
mtype Server_state = HTTP_waiting;
mtype PayType = paytype_none;
mtype event;

chan Screen_ch = [0] of {mtype};
chan HTTP_ch = [0] of {mtype};

active proctype Screen(){
    do
    ::  Screen_state == s_Item ->
        if
        ::  Screen_ch?press_pay_btn ->
            Screen_state = s_nfc;
            PayType = paytype_payment
        ::  Screen_ch?press_item_charge_btn ->
            Screen_state = s_charge;
            PayType = paytype_charge
        fi
    ::  Screen_state == s_nfc
        do
        ::  Screen_ch?press_nfc_cxl_btn ->
            if
            ::  PayType == paytype_payment -> Screen_state = s_Item
            ::  PayType == paytype_charge -> Screen_state = s_charge
            fi;
            break
        ::  Screen_ch?nfc_pay ->
            HTTP_ch!req_HTTP_pay;
            if
            ::  HTTP_ch?suc_HTTP_pay -> 
                if
                ::  Screen_state = s_suc;
                    HTTP_ch!req_HTTP_getbalance
                ::  Screen_state = s_bfail;
                    HTTP_ch!req_HTTP_getbalance
                fi
            ::  HTTP_ch?fail_HTTP_pay -> Screen_state = s_fail
            fi;
            break
        ::  Screen_ch?nfc_charge ->
            HTTP_ch!req_HTTP_charge
            if
            ::  HTTP_ch?suc_HTTP_charge -> 
                if
                ::  Screen_state = s_csuc;
                    HTTP_ch!req_HTTP_getbalance
                ::  Screen_state = s_bfail;
                    HTTP_ch!req_HTTP_getbalance
                fi
            ::  HTTP_ch?fail_HTTP_charge -> Screen_state = s_fail
            fi;
            break
        od
    ::  Screen_state == s_charge ->
        if
        ::  Screen_ch?press_charge_charge_btn -> Screen_state = s_nfc
        fi
    ::  Screen_state == s_suc -> 
        do
        ::  HTTP_ch?suc_HTTP_getbalance ->
            Screen_ch?press_ok_btn;
            if
            ::  PayType == paytype_payment -> Screen_state = s_Item
            ::  PayType == paytype_charge -> Screen_state = s_charge
            fi;
            break
        ::  HTTP_ch?fail_HTTP_getbalance ->
            Screen_state = s_fail;
            break
        od
    ::  Screen_state == s_csuc ->
        do
        ::  HTTP_ch?suc_HTTP_getbalance ->
            if
            ::  Screen_ch?press_toitem_btn -> Screen_state = s_Item
            ::  Screen_ch?press_tocharge_btn -> Screen_state = s_charge
            fi;
            break
        ::  HTTP_ch?fail_HTTP_getbalance ->
            Screen_state = s_fail;
            break
        od
    ::  Screen_state == s_bfail ->
        do
        ::  HTTP_ch?suc_HTTP_getbalance ->
            if
            ::  Screen_ch?press_bfail_return_btn ->
                if
                ::  PayType == paytype_payment -> Screen_state = s_Item
                ::  PayType == paytype_charge -> Screen_state = s_charge
                fi 
            ::  Screen_ch?press_bfail_charge_btn ->
                Screen_state = s_charge
            fi;
            break
        ::  HTTP_ch?fail_HTTP_getbalance ->
            Screen_state = s_fail;
            break
        od
    ::  Screen_state == s_fail ->
        if
        ::  Screen_ch?press_fail_return_btn ->
            if
            ::  PayType == paytype_payment -> Screen_state = s_Item
            ::  PayType == paytype_charge -> Screen_state = s_charge
            fi
        fi  
    ::  else -> skip
    od
}

active proctype User(){
    do
    ::  Screen_state == s_Item ->
        if
        ::  Screen_ch!press_pay_btn;
            Screen_state == s_nfc
        ::  Screen_ch!press_item_charge_btn;
            Screen_state == s_charge
        fi
    ::  Screen_state == s_nfc ->
        if
        ::  Screen_ch!press_nfc_cxl_btn
            do
            ::  Screen_state == s_Item -> break
            ::  Screen_state == s_charge -> break
            od
        ::  Screen_ch!nfc_pay
            do
            ::  Screen_state == s_suc -> break
            ::  Screen_state == s_bfail -> break
            ::  Screen_state == s_fail -> break
            od
        ::  Screen_ch!nfc_charge
            do
            ::  Screen_state == s_csuc -> break
            ::  Screen_state == s_bfail -> break
            ::  Screen_state == s_fail -> break
            od
        fi
    ::  Screen_state == s_charge -> Screen_ch!press_charge_charge_btn
        Screen_state == s_nfc
    ::  Screen_state == s_suc -> Screen_ch!press_ok_btn
        do
        ::  Screen_state == s_Item -> break
        ::  Screen_state == s_charge -> break
        od
    ::  Screen_state == s_csuc -> 
        if
        ::  Screen_ch!press_toitem_btn;
            Screen_state == s_Item
        ::  Screen_ch!press_tocharge_btn;
            Screen_state == s_charge
        fi
    ::  Screen_state == s_bfail ->
        if
        ::  Screen_ch!press_bfail_return_btn;
            do
            ::  Screen_state == s_Item -> break
            ::  Screen_state == s_charge -> break
            od
        ::  Screen_ch!press_bfail_charge_btn;
            Screen_state == s_charge
        fi
    ::  Screen_state == s_fail -> Screen_ch!press_fail_return_btn
        do
        ::  Screen_state == s_Item -> break
        ::  Screen_state == s_charge -> break
        od
    ::  else -> skip
    od
}

active proctype Server(){
    do
    ::  Server_state == HTTP_waiting ->
        if
        ::  HTTP_ch?req_HTTP_pay ->
            Server_state = HTTP_receive;
            if
            ::  HTTP_ch!suc_HTTP_pay
            ::  HTTP_ch!fail_HTTP_pay
            fi;
            Server_state = HTTP_waiting
        ::  HTTP_ch?req_HTTP_charge ->
            Server_state = HTTP_receive;
            if
            ::  HTTP_ch!suc_HTTP_charge
            ::  HTTP_ch!fail_HTTP_charge
            fi;
            Server_state = HTTP_waiting
        ::  HTTP_ch?req_HTTP_getbalance ->
            Server_state = HTTP_receive;
            if
            ::  HTTP_ch!suc_HTTP_getbalance
            ::  HTTP_ch!fail_HTTP_getbalance
            fi;
            Server_state = HTTP_waiting
        fi
    od
}