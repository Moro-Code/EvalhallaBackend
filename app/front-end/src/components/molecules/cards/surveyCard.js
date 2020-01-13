import React from "react"
import PropTypes from "prop-types"
import SurveyInfo from "./surveyInfo"
import * as moment from "moment-timezone"



function SurveyCard(props){
    const tzGuess = moment.tz.guess()
    console.log(tzGuess)
    const localCreatedOn = moment(props.createdOn + "Z").tz(tzGuess).format(
        "MMMM Do YYYY, h:mm:ss a"
    )

    return (
        <article className = "surveyCard">
            <SurveyInfo itemName = {"Title"}
             itemData = {props.title}></SurveyInfo>
            <SurveyInfo itemName = {"UUID"}
             itemData = {props.uuid}></SurveyInfo>
            <SurveyInfo itemName = {"Created On"}
             itemData = {localCreatedOn}></SurveyInfo> 
        </article>
    )

}


SurveyCard.propTypes = {
    title: PropTypes.string.isRequired,
    uuid: PropTypes.string.isRequired,
    createdOn: PropTypes.string.isRequired
}


export default SurveyCard;