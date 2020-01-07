import React from "react"
import PropTypes from "prop-types"



function NavItemContainer(props){
    return (
        <li className = {props.className ? props.className: null}>
            {props.children}
        </li>
    )
}


NavItemContainer.PropTypes = {
    className: PropTypes.string,
    children: PropTypes.arrayOf(
        PropTypes.oneOf(
            PropTypes.node,
            PropTypes.element
        )
    )
}

export default NavItemContainer