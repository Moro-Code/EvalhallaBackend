import React from "react"
import PropTypes from "prop-types"



function NavWrapper(props){

    return (
        <nav className = {props.className ? props.className: null }>
            {props.children}
        </nav>
    )

}


NavWrapper.PropTypes = {
    className: PropTypes.string,
    children: PropTypes.arrayOf(PropTypes.oneOf([
        PropTypes.node,
        PropTypes.element
    ]).isRequired)
}

export default NavWrapper