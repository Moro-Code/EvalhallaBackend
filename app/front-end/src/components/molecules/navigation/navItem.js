import React from "react"
import { SCREEN_SIZES } from "../../../redux/actions"
import PropTypes from "prop-types"
import Icon from "../../atoms/icons/icon"
import NavItemContainer from "../../atoms/navigation/navItemContainer"
import NavLink from "../../atoms/navigation/navLink"


function NavItem(props){

    

    const getSizeClass = function(screenSize){
        switch (screenSize){
            case SCREEN_SIZES.LARGE:
                return "lNavItemContainer"
            case SCREEN_SIZES.SMALL:
                return "mNavItemContainer"
            default:
                return "lNavItemContainer"
        }
    }

    return (
        <NavItemContainer className = {`navItemContainer ${getSizeClass(props.screenSize)}`}>
            {
                props.icon && props.icon !== "" ? 
                    <div className="navItemContainerIcon">
                        <Icon icon={props.icon}></Icon>
                    </div>: null 
            }
            <NavLink
                className = "navItemContainerLink"
                link = {props.link}
                linkText = {props.linkText}
            ></NavLink>
        </NavItemContainer>
    )

}



NavItem.propTypes = {
    screenSize: PropTypes.string.isRequired,
    icon: PropTypes.string,
    link: PropTypes.string.isRequired,
    linkText: PropTypes.string.isRequired
}


export default NavItem