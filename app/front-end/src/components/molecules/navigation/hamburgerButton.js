import React from "react"
import PropTypes from "prop-types"
import Icon from "../../atoms/icons/icon"


function HamburgerButton(props){
    return(
        <button onClick = {props.onClick} className = "hamburgerButtonContainer">
            <Icon icon="icon-hamburger"></Icon>
        </button>
    )
}

HamburgerButton.propTypes = {
    onClick: PropTypes.func.isRequired,
}

export default HamburgerButton
