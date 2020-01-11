import React from "react"
import PropTypes from "prop-types"
import { SCREEN_SIZES } from "../../../redux/actions"
import NavContainer from "../../molecules/navigation/navContainer"
import CloseButton from "../../molecules/navigation/closeButton"




function MobileNavMenu(props){
    return(
        <div className="mobileNavMenu slide-left">
            <div className = "mobileNavMenuLogoContainer">
                <div className = "align-end-center">
                    <CloseButton onClick = {props.closeOnClick}></CloseButton>
                </div>
            </div>
            <NavContainer screenSize = {SCREEN_SIZES.SMALL} 
                        links={props.links}>
            </NavContainer>
        </div>
    ) 
}

MobileNavMenu.propTypes = {
    links: PropTypes.arrayOf(
        PropTypes.objectOf(
            PropTypes.shape(
                {
                    link: PropTypes.string.isRequired,
                    linkText: PropTypes.string.isRequired,
                    icon: PropTypes.string
                }
            )
        )
    ).isRequired,
    closeOnClick: PropTypes.func.isRequired
}

export default MobileNavMenu