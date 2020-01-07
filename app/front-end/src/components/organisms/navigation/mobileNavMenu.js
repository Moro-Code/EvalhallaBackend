import React from "react"
import PropTypes from "prop-types"
import { SCREEN_SIZES } from "../../../redux/actions"
import 
import NavContainer from "../../molecules/navigation/navContainer"




function MobileNavMenu(props){

}

MobileNavMenu.PropTypes = {
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
    )
}