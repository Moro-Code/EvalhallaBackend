import React from "react"
import PropTypes from "prop-types"
import { Link, useLocation } from "react-router-dom"



function navListItem(props) {

    const location = useLocation()

    const getClassString = (pathname) => {
        if ( pathname === props.link){
            return props.activeClassName ? props.activeClassName: null
        }
        return props.className ? props.activeClassName: null 
    }

    return (
        <li className = {getClassString(location.pathname)}>
            <Link to= { props.link }>
                {props.linkText}
            </Link>
        </li>
    )
    
}


navListItem.PropTypes = {
    className: PropTypes.string,
    activeClassName: PropTypes.string,
    linkText: PropTypes.string.isRequired,
    link: PropTypes.string.isRequired
}

export default navListItem