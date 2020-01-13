import React from "react"
import PropTypes from "prop-types"


function SurveyInfo(props){

    return(
        <div className = "surveyCardInfo">
            <span><b>{props.itemName}</b></span>
            <span>{props.itemData}</span>
        </div>
    )

}


SurveyInfo.propTypes = {
    itemName: PropTypes.string.isRequired,
    itemData: PropTypes.oneOfType(
        [
            PropTypes.string,
            PropTypes.number
        ]
    ).isRequired
}

export default SurveyInfo