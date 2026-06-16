// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@aave/core-v3/contracts/interfaces/IPoolAddressesProvider.sol";
import "@aave/core-v3/contracts/flashloan/base/FlashLoanSimpleReceiverBase.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract FlashLoanExecutor is FlashLoanSimpleReceiverBase {

    address public owner;

    constructor(address _provider)
        FlashLoanSimpleReceiverBase(IPoolAddressesProvider(_provider))
    {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "NOT_OWNER");
        _;
    }

    function executeFlashLoan(
        address asset,
        uint256 amount,
        bytes calldata params
    ) external onlyOwner {

        POOL.flashLoanSimple(
            address(this),
            asset,
            amount,
            params,
            0
        );
    }

    // callback Aave
    function executeOperation(
        address asset,
        uint256 amount,
        uint256 premium,
        address initiator,
        bytes calldata params
    ) external override returns (bool) {

        require(msg.sender == address(POOL), "NOT_POOL");
        require(initiator == address(this), "BAD_INITIATOR");

        // params = encoded strategy data (swap route ecc.)
        _executeStrategy(params);

        uint256 totalOwed = amount + premium;

        IERC20(asset).approve(address(POOL), totalOwed);

        return true;
    }

    function _executeStrategy(bytes calldata params) internal {
        // TODO: qui inseriamo router swaps (Uniswap / Aerodrome)
        // per ora è placeholder
    }

    function withdraw(address token) external onlyOwner {
        IERC20(token).transfer(
            msg.sender,
            IERC20(token).balanceOf(address(this))
        );
    }
}
