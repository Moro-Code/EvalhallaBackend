import React from "react"
import PropTypes from "prop-types"
import SurveyCard from "./surveyCard"



function SurveyCardList(props){

    return (
        <main className = "surveysContainer">
            {
                props.surveys.map( (survey) => {
                    return( 
                        <SurveyCard
                        key = {survey.uuid}
                        title = {survey.surveyName}
                        uuid = {survey.uuid}
                        createdOn = {survey.createdOn}
                        >
                        </SurveyCard>
                    )
                })
            }
        </main>
    )
    
}



SurveyCardList.propTypes = {
    surveys: PropTypes.arrayOf(
        PropTypes.shape(
            {
                surveyName: PropTypes.string.isRequired,
                uuid: PropTypes.string.isRequired,
                createdOn: PropTypes.string.isRequired
            }
        )
    )
}

export default SurveyCardList