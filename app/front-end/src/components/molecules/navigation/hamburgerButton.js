import React from "react"
import PropTypes from "prop-types"
import Icon from "../../atoms/icons/icon"


function HamburgerButton(props){
    return(
        <button onClick = {props.onClick} className = ".hamburgerButtonContainer">
            <Icon icon="icon-hamburger"></Icon>
        </button>
    )
}

HamburgerButton.PropTypes = {
    onClick: PropTypes.func.isRequired,
    screenSize: PropTypes.string.isRequired
}

export default HamburgerButton
