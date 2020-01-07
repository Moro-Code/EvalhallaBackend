import React from "react"
import PropTypes from "prop-types"



function Icon(props){
    return(
        <span className = {`${props.icon}${props.className? " " + props.className: ""}`}></span>
    )
}

Icon.PropTypes = {
    icon: PropTypes.string.isRequired,
    className: PropTypes.string
}