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

        let fetchUrl = EVALHALLA_BACKEND_URL + `?numberOfItems=${numPosts}&pageNumber=${pageNumber}`

        console.log(fetchUrl)
        return fetch(
            fetchUrl
        ).then(
            response => {
                if (response.ok){
                    console.log("recieved response")
                    console.log(response)
                    response.json().then(
                        data => {
                            console.log("data recieved" + data )
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
    console.log("isSurveyFetchCalled")
    const surveys = state.surveys
    console.log(surveys)
    const surveysData = surveys.data
    console.log(surveysData) 
    if ( surveysData.length === 0 ){

        const localstorageSurveys = localStorage.getItem("surveys")
        
        if (!localstorageSurveys){
            return true;
        }
        else{

            dispatch(recieveSurveysCreator(JSON.parse(localstorageSurveys)))
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
        console.log("checking if fetch is needed ?")
        if (isSurveysFetchNeeded(dispatch, getState())) {
            console.log("fetch is needed")
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