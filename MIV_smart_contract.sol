//MIV coin ICO for studying purposes
pragma solidity ^0.8.4;
contract mivcoin_ico {
    
    //max number of available coins
    uint public max_mivcoins = 100000000;
    
    //usd to mivcoin conversion rate
    uint public usd_to_mivcoin = 1000;
    
    //introduce total number of mivcoin coins that have been bought by the investors
    uint public total_mivcoins_bought = 0;
    
    //mapping from the investor address to its equity in mivcoin and usd
    mapping(address => uint) equity_mivcoins;
    mapping(address => uint) equity_usd;
    
    //check or investor can buy mivcoin
    modifier can_buy_mivcoin(uint usd_invested) {
        require (usd_invested * usd_to_mivcoin + total_mivcoins_bought <= max_mivcoins);
        _;
    }
    
    //getting equity in mivcoins of an investor
    function equity_in_mivcoins(address investor) external constant returns (uint) {
        return equity_mivcoins[investor];
    }
    
    //getting equity in USD of an investor
    function equity_in_usd(address investor) external constant returns (uint) {
        return equity_usd[investor];
    }
    
    //buying mivcoins
    function buy_mivcoin(address investor, uint usd_invested) external
    can_buy_mivcoin(usd_invested) {
        uint mivcoins_bought = usd_invested * usd_to_mivcoin;
        equity_mivcoins[investor] += mivcoins_bought;  
        equity_usd[investor] = equity_mivcoins[investor] / 1000;
        total_mivcoins_bought += mivcoins_bought;
    }
    
    //selling mivcoins
    function sell_mivcoin(address investor, uint mivcoins_sold) external {
        equity_mivcoins[investor] -= mivcoins_sold;  
        equity_usd[investor] = equity_mivcoins[investor] / 1000;
        total_mivcoins_bought -= mivcoins_sold;
    }
}