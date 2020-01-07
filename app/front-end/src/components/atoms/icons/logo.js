import React from "react"
import PropTypes from "prop-types"



function Logo(props){
    return (
        <span className={
            props.className && props.className !== "" ? 
            props.className: null
        }
            style = {{
            fontFamily: "Pacifico"
        }}>Evalhalla Admin Panel</span>
    )
}

Logo.PropTypes = {
    className: PropTypes.string
}

export default Logo