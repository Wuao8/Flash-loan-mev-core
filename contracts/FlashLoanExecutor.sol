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

    address tokenIn;
    address tokenMid;
    address router1;
    address router2;
    uint256 amount;

    (tokenIn, tokenMid, router1, router2, amount) =
        abi.decode(params, (address, address, address, address, uint256));

    uint256 balanceBefore = IERC20(tokenIn).balanceOf(address(this));

    IERC20(tokenIn).approve(router1, amount);

    _swap(router1, tokenIn, tokenMid, amount);

    uint256 midBalance = IERC20(tokenMid).balanceOf(address(this));

    IERC20(tokenMid).approve(router2, midBalance);

    _swap(router2, tokenMid, tokenIn, midBalance);

    uint256 balanceAfter = IERC20(tokenIn).balanceOf(address(this));

    // 🔥 PROFIT CHECK ON-CHAIN
    require(balanceAfter > balanceBefore, "NO_PROFIT_REVERT");
}



    function withdraw(address token) external onlyOwner {
        IERC20(token).transfer(
            msg.sender,
            IERC20(token).balanceOf(address(this))
        );
    }
}

function _swap(
    address router,
    address tokenIn,
    address tokenOut,
    uint256 amount
) internal {

    // bytes payload standard UniswapV2-style
    bytes memory data = abi.encodeWithSignature(
        "swapExactTokensForTokens(uint256,uint256,address[],address,uint256)",
        amount,
        0,
        _path(tokenIn, tokenOut),
        address(this),
        block.timestamp
    );

    (bool success, ) = router.call(data);
    require(success, "SWAP_FAILED");
}

function _path(address tokenIn, address tokenOut)
    internal
    pure
    returns (address[] memory path)
{
    path = new address[](2);
    path[0] = tokenIn;
    path[1] = tokenOut;
}
