import React from "react"
import PropTypes from "prop-types"



function NavItemContainer(props){
    return (
        <div className = {props.className ? props.className: null}>
            {props.children}
        </div>
    )
}


NavItemContainer.PropTypes = {
    className: PropTypes.string,
    children: PropTypes.arrayOf(
        PropTypes.oneOf([
            PropTypes.node,
            PropTypes.element
        ])
    )
}

export default NavItemContainer