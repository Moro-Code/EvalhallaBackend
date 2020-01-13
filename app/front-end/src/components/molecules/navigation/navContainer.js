import React from "react"
import PropTypes from "prop-types"
import NavItem from "./navItem"
import NavWrapper from "../../atoms/navigation/navWrapper"
import { SCREEN_SIZES } from "../../../redux/actions"



function NavContainer(props){

    const renderNavItems = (links) => {
        let itemComponentArray = []
        for ( let link in links){
            itemComponentArray.push(
                <NavItem  link = {links[link].link } linkText = {links[link].linkText} icon = {links[link].icon} screenSize = {props.screenSize}> 
                </NavItem>
            )
        }

        return React.createElement(
            React.Fragment,null, ...itemComponentArray
        )
    }


    let getScreenCSS = (screenSize) => {
        switch(screenSize){
            case SCREEN_SIZES.LARGE:
                return "lNavContainer"
            case SCREEN_SIZES.SMALL:
                return "mNavContainer"
            default:
                return "lNavContainer"
        }
    }


    return (
        <NavWrapper className = {`navContainer ${getScreenCSS(props.screenSize)}`}>
            {
                renderNavItems(props.links)
            }
        </NavWrapper>
        
    )

}

NavContainer.propTypes = {
    links: PropTypes.arrayOf(
        PropTypes.shape(
            {
                link: PropTypes.string.isRequired,
                linkText: PropTypes.string.isRequired,
                icon: PropTypes.string
            }
        )
    ),
    screenSize: PropTypes.string.isRequired
}

export default NavContainer