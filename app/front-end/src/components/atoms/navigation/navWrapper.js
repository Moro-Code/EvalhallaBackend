import React from "react"
import PropTypes from "prop-types"



function NavWrapper(props){

    return (
        <nav className = {props.className ? props.className: null }>
            {props.children}
        </nav>
    )

}


NavWrapper.propTypes = {
    className: PropTypes.string,
}

export default NavWrapper