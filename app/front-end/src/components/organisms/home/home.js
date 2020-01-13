import React, {useEffect, useState } from "react"
import { shallowEqual, useSelector, useDispatch } from "react-redux"
import SurveyCardList from "../../molecules/cards/surveyCardList"
import Icon from "../../atoms/icons/icon"
import { fetchSurveysIfNeeded } from "../../../redux/dispatchers"



function Home(props){
    const [ showErrorMessage, setShowErrorMessgae ] = useState(false)
    const dispatch = useDispatch()
    const surveyData  = useSelector(
        (state) => {
            return state.surveys.data
        }, shallowEqual
    )
    const isFetching = useSelector(
        (state) => {
            return state.surveys.isFetching
        }
    )
    const fetchFailed = useSelector(
        (state) => {
            return state.surveys.fetchFailed
        }
    )

    useEffect(
        () => {
        
            if ( !isFetching && !fetchFailed && surveyData.length === 0 ){
                console.log("surveys are being fetched")
                dispatch(
                    fetchSurveysIfNeeded()
                )
            }

            if ( fetchFailed && !showErrorMessage){
                setShowErrorMessgae(true)
            }
        }, [isFetching, fetchFailed, surveyData, showErrorMessage, dispatch]
    )

    let title = <h1>Current Surveys</h1>

    if (isFetching && surveyData.length === 0){
        return (
            <main className = "homeContainer">
                {title}
                <div className = "full-page align-center-center">
                    <div className = "large-icon color rotate-center">
                        <Icon icon="icon-loading"
                        ></Icon>
                    </div>
                </div>
            </main>
        )
    }

    return (
        <main className = "homeContainer">
            {title}
            <SurveyCardList surveys = {surveyData}></SurveyCardList>
        </main>
    )

}


export default Home 