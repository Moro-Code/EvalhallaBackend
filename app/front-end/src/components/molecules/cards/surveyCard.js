import React from "react"
import PropTypes from "prop-types"
import SurveyInfo from "./surveyInfo"



function SurveyCard(props){

    const localCreatedOn = new Date(props.createdOn).toLocaleString()

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