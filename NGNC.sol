// SPDX-License-Identifier: MIT
pragma solidity 0.8.17;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract NGNC is ERC20, Ownable {
    constructor(uint256 initialSupply) ERC20("NGNC", "NGNC") {
        _mint(msg.sender, initialSupply);
    }


    function decimals() public view virtual override returns (uint8) {
        return 2;
    }

    function mintTokens(address receiver, uint256 amount) public onlyOwner{
        _mint(receiver, amount);
    }
}