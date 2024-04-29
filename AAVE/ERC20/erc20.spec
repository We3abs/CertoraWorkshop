/* TODO: write ERC20 specifications
*
* transfer(recipient, amount) should tranfer 'amount' tokens from msg.sender to recipient
*/


methods {
    // balanceOf doesn't depend on msg.sender, block.timestamp, ...
    function balanceOf(address) external returns (uint256) envfree;

}

rule transferIncreasesRecipientBalance {
    address recipient;  
    uint amount;
    address sender;
    address anybody_else;

    require sender != recipient;
    require anybody_else != sender;
    require anybody_else != recipient;


    // using mathint cause we dont want to overflow
    mathint balance_recipient_before = balanceOf(recipient);
    mathint balance_sender_before = balanceOf(sender);
    mathint balance_other_before = balanceOf(anybody_else);
   
    //call 
    env e;
    require e.msg.sender == sender;
    bool success = transfer(e, recipient, amount);     

    mathint balance_recipient_after = balanceOf(recipient);
    mathint balance_sender_after = balanceOf(sender);
    mathint balance_other_after = balanceOf(anybody_else);


       
    //assert


    assert balance_other_after == balance_other_before,
        "transfer must not change anybody else's balance";

    assert balance_recipient_after == balance_recipient_before + amount,
        "transfer(recipient,amount) must increase recipient's balance by amount";

    assert balance_sender_after == balance_sender_before - amount,
    "transfer must reduce sender's balance by amount";
      

}

rule transferRevertConditions {
    address recipient; address sender;
    uint amount;
    address anybody_else;
    env e;


 mathint balance_recipient_before = balanceOf(recipient);
    mathint balance_sender_before = balanceOf(sender);
    mathint balance_other_before = balanceOf(anybody_else);

transfer@withrevert(e, recipient, amount);

// assert amount > balance_sender_before => lastReverted,
//     "transfer must revert if sender's balance is insufficient";

// assert balance_recipient_before +amount >= max_uint256 => lastReverted,
//     "transfer must revert if recipient's account would overflow";

// assert recipient == 0 => lastReverted,
//     "transfer must revert if recipient is 0";

assert lastReverted <=> (
    amount > assert_uint256(balance_sender_before)
    || balance_recipient_before + amount >= max_uint256 
    || recipient == 0
), "transfer must only revert if one of the three revert conditions is true";
}