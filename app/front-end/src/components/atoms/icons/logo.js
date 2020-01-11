import React from "react"
import PropTypes from "prop-types"



function Logo(props){
    return (
        <span className={
            props.className && props.className !== "" ? 
            props.className: null
        }
            style = {{
            fontFamily: "Pacifico, cursive"
        }}>Evalhalla Admin Panel</span>
    )
}

Logo.propTypes = {
    className: PropTypes.string
}

export default Logo