import React from "react"
import PropTypes from "prop-types"
import Icon from "../../atoms/icons/icon"
import NavItem from "../../atoms/navigation/navItem"
import NavLink from "../../atoms/navigation/navLink"


function IconNavItem(props){
    return (
        <NavItem className = "iconNavItem">
            <div className="iconNavItemIconContainer">
                <Icon icon={props.icon}></Icon>
            </div>
            <NavLink
                className = "iconNavItemLink"
                link = {props.link}
                linkText = {props.linkText}
            ></NavLink>
        </NavItem>
    )

}



IconNavItem.PropTypes = {
    icon: PropTypes.string.isRequired,
    link: PropTypes.string.isRequired,
    linkText: PropTypes.string.isRequired
}


export default IconNavItem