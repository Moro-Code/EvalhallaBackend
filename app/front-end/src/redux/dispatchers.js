import fetch from "cross-fetch"
import {
    requestSurveysCreator, 
    recieveSurveysCreator,
    recieveSurveysFailedCreator,
    changeScreenSizeCreator,
    RECIEVE_SURVEYS_FAILED_TYPES
    } from "./actions"
import { EVALHALLA_BACKEND_URL } from "../variables"

export const fetchSurveysDispatcher = function(numPosts=50, pageNumber=1){
    return function(dispatch, getState){

        dispatch(requestSurveysCreator())

        return fetch(
            EVALHALLA_BACKEND_URL + `?numberOfItems=${numPosts}&pageNumber=${pageNumber}`
        ).then(
            response => {
                if (response.ok){
                    response.json().then(
                        data => {
                            dispatch(
                                recieveSurveysCreator(
                                    data,
                                    numPosts,
                                    pageNumber
                                )
                            )
                        }
                    )
                }
                else{
                    dispatch(
                        recieveSurveysFailedCreator(
                            RECIEVE_SURVEYS_FAILED_TYPES.HTTP_ERROR, 
                            response.status
                        )
                    )
                }
            },
            () => dispatch(
                recieveSurveysFailedCreator(
                    RECIEVE_SURVEYS_FAILED_TYPES.NETWORK_ERROR
                )
            )
        )
    }
}

const isSurveysFetchNeeded = (dispatch, state) => {
    const surveys = state.surveys
    const surveysData = surveys.data 
    if ( !surveysData ){
        const localstorageSurveys = JSON.parse(localStorage.getItem("surveys"))
        
        if (! localstorageSurveys){
            return true;
        }
        else{
            dispatch(recieveSurveysCreator(localstorageSurveys))
        }

        const lastUpdated = localStorage.getItem("lastUpdated")
        
        if ( ! lastUpdated ){
            return true 
        }
        
        const lastUpdatedUnixTS = Number(lastUpdated)

        if (isNaN(lastUpdatedUnixTS)){
            return true 
        }

        const timeNow = Date.now()

        if ((timeNow - lastUpdatedUnixTS) >= 12000){
            
            return true 
        }
        
        return false
    }

    const surveysLastUpdated = state.surveys.lastUpdated
    const timeNow = Date.now()

    if ( (timeNow - surveysLastUpdated) >= 12000 ){
        return true 
    }
    return false 
}

export const fetchSurveysIfNeeded = () => {
    return (dispatch, getState) => {
        if (isSurveysFetchNeeded(dispatch, getState())) {
            return dispatch(fetchSurveysDispatcher(100, 1))
        }
        return Promise.resolve()
    }
}

export const fetchNextPageSurveys = () => {
    return (dispatch, getState) => {
        const surveys = getState().surveys
        const surveysData = surveys.data

        if ( ! surveysData ) {
            return dispatch(
                fetchSurveysDispatcher(100,1)
            )
        }

        const pageNumber = surveys.pageNumber
        const numberOfItems = surveys.numberOfItems

        return dispatch(
            fetchSurveysDispatcher(numberOfItems, pageNumber + 1)
        )
    }
}

// screen size dispatchers


export const changeScreenSize = function(screenSize, dispatch){
    dispatch(
        changeScreenSizeCreator(
            screenSize
        )
    )
}