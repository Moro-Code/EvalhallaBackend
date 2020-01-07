import React from "react"
import PropTypes from "prop-types"
import { NavLink } from "react-router-dom"



function NavList(props) {
    return(
        <ul className = {props.className? props.className: null }>
            {props.children}
        </ul>
    )
}

NavList.PropTypes = {
    children: PropTypes.arrayOf(PropTypes.element),
    className: PropTypes.string
}

export default NavList