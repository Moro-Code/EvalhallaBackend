import React from "react"
import PropTypes from "prop-types"



function Icon(props){
    return(
        <span className = {`${props.icon}${props.className? " " + props.className: ""}`}></span>
    )
}

Icon.propTypes = {
    icon: PropTypes.string.isRequired,
    className: PropTypes.string
}

export default Icon