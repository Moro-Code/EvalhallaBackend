import React from "react"
import { useSelector } from "react-redux"
import { SCREEN_SIZES } from "../../../redux/actions"
import PropTypes from "prop-types"
import Icon from "../../atoms/icons/icon"
import NavItemContainer from "../../atoms/navigation/navItemContainer"
import NavLink from "../../atoms/navigation/navLink"


function NavItem(props){

    const screenSize = useSelector( (state) => state.screenSize )

    const getLinkColor = function(screenSize){
        switch (screenSize){
            case SCREEN_SIZES.LARGE:
                return "lColor"
            case SCREEN_SIZES.SMALL:
                return "mColor"
            default:
                return "lColor"
        }
    }

    return (
        <NavItemContainer className = {`navItemContainer ${getLinkColor(screenSize)}`}>
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



NavItem.PropTypes = {
    icon: PropTypes.string,
    link: PropTypes.string.isRequired,
    linkText: PropTypes.string.isRequired
}


export default NavItem