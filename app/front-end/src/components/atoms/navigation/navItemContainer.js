import React from "react"
import PropTypes from "prop-types"



function NavItemContainer(props){
    return (
        <div className = {props.className ? props.className: null}>
            {props.children}
        </div>
    )
}


NavItemContainer.propTypes = {
    className: PropTypes.string
}

export default NavItemContainer