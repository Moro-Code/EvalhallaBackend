

// constants for action types
export const TYPES = {
    REQUEST_SURVEYS: "REQUEST_SURVEYS",
    RECIEVE_SURVEYS: "RECIEVE_SURVEYS",
    RECIEVE_SURVEYS_FAILED: "RECIEVE_SURVEYS_FAILED",
    SCREEN_RESIZE: "SCREEN_RESIZE" 
}

export const SCREEN_SIZES = {
    LARGE: "LARGE",
    SMALL: "SMALL"
}

export const RECIEVE_SURVEYS_FAILED_TYPES = {
    NETWORK_ERROR: "NETWORK_ERROR",
    HTTP_ERROR: "HTTP_ERROR"
}


// action creators


// survey loading 
export const requestSurveysCreator = function(){
    return {
        type: TYPES.REQUEST_SURVEYS
    }
}

export const recieveSurveysCreator = function(data, numPosts, pageNumber){
    return{
        type: TYPES.RECIEVE_SURVEYS,
        surveys: data,
        recievedAt: Date.now(),
        pageNumber: pageNumber,
        numberOfItems: numPosts 
    }
}

export const recieveSurveysFailedCreator = function(failure_reason, status){
    return{
        type: TYPES.RECIEVE_SURVEYS_FAILED,
        failedAt: Date.now(),
        failedBecause: failure_reason,
        httpStatus: status
    }
}


// screen size actions
export const changeScreenSizeCreator = function(screenSize){
    return {
        type: TYPES.SCREEN_RESIZE,
        screenSize: screenSize
    }
}