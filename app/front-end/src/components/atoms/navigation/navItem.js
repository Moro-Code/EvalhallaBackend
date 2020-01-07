import React from "react"
import PropTypes from "prop-types"



function NavItem(props){
    return (
        <li className = {props.className ? props.className: null}>
            {props.children}
        </li>
    )
}


NavItem.PropTypes = {
    className: PropTypes.string,
    children: PropTypes.arrayOf(
        PropTypes.oneOf(
            PropTypes.node,
            PropTypes.element
        )
    )
}

export default NavItem