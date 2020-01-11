import React from "react"
import PropTypes from "prop-types"
import Icon from "../../atoms/icons/icon"


function CloseButton(props){
    return (
        <button onClick = {props.onClick} className = "closeButtonContainer">
            <Icon icon="icon-close"></Icon>
        </button>
    )
}


CloseButton.propTypes = {
    onClick: PropTypes.func.isRequired
}

export default CloseButton;