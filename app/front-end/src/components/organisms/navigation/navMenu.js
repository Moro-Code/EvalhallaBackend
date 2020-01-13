import React, {useState} from "react"
import { useSelector } from "react-redux"
import PropTypes from "prop-types"
import Logo from "../../atoms/icons/logo"
import HamburgerButton from "../../molecules/navigation/hamburgerButton"
import NavContainer from "../../molecules/navigation/navContainer"
import MobileNavMenu from "./mobileNavMenu"
import { SCREEN_SIZES } from "../../../redux/actions"




function NavMenu(props){

    const screenSize = useSelector( (state) => state.screenSize)

    const [ navMenuOpen, setNavMenuOpen ] = useState(false)

    let openMobileNav = (e) => {
        if (navMenuOpen === false ){
            console.log("WHHHYYYYY")
            setNavMenuOpen(true)
        }
    }

    let closeMobileNav = (e) => {
        if (navMenuOpen === true){
            setNavMenuOpen(false)
        }
    }

    return (
        <> 
            
            <div className= "navMenu">
                <div 
                    className = "navMenuLogoContainer">
                    <Logo className="navMenuLogo"></Logo>
                </div>
                { 
                    screenSize === SCREEN_SIZES.LARGE ?
                        <NavContainer screenSize = {screenSize} links = {props.links}>
                        </NavContainer>: null
                }
                {
                    screenSize === SCREEN_SIZES.SMALL ? 
                        <HamburgerButton onClick = {openMobileNav}></HamburgerButton>: null 
                }
            </div>
            {
                screenSize === SCREEN_SIZES.SMALL && navMenuOpen ?
                    <MobileNavMenu links = {props.links} closeOnClick = {closeMobileNav}>

                    </MobileNavMenu>: null 
            }
        </>
    )

}




NavMenu.propTypes = {
    links: PropTypes.arrayOf(
        PropTypes.shape(
            {
                link: PropTypes.string.isRequired,
                linkText: PropTypes.string.isRequired,
                icon: PropTypes.string
            }
        )
    ).isRequired
}

export default NavMenu